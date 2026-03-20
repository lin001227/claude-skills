#!/usr/bin/env python3
"""
commit-code 技能的安全检查模块
用于检测潜在的安全风险和提交质量问题
"""

import os
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from file_type_detector import FileTypeDetector


class SecurityChecker:
    """
    提交安全检查器
    检测潜在的安全风险和质量问题
    """

    # 需要检查的敏感词
    SENSITIVE_PATTERNS = [
        # 密钥相关
        r'[\'"]\s*(password|secret|token|key|credential|auth|api_key|access_token)[\s\'"]*[:=][\s\'"]*[a-zA-Z0-9_\-]{10,}',
        r'(?:^|\s)(AKIA[A-Z0-9]{16}|[0-9]+-[0-9A-Za-z_]{32}|gh[pousr]_[A-Za-z0-9_]{35,}|ssh-rsa\s+[A-Za-z0-9+\/]{50,})',

        # SQL 注入风险
        r"(?i)(select|drop|union|insert|delete|update)\s+.*(?:from|where|into|values)",

        # 潜在的安全漏洞
        r"(?i)(eval\s*\(|exec\s*\(|os\.system\(|subprocess\.call\(|shell=True)",

        # 敏感文件路径
        r'(/etc/|C:\\Windows\\|/root/|/home/)',

        # 调试代码
        r"(?i)(console\.log|print\(|System\.out\.println|pdb\.set_trace\(\)|breakpoint\(\))",
    ]

    # 忽略的文件类型
    IGNORE_FILE_TYPES = {
        'image', 'audio', 'video', 'font',  # 媒体文件
        'env', 'config'  # 配置文件（通常被.gitignore忽略）
    }

    def __init__(self):
        self.file_detector = FileTypeDetector()

    def check_file_for_secrets(self, filepath: str) -> List[Dict]:
        """
        检查单个文件中的敏感信息
        """
        results = []

        # 如果是二进制文件，跳过检查
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read(10000)  # 只读取前10KB以提高性能
        except UnicodeDecodeError:
            # 文件不是文本文件，跳过
            return results

        # 检查每个敏感模式
        for i, pattern in enumerate(self.SENSITIVE_PATTERNS):
            matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                results.append({
                    'file': filepath,
                    'pattern_index': i,
                    'match': match.group(0)[:100],  # 只保存前100个字符的匹配
                    'start_pos': match.start(),
                    'end_pos': match.end(),
                    'line_number': content[:match.start()].count('\n') + 1,
                    'type': self._get_pattern_type(i)
                })

        return results

    def _get_pattern_type(self, idx: int) -> str:
        """
        获取模式类型描述
        """
        types = [
            '硬编码密钥/密码',
            'API密钥/访问令牌',
            'SQL注入风险',
            '潜在代码执行漏洞',
            '敏感文件路径',
            '调试代码'
        ]
        return types[idx] if idx < len(types) else '未知风险'

    def check_git_staged_for_risks(self) -> Dict:
        """
        检查Git暂存区中的风险
        """
        # 获取暂存的文件列表
        result = subprocess.run(['git', 'diff', '--cached', '--name-only'],
                              capture_output=True, text=True)
        staged_files = result.stdout.strip().split('\n') if result.stdout.strip() else []

        all_risks = []
        risk_summary = {
            'total_risks': 0,
            'by_type': {},
            'by_file': {},
            'critical_files': []  # 存在高风险的文件
        }

        for filepath in staged_files:
            if not filepath or filepath == "":
                continue

            # 获取文件元数据
            meta = self.file_detector.get_file_metadata(filepath)

            # 如果是应该忽略的文件类型，跳过检查
            if meta['purpose'] in self.IGNORE_FILE_TYPES:
                continue

            # 检查暂存的更改中是否包含敏感信息
            diff_result = subprocess.run(['git', 'diff', '--cached', '--unified=0', filepath],
                                       capture_output=True, text=True)

            if diff_result.stdout:
                # 检查差异内容
                for i, pattern in enumerate(self.SENSITIVE_PATTERNS):
                    matches = re.finditer(pattern, diff_result.stdout, re.IGNORECASE | re.MULTILINE)
                    for match in matches:
                        risk_info = {
                            'file': filepath,
                            'pattern_index': i,
                            'match': match.group(0)[:100],
                            'context': self._get_context(diff_result.stdout, match.start()),
                            'type': self._get_pattern_type(i),
                            'severity': self._get_severity(i)
                        }

                        all_risks.append(risk_info)

                        # 更新统计
                        risk_summary['total_risks'] += 1
                        risk_type = risk_info['type']
                        risk_summary['by_type'][risk_type] = risk_summary['by_type'].get(risk_type, 0) + 1

                        if filepath not in risk_summary['by_file']:
                            risk_summary['by_file'][filepath] = []
                        risk_summary['by_file'][filepath].append(risk_info)

                        if risk_info['severity'] == 'critical':
                            if filepath not in risk_summary['critical_files']:
                                risk_summary['critical_files'].append(filepath)

        risk_summary['risks'] = all_risks
        return risk_summary

    def _get_context(self, content: str, pos: int, context_size: int = 50) -> str:
        """
        获取匹配项周围的上下文
        """
        start = max(0, pos - context_size)
        end = min(len(content), pos + context_size)
        return content[start:end]

    def _get_severity(self, pattern_idx: int) -> str:
        """
        获取风险严重程度
        """
        # 高风险：硬编码密钥、API密钥
        if pattern_idx in [0, 1]:
            return 'critical'
        # 中风险：SQL注入、代码执行
        elif pattern_idx in [2, 3]:
            return 'high'
        # 低风险：调试代码等
        else:
            return 'medium'

    def generate_security_report(self, risk_summary: Dict) -> str:
        """
        生成安全报告
        """
        if risk_summary['total_risks'] == 0:
            return "✅ 未发现明显的安全风险"

        report = ["⚠️  发现潜在安全风险:", "="*50]

        # 按文件汇总
        for filepath, risks in risk_summary['by_file'].items():
            report.append(f"\n📄 文件: {filepath}")
            for risk in risks:
                severity_symbol = {
                    'critical': '🔴',
                    'high': '🟠',
                    'medium': '🟡',
                    'low': '🔵'
                }.get(risk['severity'], '⚪')

                report.append(f"  {severity_symbol} [{risk['severity'].upper()}] {risk['type']}")
                report.append(f"     匹配: ...{risk['match']}...")

        # 总结
        report.append(f"\n📈 风险统计:")
        for risk_type, count in risk_summary['by_type'].items():
            report.append(f"  • {risk_type}: {count} 处")

        if risk_summary['critical_files']:
            report.append(f"\n🚨 高风险文件:")
            for critical_file in risk_summary['critical_files']:
                report.append(f"  • {critical_file}")

        report.append(f"\n💡 建议:")
        report.append(f"  • 在提交前移除所有敏感信息")
        report.append(f"  • 使用环境变量或密钥管理服务存储密钥")
        report.append(f"  • 审查SQL查询和系统调用代码")

        return "\n".join(report)


