#!/bin/bash
# commit-core.bash - commit-code-new 核心功能实现

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 检查是否在 Git 仓库中
check_git_repo() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        echo -e "${RED}错误: 当前目录不是一个 Git 仓库${NC}"
        exit 1
    fi
}

# 创建新分支
create_branch() {
    local branch_name=$1

    if [ -z "$branch_name" ]; then
        echo -e "${RED}错误: 请提供分支名称${NC}"
        echo "用法: commit-code-new create <branch-name>"
        return 1
    fi

    # 检查分支命名规范
    check_branch_naming_convention "$branch_name"

    # 获取当前分支
    local current_branch=$(git branch --show-current)

    # 创建并切换到新分支
    echo -e "${BLUE}正在从 '$current_branch' 创建新分支 '$branch_name'...${NC}"
    if git checkout -b "$branch_name" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ 成功创建并切换到分支 '$branch_name'${NC}"
        echo -e "${CYAN}基于: $current_branch${NC}"
        echo -e "${YELLOW}提示: 您现在可以在新分支上进行开发工作${NC}"
    else
        echo -e "${RED}✗ 创建分支失败${NC}"
        return 1
    fi
}

# 切换分支
switch_branch() {
    local branch_name=$1

    if [ -z "$branch_name" ]; then
        echo -e "${RED}错误: 请提供分支名称${NC}"
        echo "用法: commit-code-new switch <branch-name>"
        return 1
    fi

    # 检查分支是否存在
    if git show-ref --verify --quiet "refs/heads/$branch_name"; then
        # 分支存在，直接切换
        local prev_branch=$(git branch --show-current)
        if git checkout "$branch_name" > /dev/null 2>&1; then
            echo -e "${GREEN}✓ 已切换到分支 '$branch_name'${NC}"
            echo -e "${CYAN}之前分支: $prev_branch${NC}"
            echo -e "${CYAN}当前分支: $branch_name${NC}"
        else
            echo -e "${RED}✗ 切换分支失败${NC}"
            return 1
        fi
    else
        echo -e "${RED}错误: 分支 '$branch_name' 不存在${NC}"
        echo -e "${YELLOW}可用的分支:${NC}"
        list_branches
        return 1
    fi
}

# 列出分支
list_branches() {
    echo -e "${BLUE}=== 本地分支 ===${NC}"
    git branch --format='%(if)%(HEAD)%(then)* %(else)  %(end)%(refname:short)' 2>/dev/null || echo "  无本地分支"

    echo -e "${BLUE}=== 远程分支 ===${NC}"
    git branch -r --format='%(refname:short)' 2>/dev/null | grep -v HEAD || echo "  无远程分支"
}

# 检查分支命名规范
check_branch_naming_convention() {
    local branch=$1

    # 常见的规范前缀
    if [[ $branch =~ ^(feature|feat|bugfix|fix|hotfix|release|docs|refactor|test)/ ]]; then
        echo -e "${GREEN}✓ 分支命名符合规范: $branch${NC}"
    else
        echo -e "${YELLOW}提示: 建议使用以下命名规范:${NC}"
        echo "  feature/功能描述  - 新功能开发"
        echo "  bugfix/问题描述  - 修复Bug"
        echo "  hotfix/问题描述  - 紧急修复"
        echo "  release/版本号   - 发布版本"
        echo "  docs/文档描述    - 文档更新"
        echo "  refactor/描述    - 代码重构"
        echo -e "${YELLOW}当前分支名: $branch${NC}"
    fi
}

# 执行提交操作
perform_commit() {
    check_git_repo

    echo -e "${BLUE}正在分析 Git 更改...${NC}"

    # 显示 Git 状态概览
    echo -e "${BLUE}=== Git 工作区状态 ===${NC}"
    git status --short

    echo ""
    echo -e "${BLUE}=== 详细更改摘要 ===${NC}"

    # 获取暂存区的更改
    local staged_files=$(git diff --cached --name-only 2>/dev/null)
    local unstaged_files=$(git diff --name-only 2>/dev/null)
    local new_files=$(git diff --cached --name-status 2>/dev/null | grep '^A' | cut -f2-)
    local deleted_files=$(git diff --cached --name-status 2>/dev/null | grep '^D' | cut -f2-)

    if [ -n "$staged_files" ]; then
        echo -e "${GREEN}已暂存的文件:${NC}"
        for file in $staged_files; do
            # 检查文件类型
            if echo "$new_files" | grep -q "^${file}$"; then
                echo "  A+ $file ${CYAN}(新增文件)${NC}"
            elif echo "$deleted_files" | grep -q "^${file}$"; then
                echo "  D  $file ${RED}(已删除)${NC}"
            else
                echo "  M  $file ${YELLOW}(已修改)${NC}"
            fi
        done
    else
        echo -e "${RED}无已暂存文件${NC}"
        echo -e "${YELLOW}提示: 使用 'git add .' 暂存所有更改，或 'git add <file>' 暂存特定文件${NC}"
        return 1
    fi

    if [ -n "$unstaged_files" ]; then
        echo ""
        echo -e "${YELLOW}未暂存的文件:${NC}"
        for file in $unstaged_files; do
            echo "  ?? $file (未暂存)"
        done
    fi

    # 获取暂存的更改统计
    local added_lines=$(git diff --cached --numstat 2>/dev/null | awk '{sum += $1} END {print sum+0}')
    local deleted_lines=$(git diff --cached --numstat 2>/dev/null | awk '{sum += $2} END {print sum+0}')

    echo ""
    echo -e "${BLUE}=== 更改进度统计 ===${NC}"
    echo -e "新增: ${GREEN}${added_lines}${NC} 行"
    echo -e "删除: ${RED}${deleted_lines}${NC} 行"

    # 生成提交信息
    suggest_commit_message "$staged_files"
}

