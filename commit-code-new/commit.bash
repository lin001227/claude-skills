#!/bin/bash
# commit-code-new 主程序
# 一个基于纯Bash实现的智能Git提交助手

# 引入核心功能脚本
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CORE_SCRIPT="${SOURCE_DIR}/commit-core.bash"

if [[ -f "$CORE_SCRIPT" ]]; then
    source "$CORE_SCRIPT"
else
    echo "错误: 找不到核心脚本 $CORE_SCRIPT"
    exit 1
fi

# 检查是否提供了参数
if [ $# -eq 0 ]; then
    # 默认行为：执行提交流程
    perform_commit
else
    # 解析命令行参数
    case $1 in
        "create"|"new")
            create_branch "${2:-""}"
            ;;
        "switch"|"checkout")
            switch_branch "${2:-""}"
            ;;
        "list"|"ls")
            list_branches
            ;;
        "commit")
            perform_commit
            ;;
        *)
            echo "使用方法:"
            echo "  commit-code-new                    - 执行提交流程"
            echo "  commit-code-new create <branch>    - 创建新分支"
            echo "  commit-code-new switch <branch>    - 切换到分支"
            echo "  commit-code-new list              - 列出所有分支"
            ;;
    esac
fi