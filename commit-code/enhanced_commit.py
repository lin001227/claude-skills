#!/usr/bin/env python3
"""
commit-code 技能增强版主脚本
整合所有功能的智能提交助手
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Tuple
from file_type_detector import FileTypeDetector, aggregate_analysis_results
from security_checker import SecurityChecker, validate_commit_message
from repo_manager import get_repo_info, initialize_git_repo, setup_remote_repository, push_to_remote


def run_command(cmd: str, cwd: str = None) -> Tuple[str, bool]:
    """运行shell命令并返回输出和是否成功"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=False,
            cwd=cwd
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


def analyze_file_changes(staged_files: List[Dict]) -> Dict:
    """分析文件更改"""
    detector = FileTypeDetector()

    analyses = []
    for file_info in staged_files:
        analysis = detector.analyze_file_changes(file_info['file'], file_info['status'])
        analyses.append(analysis)

    return aggregate_analysis_results(analyses)


def classify_change_type(analysis_summary: Dict) -> str:
    """根据分析结果分类更改类型"""
    by_purpose = analysis_summary['summary']['by_purpose']
    by_language = analysis_summary['summary']['by_language']

    # 检查是否有测试文件
    if by_purpose.get('test', 0) > 0 and sum(by_purpose.values()) == by_purpose.get('test', 0):
        return '测试'  # 纯测试提交

    # 检查是否有文档文件
    if by_purpose.get('documentation', 0) > 0 and by_purpose.get('code', 0) == 0:
        return '文档'  # 纯文档提交

    # 检查CSS/样式文件
    if any(lang in ['css', 'scss', 'sass', 'less'] for lang in by_language.keys()):
        if by_purpose.get('code', 0) == 0:  # 没有代码文件，只有样式
            return '样式'

    # 检查是否有bug修复关键词
    staged_files_list = [a['filepath'] for a in analysis_summary['details']]
    for file_path in staged_files_list:
        diff_output, _ = run_command(f"git diff --cached --unified=0 {file_path}")
        if any(keyword in diff_output.lower() for keyword in ['fix', 'bug', 'error', 'issue', 'resolve', 'correct', 'patch']):
            return '修复'

    # 检查是否有新功能关键词
    for file_path in staged_files_list:
        if any(new_word in file_path.lower() for new_word in ['feature', 'feat', 'new']):
            return '功能'

    # 默认根据数量最多的文件类型判断
    code_related = sum(by_purpose.get(t, 0) for t in ['code', 'component', 'page', 'view', 'utility', 'service', 'model', 'api', 'controller', 'route'])
    if code_related > 0:
        return '功能'  # 新功能或更新

    return '杂务'  # 杂项维护


def suggest_commit_scope(analysis_summary: Dict) -> str:
    """建议提交的作用域"""
    # 检查文件路径以建议作用域
    for detail in analysis_summary['details']:
        path_parts = Path(detail['filepath']).parts

        # 常见的作用域路径
        if path_parts[0] in ['src', 'app', 'lib'] and len(path_parts) > 1:
            if path_parts[1] in ['components', 'widgets', 'elements']:
                return '组件'
            elif path_parts[1] in ['pages', 'screens', 'views']:
                return '页面'
            elif path_parts[1] in ['utils', 'helpers', 'common', 'shared']:
                return '工具'
            elif path_parts[1] in ['services', 'api', 'clients']:
                return '服务'
            elif path_parts[1] in ['styles', 'themes', 'css', 'sass', 'scss']:
                return '样式'
            elif path_parts[1] in ['assets', 'resources', 'static']:
                return '资源'
            elif path_parts[1] in ['tests', 'specs', 'e2e']:
                return '测试'
            elif path_parts[1] in ['docs', 'documentation']:
                return '文档'

    # 如果没找到特定作用域，根据主要用途决定
    by_purpose = analysis_summary['summary']['by_purpose']
    if 'test' in by_purpose:
        return '测试'
    elif 'documentation' in by_purpose:
        return '文档'
    elif 'config' in by_purpose:
        return '配置'

    return '通用'


