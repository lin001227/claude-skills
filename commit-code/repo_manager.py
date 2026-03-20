#!/usr/bin/env python3
"""
commit-code 技能仓库初始化和推送模块
用于检测和处理仓库初始化及远程推送
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional


def run_command(cmd: str, cwd: Optional[str] = None) -> Tuple[str, bool]:
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


def has_remote_origin() -> bool:
    """检查是否有远程origin"""
    _, success = run_command("git remote get-url origin")
    return success


def get_current_branch() -> str:
    """获取当前分支名称"""
    output, success = run_command("git branch --show-current")
    if success:
        return output if output else "main"  # 如果没有分支则返回main
    else:
        return "main"  # 默认分支


def initialize_git_repo() -> bool:
    """初始化Git仓库"""
    print("📦 正在初始化Git仓库...")

    # 初始化仓库
    _, init_success = run_command("git init")
    if not init_success:
        print("❌ 无法初始化Git仓库")
        return False

    # 检查是否存在 .gitignore 文件，如果没有则创建一个基本的
    gitignore_path = Path(".gitignore")
    if not gitignore_path.exists():
        basic_gitignore = """# Dependencies
node_modules/
__pycache__/
*.egg-info/
.venv/
venv/

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Logs
logs/
*.log

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# IDE specific
.vscode/
.idea/
*.swp
*.swo
*~

