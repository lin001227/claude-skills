# Claude Code Skills - commit-code-new

## 技能概述

`commit-code-new` 是一个基于纯Bash实现的智能Git提交助手，旨在替代原有的Python版本，提供相同的功能但更高的性能和更少的依赖。

## 功能特性

- **智能提交信息生成**：自动分析更改内容并生成符合 Conventional Commits 规范的提交信息
- **分支管理**：创建、切换、列出分支等功能
- **零依赖**：只需要 Git 和 Bash 环境
- **交互式体验**：提供提交信息预览和确认流程
- **安全性检查**：防止意外提交敏感信息

## 在Claude中使用

由于这是一个Claude Code技能，您可以通过以下方式使用：

### 1. 自动触发
当您说以下内容时，技能会自动触发：
- "提交我的更改"
- "生成提交信息"
- "创建新分支 feature/my-feature"
- "切换到 main 分支"
- 等相关Git操作请求

### 2. 直接调用
您也可以通过直接命令调用：
```bash
commit-code-new
commit-code-new create feature/new-feature
commit-code-new switch develop
commit-code-new list
```

## 技能配置

此技能已配置在Claude环境中，位于 `d:/claude-skills/commit-code-new/` 目录下。
所有必要的权限已在 `.claude/settings.local.json` 中设置。

## 优势

- 不需要Python环境
- 更快的执行速度
- 更少的系统资源占用
- 与原有功能保持一致

## 注意事项

- 仅在Git仓库中运行
- 尊重用户的.gitignore配置
- 严格按照Conventional Commits规范生成提交信息