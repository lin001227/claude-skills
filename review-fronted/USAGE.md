# Vue3 代码审查技能配置

## 技能名称
`/review-frontend`

## 描述
这是一个专门用于审查 Vue3 项目代码质量的技能。它可以检查常见的代码问题、性能问题、安全问题和最佳实践。

## 触发条件
- 当用户在 Vue3 项目中运行 `/review-frontend` 命令时
- 当检测到项目包含 Vue3 相关文件（如 .vue 文件）时

## 使用方法
```
/review-frontend
```

## 功能
1. 检查组件结构和文件长度
2. 审查 Composition API 使用
3. 验证 TypeScript 类型安全
4. 识别性能问题
5. 检测安全漏洞
6. 验证最佳实践

## 配置选项
- `--performance`: 包含性能问题检查
- `--security`: 包含安全问题检查
- `--best-practices`: 包含最佳实践检查

## 示例
```
/review-frontend                    # 审查整个项目
/review-frontend src/components/    # 审查特定目录
```