def validate_commit_message(message: str) -> List[str]:
    """
    验证提交消息是否符合规范
    """
    errors = []

    if not message or message.strip() == "":
        errors.append("提交消息不能为空")
        return errors

    # 检查长度
    if len(message) > 72:
        errors.append("提交消息应不超过72个字符")

    # 检查是否以小写字母开头（除非是缩写)
    lines = message.split('\n')
    first_line = lines[0] if lines else ""

    if first_line:
        # 检查是否符合 Conventional Commits 规范
        conventional_pattern = r'^(build|chore|ci|docs|feat|fix|perf|refactor|revert|style|test)(\(.+\))?: .+'
        if not re.match(conventional_pattern, first_line):
            errors.append("建议使用 Conventional Commits 格式: type(scope): description")

        # 检查第一行是否以大写字母开头
        desc_part = first_line
        if ':' in first_line:
            desc_part = first_line.split(':', 1)[1].strip()

        if desc_part and not desc_part[0].isupper() and not re.match(r'^[A-Z]{2,}', desc_part):
            errors.append("描述部分应以大写字母开头")

        # 检查是否以句号结尾
        if desc_part and desc_part[-1] == '.':
            errors.append("提交消息不应以句号结尾")

    # 检查空行分隔（如果有正文部分）
    if len(lines) > 1:
        if lines[1] != "":
            errors.append("提交消息标题和正文之间应有空行分隔")

    return errors


def main():
    """
    测试安全检查功能
    """
    print("🛡️  安全检查模块测试")

    # 创建安全检查器实例
    checker = SecurityChecker()

    # 执行安全检查
    print("\n🔍 正在检查暂存区的安全风险...")
    risk_summary = checker.check_git_staged_for_risks()

    # 生成报告
    report = checker.generate_security_report(risk_summary)
    print(report)

    # 测试提交消息验证
    print(f"\n📋 提交消息验证测试:")
    print("-" * 30)

    test_messages = [
        "feat(user-auth): add login functionality",  # 应该通过
        "fix bug that caused crash",  # 应该有问题
        "docs(readme): update installation instructions",  # 应该通过
        "add new feature"  # 应该有问题
    ]

    for msg in test_messages:
        errors = validate_commit_message(msg)
        status = "✅" if not errors else "❌"
        print(f"{status} '{msg}'")
        if errors:
            for error in errors:
                print(f"   • {error}")
        print()


if __name__ == "__main__":
    main()