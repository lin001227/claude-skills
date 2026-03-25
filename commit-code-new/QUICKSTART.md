# 快速开始 - commit-code-new

## 安装

只需确保你有 Git 和 Bash 环境即可，无需额外依赖。

## 基本使用

### 1. 执行代码提交
当你完成了代码修改后，运行：
```bash
commit-code-new
```

这将会：
- 分析当前 Git 工作区状态
- 生成已暂存文件的摘要
- 提供符合 Conventional Commits 规范的提交信息建议
- 让你确认或修改提交信息
- 执行最终的提交操作

### 2. 分支管理
#### 创建新分支
```bash
commit-code-new create feature/new-feature
```

#### 切换分支
```bash
commit-code-new switch develop
```

#### 查看分支列表
```bash
commit-code-new list
```

## 高级用法

### 手动暂存后提交
如果你想要选择性提交部分更改：
```bash
git add src/file1.js src/file2.js  # 只添加部分文件
commit-code-new                   # 自动处理暂存的文件
```

### 分支命名规范
建议使用以下格式创建分支：
- 新功能：`feature/功能描述`
- 修复 Bug：`bugfix/问题描述`
- 紧急修复：`hotfix/问题描述`
- 文档更新：`docs/文档描述`

## 工作流程

1. 编写代码并保存
2. 使用 `git add` 暂存想要提交的文件
3. 运行 `commit-code-new`
4. 检查工具生成的更改摘要
5. 确认或修改建议的提交信息
6. 完成提交
7. 如有必要，推送更改到远程仓库