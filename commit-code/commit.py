#!/usr/bin/env python3
"""
commit-code 技能核心脚本
用于分析 Git 更改并生成高质量的提交信息
"""

import os
import subprocess
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple


def run_command(cmd: str) -> Tuple[str, bool]:
    """运行shell命令并返回输出和是否成功"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=False
        )
        success = result.returncode == 0
        return result.stdout.strip(), success
    except Exception as e:
        return f"Error: {str(e)}", False


def is_git_repo() -> bool:
    """检查当前目录是否为Git仓库"""
    _, success = run_command("git rev-parse --git-dir")
    return success


def get_git_status() -> Dict:
    """获取Git状态详情"""
    status_short, _ = run_command("git status --porcelain")

    staged_files = []
    unstaged_files = []
    untracked_files = []

    for line in status_short.split('\n'):
        if not line.strip():
            continue

        # 解析 Git 状态输出 (XY filepath)
        x = line[0] if line[0] != ' ' else ''
        y = line[1] if len(line) > 1 and line[1] != ' ' else ''
        filepath = line[3:].strip()

        if x in ['A', 'M', 'D', 'R', 'C'] or (x == ' ' and y in ['M', 'D']):
            # 文件已暂存
            staged_files.append({'file': filepath, 'status': x + y})
        elif x == '?' and y == '?':
            # 未跟踪文件
            untracked_files.append(filepath)
        else:
            # 未暂存文件
            unstaged_files.append({'file': filepath, 'status': x + y})

    return {
        'staged': staged_files,
        'unstaged': unstaged_files,
        'untracked': untracked_files
    }


def analyze_file_type(filepath: str) -> str:
    """分析文件类型"""
    ext = Path(filepath).suffix.lower()

    # 映射文件扩展名到文件类型
    type_map = {
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.py': 'python',
        '.java': 'java',
        '.cpp': 'cpp',
        '.c': 'c',
        '.h': 'c_header',
        '.cs': 'csharp',
        '.rb': 'ruby',
        '.php': 'php',
        '.go': 'go',
        '.rs': 'rust',
        '.vue': 'vue',
        '.html': 'html',
        '.htm': 'html',
        '.css': 'css',
        '.scss': 'scss',
        '.sass': 'sass',
        '.less': 'less',
        '.json': 'json',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.xml': 'xml',
        '.md': 'markdown',
        '.txt': 'text',
        '.sql': 'sql',
        '.sh': 'shell',
        '.dockerfile': 'docker',
        'dockerfile': 'docker',
        '.env': 'config',
    }

    # 检查是否为特定类型的文件
    basename = Path(filepath).name.lower()

    if any(name in basename for name in ['readme', 'license', 'changelog', 'contributing']):
        return 'documentation'

    if any(ext in ['.md', '.txt', '.rst'] or 'readme' in basename):
        return 'documentation'

    if any(ext in ['.css', '.scss', '.sass', '.less']):
        return 'style'

    if any(name in ['package.json', 'requirements.txt', 'setup.py', 'pipfile', 'gemfile', 'cargo.toml']):
        return 'dependency'

    if any('test' in name or 'spec' in name or ext in ['.test.js', '.spec.js']):
        return 'test'

    return type_map.get(ext, 'other')


def classify_change_type(staged_files: List[Dict]) -> str:
    """根据更改的文件推断变更类型"""
    file_types = [analyze_file_type(f['file']) for f in staged_files]

    # 计算最常见的文件类型
    type_counts = {}
    for ftype in file_types:
        type_counts[ftype] = type_counts.get(ftype, 0) + 1

    # 根据最常见的文件类型决定提交类型
    if 'documentation' in type_counts:
        return 'docs'
    elif 'style' in type_counts:
        return 'style'
    elif 'test' in type_counts:
        return 'test'
    elif 'dependency' in type_counts:
        return 'build'
    else:
        # 检查更改内容中是否有错误修复相关的关键词
        for file_info in staged_files:
            diff_output, _ = run_command(f"git diff --cached --unified=0 {file_info['file']}")
            if any(keyword in diff_output.lower() for keyword in ['fix', 'bug', 'error', 'issue', 'resolve', 'correct']):
                return 'fix'

        # 默认为功能新增
        return 'feat'


def suggest_commit_scope(staged_files: List[Dict]) -> str:
    """建议提交的作用域"""
    # 根据文件路径建议作用域
    paths = [Path(f['file']).parts for f in staged_files]

    # 常见的路径模式
    scopes_by_path = {
        ('src', 'components'): 'components',
        ('src', 'pages'): 'pages',
        ('src', 'utils'): 'utils',
        ('src', 'services'): 'services',
        ('src', 'assets'): 'assets',
        ('src', 'styles'): 'styles',
        ('src', 'api'): 'api',
        ('tests',): 'test',
        ('docs',): 'docs',
        ('scripts',): 'build',
        ('config',): 'config',
    }

    # 检查路径匹配
    for path_parts in paths:
        for path_prefix, scope in scopes_by_path.items():
            if len(path_parts) >= len(path_prefix) and path_parts[:len(path_prefix)] == path_prefix:
                return scope

    # 如果没有明确匹配，使用第一个路径的第一个部分作为作用域
    if paths:
        first_part = paths[0][0] if paths[0] else 'misc'
        # 过滤掉常见的非作用域目录
        if first_part not in ['.', '..']:
            return first_part

    return 'misc'


def generate_commit_message(staged_files: List[Dict]) -> str:
    """生成提交消息"""
    if not staged_files:
        return "初始提交"

    # 分析更改类型
    change_type = classify_change_type(staged_files)

    # 建议作用域
    scope = suggest_commit_scope(staged_files)

    # 生成描述
    descriptions = []

    # 统计更改类型
    additions = 0
    modifications = 0
    deletions = 0

    for file_info in staged_files:
        status = file_info['status']
        if 'A' in status:  # Added
            additions += 1
        elif 'D' in status:  # Deleted
            deletions += 1
        else:  # Modified
            modifications += 1

    # 根据更改内容生成描述
    if additions > 0 and modifications == 0 and deletions == 0:
        if additions == 1:
            descriptions.append(f"添加 {Path(staged_files[0]['file']).name}")
        else:
            descriptions.append(f"添加 {additions} 个文件")
    elif deletions > 0 and additions == 0 and modifications == 0:
        if deletions == 1:
            descriptions.append(f"删除 {Path(staged_files[0]['file']).name}")
        else:
            descriptions.append(f"删除 {deletions} 个文件")
    elif modifications > 0:
        if modifications == 1:
            descriptions.append(f"更新 {Path(staged_files[0]['file']).name}")
        else:
            descriptions.append(f"更新 {modifications} 个文件")
    else:
        descriptions.append("代码整理")

    # 组合提交消息
    if scope:
        return f"{change_type}({scope}): {descriptions[0]}"
    else:
        return f"{change_type}: {descriptions[0]}"


def get_diff_statistics() -> Dict:
    """获取差异统计信息"""
    numstat_output, _ = run_command("git diff --cached --numstat")

    added = 0
    deleted = 0

    for line in numstat_output.split('\n'):
        if line.strip():
            parts = line.split('\t')
            if len(parts) >= 2:
                try:
                    added += int(parts[0]) if parts[0] != '-' else 0
                    deleted += int(parts[1]) if parts[1] != '-' else 0
                except ValueError:
                    continue

    return {'added': added, 'deleted': deleted}


def main():
    """主函数"""
    print("🔍 正在分析 Git 更改...")

    if not is_git_repo():
        print("❌ 错误: 当前目录不是一个 Git 仓库")
        sys.exit(1)

    git_status = get_git_status()

    print("\n📋 Git 工作区状态:")
    print("="*50)

    if git_status['staged']:
        print("✅ 已暂存文件:")
        for file_info in git_status['staged']:
            file_path = file_info['file']
            status = file_info['status']

            # 判断文件类型
            file_type = analyze_file_type(file_path)

            # 根据状态显示符号
            if 'A' in status:
                print(f"  + {file_path} ({file_type})")
            elif 'D' in status:
                print(f"  - {file_path} ({file_type})")
            else:
                print(f"  ~ {file_path} ({file_type})")
    else:
        print("  没有暂存的更改")

    if git_status['unstaged']:
        print("\n📝 未暂存文件:")
        for file_info in git_status['unstaged']:
            print(f"  ⚠️  {file_info['file']} ({analyze_file_type(file_info['file'])})")

    if git_status['untracked']:
        print("\n📄 未跟踪文件:")
        for file_path in git_status['untracked']:
            print(f"  ? {file_path} ({analyze_file_type(file_path)})")

    # 显示统计信息
    stats = get_diff_statistics()
    print(f"\n📊 更改进度统计:")
    print(f"  新增: {stats['added']} 行")
    print(f"  删除: {stats['deleted']} 行")

    # 生成提交消息建议
    if git_status['staged']:
        print(f"\n✨ 建议的提交信息:")
        print("-"*50)

        suggested_msg = generate_commit_message(git_status['staged'])
        print(f"  {suggested_msg}")

        print(f"\n📋 详细更改列表:")
        for file_info in git_status['staged']:
            print(f"  • {file_info['file']}")

        # 询问用户是否使用建议的提交消息
        print(f"\n❓ 是否使用上述提交信息进行提交? [y/N]: ", end='')
        response = input().strip().lower()

        if response in ['y', 'yes']:
            result, success = run_command(f'git commit -m "{suggested_msg}"')
            if success:
                print(f"✅ 成功提交更改")
                print(f"📝 提交信息: {suggested_msg}")
            else:
                print(f"❌ 提交失败: {result}")
        else:
            print(f"\n🖊️  请输入自定义提交信息 (直接回车取消):")
            custom_msg = input().strip()

            if custom_msg:
                result, success = run_command(f'git commit -m "{custom_msg}"')
                if success:
                    print(f"✅ 成功提交更改")
                    print(f"📝 提交信息: {custom_msg}")
                else:
                    print(f"❌ 提交失败: {result}")
            else:
                print("ℹ️  提交已取消")
    else:
        print(f"\n💡 提示: 没有暂存的更改可以提交。请先使用 'git add' 添加更改。")


if __name__ == "__main__":
    main()