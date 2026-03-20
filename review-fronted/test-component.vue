<template>
  <div>
    <h1>{{ title }}</h1>
    <p v-if="showDescription">这是一个测试组件</p>
    <!-- 错误用法：使用索引作为 key -->
    <div v-for="(item, index) in items" :key="index">{{ item }}</div>

    <!-- 潜在的安全问题：使用 v-html -->
    <div v-html="unsafeContent"></div>
  </template>

<script setup lang="ts">
import { ref, reactive } from 'vue';

// 定义 props（无类型定义）
const props = defineProps(['title', 'showDescription']);

// 没有为 defineProps 定义类型
const items = ref(['item1', 'item2', 'item3']);
const unsafeContent = ref('<script>alert("XSS")</script>');

// 复杂的模板表达式
const computedValue = () => {
  return items.value.map(item => item.toUpperCase()).join(', ');
};
</script>

<style scoped>
.title {
  color: blue;
}
</style>