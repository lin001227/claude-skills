# commit-code-new 使用说明

## 概述

commit-code-new 是一个基于纯 Bash 实现的智能 Git 提交助手，它能够自动生成符合 Conventional Commits 规范的提交信息，并提供便捷的分支管理功能。

## 主要功能

### 提交功能
- 自动分析 Git 更改
- 生成规范化的提交信息
- 提供提交预览和确认

### 分支管理功能
- 创建新分支
- 切换分支
- 列出分支
- 分支命名规范检查

## 使用方式

### 基础提交操作
```bash
# 直接执行提交流程
commit-code-new

# 执行提交时自动处理暂存的更改
```

### 分支管理
```bash
# 创建新分支
commit-code-new create feature/my-feature

# 切换到现有分支
commit-code-new switch main

# 查看所有分支
commit-code-new list
```

## 功能特点

### 自动检测更改类型
- 根据文件类型自动确定提交类别（feat, fix, docs, style, refactor, test, chore）
- 根据文件路径确定提交作用域（components, utils, services等）

### 交互式提交
- 自动生成提交信息建议
- 允许用户修改或确认
- 提交完成后提示推送选项

### 分支命名规范
- 提供分支命名最佳实践
- 检查是否遵循常见规范（feature/, bugfix/, hotfix/等）