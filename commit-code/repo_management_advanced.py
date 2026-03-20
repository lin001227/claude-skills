#!/usr/bin/env python3
"""
commit-code 技能仓库管理增强模块
用于处理仓库初始化、撤销初始化和删除仓库等功能
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


def get_repo_info() -> Dict:
    """获取仓库信息"""
    info = {
        'is_git_repo': is_git_repo(),
        'has_remote': has_remote_origin(),
        'current_branch': get_current_branch(),
    }

    # 获取未提交的更改数
    if info['is_git_repo']:
        output, success = run_command("git status --porcelain")
        if success:
            changes = [line for line in output.split('\n') if line.strip()]
            info['uncommitted_changes'] = len(changes)
        else:
            info['uncommitted_changes'] = 0
    else:
        info['uncommitted_changes'] = 0

    return info


def main():
    """主函数，用于测试仓库管理功能"""
    print("🔧 Git仓库管理工具")
    print("\n选择操作:")
    print("1. 检查仓库状态")
    print("2. 初始化仓库")
    print("3. 撤销仓库初始化")
    print("4. 清理本地历史记录")
    print("5. 删除整个仓库")
    print("6. 退出")

    while True:
        choice = input("\n请选择操作 (1-6): ").strip()

        if choice == "1":
            repo_info = get_repo_info()
            print(f"\n📋 仓库状态:")
            print(f"  Git仓库: {'✅ 是' if repo_info['is_git_repo'] else '❌ 否'}")
            print(f"  远程连接: {'✅ 是' if repo_info['has_remote'] else '❌ 否'}")
            print(f"  当前分支: {repo_info['current_branch']}")
            print(f"  未提交更改: {repo_info['uncommitted_changes']} 个")
        elif choice == "2":
            initialize_git_repo()
        elif choice == "3":
            undo_git_init()
        elif choice == "4":
            cleanup_local_git_history()
        elif choice == "5":
            delete_git_repo()
        elif choice == "6":
            print("👋 退出仓库管理工具")
            break
        else:
            print("❌ 无效选择，请重新输入")


if __name__ == "__main__":
    main()