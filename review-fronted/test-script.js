console.log('Vue3 代码审查工具测试');

// 简单的测试来验证脚本是否能运行
const testFile = `
<template>
  <div>
    <h1>{{ title }}</h1>
    <p v-html="userInput"></p>
    <div v-for="item in items" :key="item.index">
      <span v-if="item.visible">{{ item.name }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const title = ref('Test');
const userInput = '<b>Safe content</b>';
const items = [
  { id: 1, name: 'Item 1', visible: true },
  { id: 2, name: 'Item 2', visible: false }
];
</script>
`;

// 模拟一些基本检查
console.log('🔍 开始代码分析...');

// 检查 v-html 使用 (安全问题)
if (testFile.includes('v-html=')) {
  console.log('⚠️  发现安全问题: 使用了 v-html，可能存在 XSS 风险');
}

// 检查 index 作为 key (性能问题)
if (testFile.includes(':key="item.index"')) {
  console.log('⚠️  发现性能问题: 使用了 index 作为 key');
}

// 检查 TypeScript 使用
const hasTs = testFile.includes('lang="ts"');
if (!hasTs) {
  console.log('💡 建议: 未使用 TypeScript，建议启用以获得更好的类型安全');
}

console.log('✅ 代码分析完成');