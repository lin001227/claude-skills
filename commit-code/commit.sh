#!/bin/bash
# commit-code 技能主脚本
# 用于分析 Git 更改并生成提交信息

# 检查是否在 Git 仓库中
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "错误: 当前目录不是一个 Git 仓库"
    exit 1
fi

echo "正在分析 Git 更改..."

# 显示 Git 状态概览
echo "=== Git 工作区状态 ==="
git status --short

echo ""
echo "=== 详细更改摘要 ==="

# 获取暂存区的更改
staged_files=$(git diff --cached --name-only 2>/dev/null)
unstaged_files=$(git diff --name-only 2>/dev/null)
new_files=$(git diff --cached --name-status 2>/dev/null | grep '^A' | cut -f2-)

if [ -n "$staged_files" ]; then
    echo "已暂存的文件:"
    for file in $staged_files; do
        # 检查文件是否是新文件
        if echo "$new_files" | grep -q "^${file}$"; then
            echo "  A+ $file (新增文件)"
        else
            echo "  M  $file (已修改)"
        fi
    done
else
    echo "无已暂存文件"
fi

if [ -n "$unstaged_files" ]; then
    echo ""
    echo "未暂存的文件:"
    for file in $unstaged_files; do
        echo "  ?? $file (未暂存)"
    done
fi

# 获取暂存的更改统计
added_lines=$(git diff --cached --numstat 2>/dev/null | awk '{sum += $1} END {print sum+0}')
deleted_lines=$(git diff --cached --numstat 2>/dev/null | awk '{sum += $2} END {print sum+0}')

echo ""
echo "=== 更改进度统计 ==="
echo "新增: $added_lines 行"
echo "删除: $deleted_lines 行"

# 基于更改生成提交信息建议
suggest_commit_message() {
    local commit_type="chore"
    local commit_scope=""
    local commit_desc=""

    # 分析更改的文件以确定提交类型
    local files="$1"
    if [ -z "$files" ]; then
        echo "没有待提交的文件"
        return
    fi

    # 确定提交类型
    for file in $files; do
        if [[ $file == *.md ]] || [[ $file == *.txt ]] || [[ $file == *README* ]]; then
            commit_type="docs"
            break
        elif [[ $file == *.css ]] || [[ $file == *.scss ]] || [[ $file == *.sass ]]; then
            commit_type="style"
            break
        elif [[ $file == *test* ]] || [[ $file == *.spec.* ]] || [[ $file == *.test.* ]]; then
            commit_type="test"
            break
        elif [[ $file == src/* ]] || [[ $file == app/* ]]; then
            # 如果文件中有bug相关关键词，则标记为fix
            if git diff --cached --unified=0 "$file" 2>/dev/null | grep -q -i -E "(fix|bug|error|issue|resolve|correct)"; then
                commit_type="fix"
                break
            else
                commit_type="feat"
            fi
        fi
    done

    # 确定作用域（基于路径）
    for file in $files; do
        if [[ $file == src/components/* ]]; then
            commit_scope="components"
            break
        elif [[ $file == src/utils/* ]]; then
            commit_scope="utils"
            break
        elif [[ $file == src/services/* ]]; then
            commit_scope="services"
            break
        elif [[ $file == src/pages/* ]]; then
            commit_scope="pages"
            break
        elif [[ $file == src/styles/* ]]; then
            commit_scope="styles"
            break
        elif [[ $file == docs/* ]]; then
            commit_scope="docs"
            break
        fi
    done

    # 确定描述
    if [ -n "$new_files" ]; then
        commit_desc="添加新文件"
    else
        case $commit_type in
            feat)
                commit_desc="新增功能"
                ;;
            fix)
                commit_desc="修复问题"
                ;;
            docs)
                commit_desc="更新文档"
                ;;
            style)
                commit_desc="调整样式"
                ;;
            refactor)
                commit_desc="重构代码"
                ;;
            test)
                commit_desc="添加测试"
                ;;
            chore)
                commit_desc="日常维护"
                ;;
        esac
    fi

    # 构建提交信息
    if [ -n "$commit_scope" ]; then
        echo "${commit_type}(${commit_scope}): ${commit_desc}"
    else
        echo "${commit_type}: ${commit_desc}"
    fi
}

if [ -n "$staged_files" ]; then
    echo ""
    echo "=== 建议的提交信息 ==="
    suggested_msg=$(suggest_commit_message "$staged_files")
    echo "$suggested_msg"

    # 询问用户是否使用建议的提交信息
    echo ""
    echo "是否使用上述提交信息进行提交？(y/N): "
    read -r response
    if [[ $response =~ ^[Yy]$ ]]; then
        git commit -m "$suggested_msg"
        echo "已提交更改。"
    else
        echo "您可以手动输入提交信息："
        read -r manual_msg
        if [ -n "$manual_msg" ]; then
            git commit -m "$manual_msg"
            echo "已使用您的提交信息进行提交。"
        else
            echo "未进行提交。"
        fi
    fi
else
    echo ""
    echo "没有暂存的更改可以提交。请先使用 'git add' 添加更改。"
fi