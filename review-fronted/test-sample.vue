<template>
  <div>
    <h1>{{ title }}</h1>
    <p v-html="userInput"></p>
    <div v-for="item in items" :key="item.id">
      <span v-if="item.visible">{{ item.name }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';

interface TestProps {
  title: string;
}

const props = withDefaults(defineProps<TestProps>(), {
  title: 'Default Title'
});

const userInput = ref('<script>alert("xss")</script>');
const items = reactive([
  { id: 0, name: 'Item 1', visible: true },
  { id: 1, name: 'Item 2', visible: false }
]);
</script>