def generate_commit_message_from_analysis(analysis_summary: Dict) -> str:
    """根据分析结果生成提交消息"""
    if not analysis_summary['details']:
        return "初始化项目"

    # 分析更改类型
    change_type = classify_change_type(analysis_summary)

    # 建议作用域
    scope = suggest_commit_scope(analysis_summary)

    # 生成描述
    total_files = analysis_summary['summary']['total_files']
    by_purpose = analysis_summary['summary']['by_purpose']
    by_change_type = analysis_summary['summary']['by_change_type']

    # 统计各类更改
    added_count = by_change_type.get('A', 0)
    modified_count = by_change_type.get('M', 0)
    deleted_count = by_change_type.get('D', 0)

    # 根据更改内容生成描述
    if added_count > 0 and modified_count == 0 and deleted_count == 0:
        # 纯新增
        if 'test' in by_purpose and total_files == by_purpose['test']:
            desc = "添加测试"
        elif 'documentation' in by_purpose and by_purpose['documentation'] >= total_files / 2:
            desc = "添加文档"
        else:
            desc = "添加新功能"
    elif deleted_count > 0 and added_count == 0 and modified_count == 0:
        # 纯删除
        desc = "删除文件"
    else:
        # 混合更改或纯修改
        if change_type == '修复':
            desc = "修复问题"
        elif change_type == '文档':
            desc = "更新文档"
        elif change_type == '样式':
            desc = "调整样式"
        elif change_type == '测试':
            desc = "更新测试"
        else:
            desc = "更新代码"

    # 组合提交消息
    if scope and scope != '通用':
        return f"{change_type}({scope}): {desc}"
    else:
        return f"{change_type}: {desc}"


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
    print("commit-code 技能启动")

    # 检查仓库状态并初始化
    repo_info = get_repo_info()

    print("正在分析仓库和 Git 更改...")

    # 如果不是Git仓库，询问是否初始化
    if not repo_info['is_git_repo']:
        print(" 检测到当前目录不是Git仓库")
        response = input("是否初始化一个新的Git仓库？[Y/n]: ").strip().lower()
        if response in ['', 'y', 'yes']:
            if initialize_git_repo():
                print(" 仓库初始化成功")
                # 更新仓库信息
                repo_info = get_repo_info()
                # 重新检查是否成功初始化
                if not repo_info['is_git_repo']:
                    print(" 仓库初始化失败，无法继续提交")
                    sys.exit(1)
            else:
                print(" 仓库初始化失败，无法继续提交")
                sys.exit(1)
        else:
            print(" 操作已取消，提交需要Git仓库")
            sys.exit(1)

    git_status = get_git_status()
    print(f"\n Git 工作区状态:")
    print("="*60)

    if git_status['staged']:
        print(" 已暂存文件:")

        # 使用文件类型检测器分析文件
        file_analyses = analyze_file_changes(git_status['staged'])

        for file_info in git_status['staged']:
            file_path = file_info['file']
            status = file_info['status']

            # 获取文件分析结果
            analysis = None
            for a in file_analyses['details']:
                if a['filepath'] == file_path:
                    analysis = a
                    break

            if analysis:
                file_type = analysis['metadata']['purpose']
                lang = analysis['metadata']['language']
            else:
                file_type = "unknown"
                lang = "unknown"

            # 根据状态显示符号
            status_icon = {
                'A': '+',   # Added
                'M': '~',   # Modified
                'D': '-',   # Deleted
                'R': '→',   # Renamed
                'C': '++',  # Copied
            }.get(status.replace(' ', '')[0] if status.replace(' ', '') else 'M', '~')

            print(f"  {status_icon} {file_path} ({lang}/{file_type})")
    else:
        print("  没有暂存的更改")
        print(" 提示: 使用 'git add' 命令暂存更改后再提交")

    if git_status['unstaged']:
        print(f"\n 未暂存文件: {len(git_status['unstaged'])} 个")
        for i, file_info in enumerate(git_status['unstaged'][:5]):  # 只显示前5个
            print(f"  ️  {file_info['file']}")
        if len(git_status['unstaged']) > 5:
            print(f"  ... 还有 {len(git_status['unstaged']) - 5} 个文件")

    if git_status['untracked']:
        print(f"\n 未跟踪文件: {len(git_status['untracked'])} 个")
        for i, file_path in enumerate(git_status['untracked'][:5]):  # 只显示前5个
            print(f"  ? {file_path}")
        if len(git_status['untracked']) > 5:
            print(f"  ... 还有 {len(git_status['untracked']) - 5} 个文件")

    if not git_status['staged']:
        print(f"\n 没有暂存的更改可以提交。")
        print(" 请先使用 'git add .' 或 'git add <具体文件>' 暂存更改。")

        # 询问是否添加所有更改
        response = input("是否添加所有文件到暂存区？[Y/n]: ").strip().lower()
        if response in ['', 'y', 'yes']:
            print(" 添加所有文件到暂存区...")
            _, add_success = run_command("git add .")
            if add_success:
                print(" 文件已添加到暂存区")
                # 重新获取状态
                git_status = get_git_status()

                # 检查是否仍有无文件可提交
                if not git_status['staged']:
                    print(" 仍然没有可提交的文件")
                    return
            else:
                print(" 添加文件失败")
                return
        else:
            print(" 提交已取消")
            return

    # 显示统计信息
    stats = get_diff_statistics()
    print(f"\n 更改进度统计:")
    print(f"  新增: {stats['added']:>6} 行")
    print(f"  删除: {stats['deleted']:>6 } 行")

    # 显示文件类型分析
    print(f"\n 文件类型分析:")
    for purpose, count in file_analyses['summary']['by_purpose'].items():
        print(f"  {purpose:>12}: {count} 个文件")

    # 显示建议
    print(f"\n 分析建议:")
    for rec in file_analyses['recommendations']:
        print(f"  • {rec}")

    # 执行安全检查
    print(f"\n️  安全扫描:")
    print("-" * 30)
    security_checker = SecurityChecker()
    risk_summary = security_checker.check_git_staged_for_risks()
    security_report = security_checker.generate_security_report(risk_summary)
    print(security_report)

    if risk_summary['total_risks'] > 0:
        print(f"\n️  检测到 {risk_summary['total_risks']} 个安全风险，建议解决后再提交！")
        response = input(" 是否继续提交？这可能会暴露敏感信息。[y/N]: ").strip().lower()
        if response not in ['y', 'yes']:
            print(" 提交已取消。请先解决安全风险。")
            return

    # 生成提交消息建议
    print(f"\n 建议的提交信息:")
    print("-" * 50)

    suggested_msg = generate_commit_message_from_analysis(file_analyses)
    print(f"  {suggested_msg}")

    # 验证提交消息
    validation_errors = validate_commit_message(suggested_msg)
    if validation_errors:
        print(f"\n 提交消息验证:")
        for error in validation_errors:
            print(f"  ️  {error}")

    print(f"\n 详细更改列表:")
    for i, detail in enumerate(file_analyses['details'][:10]):  # 只显示前10个
        print(f"  {i+1:2}. {detail['filepath']}")

    if len(file_analyses['details']) > 10:
        print(f"     ... 还有 {len(file_analyses['details']) - 10} 个文件")

    # 询问用户是否使用建议的提交消息
    print(f"\n 选择操作:")
    print("  1. 使用建议的消息提交 (默认)")
    print("  2. 编辑建议的消息")
    print("  3. 输入自定义消息")
    print("  4. 取消提交")

    choice = input("请选择 (1-4, 默认1): ").strip() or "1"

    if choice == "1":
        # 使用建议的消息
        commit_msg = suggested_msg
    elif choice == "2":
        # 编辑建议的消息
        edit_msg = input(f"编辑消息 (当前: '{suggested_msg}'): ").strip()
        commit_msg = edit_msg if edit_msg else suggested_msg
    elif choice == "3":
        # 自定义消息
        custom_msg = input("输入自定义提交消息: ").strip()
        if not custom_msg:
            print(" 提交已取消")
            return
        commit_msg = custom_msg

        # 验证自定义消息
        validation_errors = validate_commit_message(commit_msg)
        if validation_errors:
            print(f"\n 自定义消息验证:")
            for error in validation_errors:
                print(f"  ️  {error}")

            confirm = input(" 消息存在问题，仍要使用此消息提交吗？[y/N]: ").strip().lower()
            if confirm not in ['y', 'yes']:
                print(" 提交已取消")
                return
    else:
        # 取消提交
        print(" 提交已取消")
        return

    # 执行提交
    print(f"\n 正在提交更改...")
    result, success = run_command(f'git commit -m "{commit_msg}"')

    if success:
        print(f" 成功提交更改!")
        print(f" 提交信息: {commit_msg}")

        # 显示提交哈希
        hash_result, hash_success = run_command("git rev-parse --short HEAD")
        if hash_success:
            print(f" 提交哈希: {hash_result}")

            # 检查是否需要推送
            unpushed_count, _ = check_unpushed_commits()
            if unpushed_count > 0:
                print(f" 检测到 {unpushed_count} 个未推送的提交")

                # 设置远程仓库（如果还没有的话）
                if not repo_info['has_remote']:
                    setup_remote_repository()

                # 询问是否推送
                response = input("是否将更改推送到远程仓库？[Y/n]: ").strip().lower()
                if response in ['', 'y', 'yes']:
                    current_branch = get_current_branch()
                    push_success = push_to_remote(current_branch)
                    if push_success:
                        print(" 推送成功！")
                    else:
                        print("️  推送失败，请检查网络连接和远程仓库设置")
        else:
            print("️  无法获取提交哈希")
    else:
        print(f" 提交失败: {result}")


if __name__ == "__main__":
    main()