# 基于更改生成提交信息建议
suggest_commit_message() {
    local files="$1"
    local commit_type="chore"
    local commit_scope=""
    local commit_desc=""
    local commit_body=""

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
            if git diff --cached --unified=0 "$file" 2>/dev/null | grep -qi -E "(fix|bug|error|issue|resolve|correct|patch)"; then
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
        elif [[ $file == src/hooks/* ]]; then
            commit_scope="hooks"
            break
        elif [[ $file == src/reducers/* ]]; then
            commit_scope="reducers"
            break
        elif [[ $file == src/actions/* ]]; then
            commit_scope="actions"
            break
        elif [[ $file == docs/* ]]; then
            commit_scope="docs"
            break
        elif [[ $file == scripts/* ]]; then
            commit_scope="scripts"
            break
        elif [[ $file == config/* ]]; then
            commit_scope="config"
            break
        fi
    done

    # 确定描述和正文
    local new_count=0
    local mod_count=0
    local del_count=0

    for file in $files; do
        if echo "$new_files" | grep -q "^${file}$"; then
            ((new_count++))
        elif echo "$deleted_files" | grep -q "^${file}$"; then
            ((del_count++))
        else
            ((mod_count++))
        fi
    done

    # 确定描述
    if [ $new_count -gt 0 ] && [ $mod_count -eq 0 ] && [ $del_count -eq 0 ]; then
        commit_desc="添加新文件"
    elif [ $del_count -gt 0 ] && [ $new_count -eq 0 ] && [ $mod_count -eq 0 ]; then
        commit_desc="删除文件"
    elif [ $mod_count -gt 0 ]; then
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

    # 构建提交信息主体
    commit_body=""
    if [ $new_count -gt 0 ]; then
        commit_body+="\n- 新增 $new_count 个文件"
    fi
    if [ $mod_count -gt 0 ]; then
        commit_body+="\n- 修改 $mod_count 个文件"
    fi
    if [ $del_count -gt 0 ]; then
        commit_body+="\n- 删除 $del_count 个文件"
    fi

    # 构建提交信息
    local suggested_msg
    if [ -n "$commit_scope" ]; then
        suggested_msg="${commit_type}(${commit_scope}): ${commit_desc}"
    else
        suggested_msg="${commit_type}: ${commit_desc}"
    fi

    echo ""
    echo -e "${BLUE}=== 建议的提交信息 ===${NC}"
    echo -e "${GREEN}$suggested_msg${NC}"

    if [ -n "$commit_body" ]; then
        echo -e "${YELLOW}$commit_body${NC}"
    fi

    # 询问用户是否使用建议的提交信息
    echo ""
    echo -e "${YELLOW}是否使用上述提交信息进行提交？(Y/n): ${NC}"
    read -r response
    if [[ $response =~ ^[Nn]$ ]] || [ -z "$response" ] && [ "$response" != "y" ] && [ "$response" != "Y" ]; then
        echo -e "${YELLOW}请输入您的提交信息 (留空则取消提交):${NC}"
        read -r manual_msg
        if [ -n "$manual_msg" ]; then
            git commit -m "$manual_msg"
            echo -e "${GREEN}已使用您的提交信息进行提交。${NC}"
        else
            echo -e "${YELLOW}未进行提交。${NC}"
            return 1
        fi
    else
        git commit -m "$suggested_msg"
        echo -e "${GREEN}已提交更改。${NC}"
    fi

    # 检查是否需要推送
    check_for_push
}

# 检查是否需要推送
check_for_push() {
    local current_branch=$(git branch --show-current)

    # 检查是否有远程仓库
    if git remote | grep -q origin; then
        # 获取本地和远程的提交数差异
        local ahead_count=$(git rev-list --count HEAD...origin/$current_branch 2>/dev/null | cut -d'	' -f1)

        if [ "$ahead_count" -gt 0 ]; then
            echo ""
            echo -e "${YELLOW}⚠ 当前分支 '$current_branch' 领先远程 $ahead_count 个提交。${NC}"
            echo -e "${YELLOW}是否推送到远程仓库？(y/N): ${NC}"
            read -r push_response
            if [[ $push_response =~ ^[Yy]$ ]]; then
                git push origin "$current_branch"
                echo -e "${GREEN}✓ 已推送到远程仓库${NC}"
            else
                echo -e "${YELLOW}跳过推送操作。请稍后手动运行 'git push'${NC}"
            fi
        fi
    else
        echo -e "${YELLOW}提示: 未检测到远程仓库。${NC}"
    fi
}