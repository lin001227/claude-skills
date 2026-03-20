# Vue3 代码审查技能 (/review-frontend)

## 概述
这是一个专门用于审查 Vue3 项目代码质量的技能，可以帮助开发者识别潜在的问题、改进代码质量和提高性能。

## 安装与配置

### 文件结构
```
.claude/
└── skills/
    └── vue3-code-review/
        ├── index.mjs          # 主执行文件
        ├── README.md          # 详细说明
        ├── USAGE.md           # 使用说明
        ├── package.json       # 配置文件
        └── test-component.vue # 测试文件
```

### 权限配置
由于这是一个自定义技能，您可能需要确保 Node.js 脚本能够执行。如需权限设置，请参考您的 Claude Code 配置。

## 使用方法

### 基本用法
```
/review-frontend
```

或者直接运行脚本：
```bash
node .claude/skills/vue3-code-review/index.mjs
```

### 带参数的用法
```bash
# 审查特定目录
node .claude/skills/vue3-code-review/index.mjs src/components/

# 只检查安全问题
node .claude/skills/vue3-code-review/index.mjs --security

# 只检查性能问题
node .claude/skills/vue3-code-review/index.mjs --performance

# 只检查最佳实践
node .claude/skills/vue3-code-review/index.mjs --best-practices

# 查看帮助
node .claude/skills/vue3-code-review/index.mjs --help
```

## 检查功能

### 1. 组件结构检查
- **文件长度检查**：检查组件文件是否过长（超过300行为警告，超过500行为严重）
- **标签完整性**：确保包含 `<template>` 和 `<script>` 标签
- **标签配对**：验证所有标签是否正确配对

### 2. Composition API 检查
- **响应式 API 使用**：检查 `ref` 和 `reactive` 的正确使用
- **setup 语法糖**：验证 `<script setup>` 语法的使用
- **错误解构**：检测不正确的 ref 解构（可能导致失去响应性）

### 3. TypeScript 类型安全
- **TypeScript 使用**：建议使用 TypeScript
- **Props 类型定义**：检查是否为 `defineProps` 定义了类型
- **Emits 类型定义**：检查是否为 `defineEmits` 定义了类型

### 4. 性能问题检查
- **v-if 和 v-for 滥用**：避免在同一元素上同时使用 v-if 和 v-for
- **深度监听**：标识深度监听的使用（可能影响性能）
- **模板复杂表达式**：检测模板中的复杂表达式

### 5. 安全问题检查
- **XSS 风险**：检测 `v-html` 的使用
- **DOM 操作**：检测不安全的直接 DOM 操作
- **动态组件**：检查动态组件的安全性

### 6. 最佳实践检查
- **组件命名**：检查组件命名是否符合 PascalCase 规范
- **Key 属性**：检测数组渲染中使用索引作为 key 的情况
- **未使用导入**：简单检查未使用的导入（基础版本）

## 输出格式

审查完成后，工具会生成以下信息：

1. **概览信息**：
   - 总文件数
   - 总组件数
   - 总问题数
   - 各严重程度问题数

2. **详细问题**：
   - 文件路径
   - 问题描述
   - 严重程度（critical, high, medium, low）
   - 规则ID

3. **改进建议**：
   - 根据问题严重程度提供改进建议

## 示例输出

```
🚀 开始 Vue3 项目代码审查...
📋 找到 5 个 Vue 文件
🔍 分析文件: src/components/Button.vue
🔍 分析文件: src/views/Home.vue
...

📊 代码审查报告:
=====================
总文件数: 5
总组件数: 5
总问题数: 3
严重问题: 0
高危问题: 1
中等问题: 2
低等问题: 0

📝 详细问题:
-------------
📁 src/components/DangerousComponent.vue:
   🟠 [HIGH] 使用 v-html 可能导致 XSS 攻击，请谨慎使用并验证内容 (potential-xss)

📁 src/views/Home.vue:
   🟡 [MEDIUM] 组件文件过长 (350 行)，建议拆分为更小的组件 (component-too-long)
   🟡 [MEDIUM] Props 缺少明确的类型定义，建议使用接口或泛型定义 (props-missing-type)

💡 改进建议:
-------------
⚠️ 发现高危问题，建议尽快修复
📈 整体代码质量有待提升，共发现 3 个问题
```

## 自定义配置

您可以通过修改 `index.mjs` 中的默认配置来调整检查行为：

```javascript
const reviewer = new Vue3CodeReviewer({
  includePerformance: true,      // 是否检查性能问题
  includeSecurity: true,         // 是否检查安全问题
  includeBestPractices: true,    // 是否检查最佳实践
  projectPath: './'              // 项目路径
});
```

## 故障排除

### 1. 如果没有输出
- 检查是否有 Vue 文件（.vue 扩展名）
- 确保 Node.js 版本兼容（需要支持 ES 模块）

### 2. 权限问题
- 在某些系统上可能需要设置执行权限
- 可以使用 `chmod +x .claude/skills/vue3-code-review/index.mjs`（Linux/Mac）

### 3. 错误处理
- 工具会在遇到错误时输出错误信息
- 检查文件路径和权限设置

## 扩展性

这个技能是模块化的，您可以轻松添加新的检查规则：

1. 在 `Vue3CodeReviewer` 类中添加新的检查方法
2. 在 `analyzeFile` 方法中调用新方法
3. 使用 `addIssue` 方法添加检测到的问题

例如，添加一个新的检查：
```javascript
checkNewRule(fileInfo) {
  if (someCondition) {
    this.addIssue(
      fileInfo,
      'rule-id',
      '问题描述',
      'severity-level'
    );
  }
}
```

## 适用场景

- Vue3 项目代码质量评估
- 团队代码规范检查
- 项目重构前的代码审查
- 新成员代码提交前检查
- 自动化 CI/CD 流程集成