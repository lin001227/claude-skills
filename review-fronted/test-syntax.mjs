// 简单测试脚本，验证主程序文件语法是否正确
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

async function testSyntax() {
  try {
    // 检查 JavaScript 语法
    await execAsync('node --check .claude/skills/vue3-code-review/index.mjs');
    console.log('✅ 语法检查通过');
  } catch (error) {
    console.error('❌ 语法错误:', error.message);
  }
}

testSyntax();