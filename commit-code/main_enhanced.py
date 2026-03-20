#!/usr/bin/env python3
"""
commit-code 技能主入口点（增强版）
支持提交、初始化仓库、撤销初始化等多种操作
"""

import os
import sys
from pathlib import Path
import importlib.util

def load_module_from_file(module_name, file_path):
    """从文件加载模块"""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    """主入口函数"""
    # 获取技能目录
    skill_dir = Path(__file__).parent

    print("🚀 commit-code 技能启动")
    print("\n选择操作:")
    print("1. 提交代码（智能分析并生成提交信息）")
    print("2. 初始化 Git 仓库")
    print("3. 撤销 Git 仓库初始化")
    print("4. 删除整个仓库")
    print("5. 清理本地 Git 历史记录")
    print("6. 检查仓库状态")
    print("7. 设置远程仓库")
    print("8. 推送提交到远程仓库")

    choice = input("\n请选择操作 (1-8, 默认1): ").strip() or "1"

    if choice == "1":
        # 运行增强版提交功能
        enhanced_script = skill_dir / "enhanced_commit.py"
        if enhanced_script.exists():
            commit_module = load_module_from_file("enhanced_commit", enhanced_script)
            commit_module.main()
        else:
            print("❌ 错误: 未找到提交脚本")
            sys.exit(1)

    elif choice == "2":
        # 初始化仓库
        repo_manager = load_module_from_file("repo_manager", skill_dir / "repo_manager.py")
        repo_manager.initialize_git_repo()

    elif choice == "3":
        # 撤销仓库初始化
        repo_manager = load_module_from_file("repo_manager", skill_dir / "repo_manager.py")
        repo_manager.undo_git_init()

    elif choice == "4":
        # 删除整个仓库
        repo_manager = load_module_from_file("repo_manager", skill_dir / "repo_manager.py")
        repo_manager.delete_git_repo()

    elif choice == "5":
        # 清理本地历史记录
        repo_manager = load_module_from_file("repo_manager", skill_dir / "repo_manager.py")
        repo_manager.cleanup_local_git_history()

    elif choice == "6":
        # 检查仓库状态
        repo_manager = load_module_from_file("repo_manager", skill_dir / "repo_manager.py")
        repo_info = repo_manager.get_repo_info()
        print(f"\n📋 仓库状态:")
        print(f"  Git仓库: {'✅ 是' if repo_info['is_git_repo'] else '❌ 否'}")
        print(f"  远程连接: {'✅ 是' if repo_info['has_remote'] else '❌ 否'}")
        print(f"  当前分支: {repo_info['current_branch']}")
        print(f"  未提交更改: {'✅ 有' if repo_info['has_uncommitted_changes'] else '❌ 无'}")
        print(f"  未推送提交: {repo_info['unpushed_commits']} 个")

    elif choice == "7":
        # 设置远程仓库
        repo_manager = load_module_from_file("repo_manager", skill_dir / "repo_manager.py")
        repo_manager.setup_remote_repository()

    elif choice == "8":
        # 推送提交到远程仓库
        repo_manager = load_module_from_file("repo_manager", skill_dir / "repo_manager.py")
        current_branch = repo_manager.get_current_branch()
        repo_manager.push_to_remote(current_branch)

    else:
        print("❌ 无效选择")
        sys.exit(1)

if __name__ == "__main__":
    main()