# Python
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg
"""
        with open(gitignore_path, 'w', encoding='utf-8') as f:
            f.write(basic_gitignore)
        print("📄 创建了基本的 .gitignore 文件")

    # 添加所有文件
    print("➕ 添加所有文件到暂存区...")
    _, add_success = run_command("git add .")
    if not add_success:
        print("❌ 无法添加文件到暂存区")
        return False

    print("✅ Git仓库初始化完成")
    return True


def undo_git_init() -> bool:
    """撤销Git仓库初始化"""
    print("🔄 正在撤销Git仓库初始化...")

    if not is_git_repo():
        print("ℹ️  当前目录不是Git仓库，无需撤销")
        return True

    # 检查是否有未提交的更改
    status_output, _ = run_command("git status --porcelain")
    if status_output.strip():
        print("⚠️  仓库中有未提交的更改，撤销初始化将丢失这些更改")
        response = input("是否继续撤销初始化？[y/N]: ").strip().lower()
        if response not in ['y', 'yes']:
            print("❌ 操作已取消")
            return False

    # 删除 .git 目录
    git_dir = Path(".git")
    if git_dir.exists():
        import shutil
        try:
            shutil.rmtree(git_dir)
            print("✅ 已删除 .git 目录，Git仓库已撤销初始化")
            return True
        except Exception as e:
            print(f"❌ 删除 .git 目录失败: {str(e)}")
            return False
    else:
        print("ℹ️  未找到 .git 目录")
        return False


def delete_git_repo() -> bool:
    """删除整个Git仓库（包括所有文件）"""
    print("⚠️  警告：此操作将删除整个仓库目录及其所有内容！")

    repo_name = Path.cwd().name
    print(f"📁 当前仓库目录: {repo_name}")

    response = input(f"是否确认删除整个 '{repo_name}' 目录？[y/N]: ").strip().lower()
    if response not in ['y', 'yes']:
        print("❌ 操作已取消")
        return False

    # 获取父目录
    parent_dir = Path.cwd().parent

    try:
        import shutil
        current_dir = Path.cwd()
        shutil.rmtree(current_dir)
        print(f"✅ 仓库 '{repo_name}' 已被完全删除")
        print(f"ℹ️  当前工作目录已切换到上级目录: {parent_dir}")
        os.chdir(parent_dir)
        return True
    except Exception as e:
        print(f"❌ 删除仓库失败: {str(e)}")
        return False


def cleanup_local_git_history() -> bool:
    """清理本地Git历史记录（保留远程同步状态）"""
    print("🧹 正在清理本地Git历史记录...")

    if not is_git_repo():
        print("❌ 当前目录不是Git仓库")
        return False

    # 检查是否有远程仓库
    has_remote = has_remote_origin()
    if has_remote:
        print("ℹ️  检测到远程仓库连接")

    # 保留远程配置的情况下重置仓库
    try:
        # 保存远程配置
        if has_remote:
            origin_url, _ = run_command("git remote get-url origin")

        # 删除 .git 目录
        git_dir = Path(".git")
        if git_dir.exists():
            import shutil
            shutil.rmtree(git_dir)

        # 重新初始化仓库
        _, init_success = run_command("git init")
        if not init_success:
            print("❌ 重新初始化仓库失败")
            return False

        # 恢复远程配置
        if has_remote and origin_url:
            run_command(f"git remote add origin {origin_url}")
            print(f"✅ 已恢复远程仓库连接: {origin_url}")

        print("✅ 本地Git历史记录已清理")
        return True
    except Exception as e:
        print(f"❌ 清理本地Git历史记录失败: {str(e)}")
        return False


def setup_remote_repository() -> bool:
    """设置远程仓库"""
    print("\n📡 设置远程仓库...")

    # 检查是否已经有远程仓库
    if has_remote_origin():
        print("✅ 已存在远程仓库连接")
        return True

    print("💡 未检测到远程仓库，需要设置远程仓库")

    # 询问用户是否要创建新的仓库
    response = input("是否要设置远程仓库地址？[Y/n]: ").strip().lower()
    if response in ['', 'y', 'yes']:
        print("\n请输入远程仓库地址 (例如 GitHub/GitLab 等):")
        remote_url = input("Remote URL: ").strip()

        if remote_url:
            print(f"🔗 连接到远程仓库: {remote_url}")
            _, success = run_command(f"git remote add origin {remote_url}")

            if success:
                print("✅ 远程仓库连接成功")
                return True
            else:
                print("❌ 远程仓库连接失败")
                return False
        else:
            print("⚠️  未提供远程仓库地址，将继续本地提交")
            return True
    else:
        print("⚠️  用户选择跳过远程仓库设置，将继续本地提交")
        return True


def push_to_remote(branch_name: str) -> bool:
    """推送更改到远程仓库"""
    print(f"\n📤 推送更改到远程仓库...")

    if not has_remote_origin():
        print("⚠️  未设置远程仓库，仅进行本地提交")
        return True

    # 获取当前分支
    current_branch = get_current_branch()

    # 第一次推送，需要设置上游分支
    print(f"🔄 推送 {current_branch} 分支到远程仓库...")
    stdout, success = run_command(f"git push -u origin {current_branch}")

    if success:
        print("✅ 推送成功！")
        return True
    else:
        print(f"❌ 推送失败: {stdout}")
        return False


def check_uncommitted_changes() -> bool:
    """检查是否有未提交的更改"""
    output, success = run_command("git status --porcelain")

    if success and output.strip():
        print("📝 检测到未暂存的更改，建议先添加文件：")
        print("   git add .  # 添加所有更改")
        print("   或 git add <specific-file>  # 添加特定文件")
        return True
    else:
        return False


def check_unpushed_commits() -> Tuple[int, bool]:
    """检查是否有未推送的提交"""
    output, success = run_command("git rev-list HEAD --not --remotes")

    if success:
        commits = [line for line in output.split('\n') if line.strip()]
        return len(commits), True
    else:
        return 0, False


def get_repo_info() -> Dict:
    """获取仓库信息"""
    info = {
        'is_git_repo': is_git_repo(),
        'has_remote': has_remote_origin(),
        'current_branch': get_current_branch(),
        'has_uncommitted_changes': check_uncommitted_changes(),
    }

    # 获取未推送的提交数
    unpushed_count, unpushed_success = check_unpushed_commits()
    info['unpushed_commits'] = unpushed_count if unpushed_success else 0

    return info


def main():
    """主函数，用于测试仓库初始化和推送功能"""
    print("🔧 Git仓库状态检查工具")

    # 获取当前仓库信息
    repo_info = get_repo_info()

    print(f"\n📋 当前仓库状态:")
    print(f"  Git仓库: {'✅ 是' if repo_info['is_git_repo'] else '❌ 否'}")
    print(f"  远程连接: {'✅ 是' if repo_info['has_remote'] else '❌ 否'}")
    print(f"  当前分支: {repo_info['current_branch']}")
    print(f"  未提交更改: {'✅ 有' if repo_info['has_uncommitted_changes'] else '❌ 无'}")
    print(f"  未推送提交: {repo_info['unpushed_commits']} 个")

    # 如果不是Git仓库，询问是否初始化
    if not repo_info['is_git_repo']:
        response = input("\n💡 检测到当前目录不是Git仓库，是否初始化？[Y/n]: ").strip().lower()
        if response in ['', 'y', 'yes']:
            if initialize_git_repo():
                print("✅ 仓库初始化成功")
            else:
                print("❌ 仓库初始化失败")
                return False
        else:
            print("❌ 操作已取消")
            return False

    # 设置远程仓库
    if not setup_remote_repository():
        print("❌ 远程仓库设置失败")
        return False

    # 检查是否有未提交的更改
    if repo_info['has_uncommitted_changes']:
        response = input("\n💡 有未提交的更改，是否添加并提交所有文件？[Y/n]: ").strip().lower()
        if response in ['', 'y', 'yes']:
            print("➕ 添加所有更改...")
            _, add_success = run_command("git add .")
            if add_success:
                print("✅ 文件已添加到暂存区")

                # 然后执行提交
                print("💡 现在你可以使用 /commit-code 命令来生成提交信息并提交更改")
            else:
                print("❌ 添加文件失败")
                return False

    # 检查未推送的提交并推送
    repo_info_after = get_repo_info()
    if repo_info_after['unpushed_commits'] > 0 or repo_info['has_uncommitted_changes']:
        response = input(f"\n💡 检测到 {repo_info_after['unpushed_commits']} 个未推送的提交，是否推送？[Y/n]: ").strip().lower()
        if response in ['', 'y', 'yes']:
            if push_to_remote(repo_info_after['current_branch']):
                print("✅ 推送完成")
            else:
                print("❌ 推送失败")
                return False

    print("\n🎉 仓库状态检查完成")
    return True


if __name__ == "__main__":
    main()