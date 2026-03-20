#!/usr/bin/env node

/**
 * Vue3 项目代码审查工具
 * 用于分析 Vue3 项目中的代码质量问题
 * 可在任何 Vue3 项目中使用
 */

import fs from 'fs/promises';
import path from 'path';

/**
 * Vue3 代码审查器类
 */
class Vue3CodeReviewer {
  constructor(options = {}) {
    this.options = {
      includePerformance: true,
      includeSecurity: true,
      includeBestPractices: true,
      projectPath: './',
      ...options
    };

    this.results = {
      summary: {
        totalFiles: 0,
        totalIssues: 0,
        totalComponents: 0,
        severityCounts: { critical: 0, high: 0, medium: 0, low: 0 }
      },
      issues: [],
      filesAnalyzed: []
    };
  }

  /**
   * 运行代码审查
   */
  async run(projectPath = './') {
    console.log('🚀 开始 Vue3 项目代码审查...');

    this.options.projectPath = projectPath;

    try {
      // 查找所有 Vue 文件
      const vueFiles = await this.findVueFiles(projectPath);

      console.log(`📋 找到 ${vueFiles.length} 个 Vue 文件`);

      this.results.summary.totalFiles = vueFiles.length;
      this.results.summary.totalComponents = vueFiles.length;

      // 分析每个文件
      for (const file of vueFiles) {
        const relativePath = path.relative(projectPath, file);
        console.log(`🔍 分析文件: ${relativePath}`);

        const content = await fs.readFile(file, 'utf-8');
        const fileInfo = {
          path: file,
          content: content,
          relativePath: relativePath
        };

        this.analyzeFile(fileInfo);
      }

      // 生成报告
      this.generateReport();

      return this.results;
    } catch (error) {
      console.error('❌ 代码审查过程中发生错误:', error);
      throw error;
    }
  }

  /**
   * 查找项目中的 Vue 文件
   */
  async findVueFiles(projectPath) {
    const walk = async (dir) => {
      let results = [];
      const entries = await fs.readdir(dir, { withFileTypes: true });

      for (const entry of entries) {
        const fullPath = path.resolve(dir, entry.name);

        // 忽略特定目录
        const relativePath = path.relative(projectPath, fullPath);
        const ignoreDirs = ['node_modules', 'dist', 'build', '.git', 'coverage', '.next', 'public'];

        if (ignoreDirs.some(ignoreDir => relativePath.startsWith(ignoreDir))) {
          continue;
        }

        if (entry.isDirectory()) {
          results = results.concat(await walk(fullPath));
        } else if (entry.isFile() && entry.name.endsWith('.vue')) {
          results.push(fullPath);
        }
      }

      return results;
    };

    return walk(projectPath);
  }

  /**
   * 分析单个文件
   */
  analyzeFile(fileInfo) {
    this.results.filesAnalyzed.push(fileInfo.relativePath);

    // 检查组件结构
    this.checkComponentStructure(fileInfo);

    // 检查 Composition API 使用
    this.checkCompositionAPI(fileInfo);

    // 检查 TypeScript 类型安全
    this.checkTypeSafety(fileInfo);

    // 检查性能问题
    if (this.options.includePerformance) {
      this.checkPerformanceIssues(fileInfo);
    }

    // 检查安全问题
    if (this.options.includeSecurity) {
      this.checkSecurityIssues(fileInfo);
    }

    // 检查最佳实践
    if (this.options.includeBestPractices) {
      this.checkBestPractices(fileInfo);
    }
  }

  /**
   * 检查组件结构
   */
  checkComponentStructure(fileInfo) {
    const content = fileInfo.content;

    // 检查文件长度
    const lines = content.split('\n').length;
    if (lines > 300) {
      this.addIssue(
        fileInfo,
        'component-too-long',
        `组件文件过长 (${lines} 行)，建议拆分为更小的组件`,
        'medium',
        { lines }
      );
    } else if (lines > 500) {
      this.addIssue(
        fileInfo,
        'component-too-long',
        `组件文件过长 (${lines} 行)，强烈建议拆分组件`,
        'high',
        { lines }
      );
    }

    // 检查是否包含 template、script 标签
    const hasTemplate = /<template[\s>]/.test(content);
    const hasScript = /<script[\s>]/.test(content);

    if (!hasTemplate) {
      this.addIssue(fileInfo, 'missing-template', '组件缺少 template 标签', 'critical');
    }

    if (!hasScript) {
      this.addIssue(fileInfo, 'missing-script', '组件缺少 script 标签', 'high');
    }

    // 检查 script 标签是否正确闭合
    const hasSetup = /<script\s+setup/.test(content);

    // 检查是否在非 setup 模式下正确导出组件
    if (!hasSetup) {
      if (!/export\s+default\s+{/.test(content) && /<script[\s>]/.test(content)) {
        this.addIssue(fileInfo, 'missing-default-export', '组件缺少默认导出', 'high');
      }
    }
  }

  /**
   * 检查 Composition API 使用
   */
  checkCompositionAPI(fileInfo) {
    const content = fileInfo.content;

    // 检查是否使用了 setup 语法糖
    const hasSetup = /<script\s+setup/.test(content);

    // 检查 ref 和 reactive 的使用
    const refMatches = (content.match(/\bref\s*\(/g) || []).length;
    const reactiveMatches = (content.match(/\breactive\s*\(/g) || []).length;

    if (refMatches === 0 && reactiveMatches === 0 && hasSetup) {
      // 在 setup 语法糖中如果没有使用响应式 API，可能是纯展示组件
    }

    // 检查是否正确解构了 ref
    if (/\bconst\s*{\s*\w+\s*}\s*=\s*ref\b/.test(content)) {
      this.addIssue(
        fileInfo,
        'incorrect-ref-destructure',
        '不应解构 ref，这会导致失去响应性，应使用 .value 访问',
        'high'
      );
    }

    // 检查 defineProps 使用
    if (hasSetup && /defineProps/.test(content)) {
      // 检查是否有类型注解
      if (!/defineProps<\s*\w+Props\s*>/.test(content) && !/\binterface\s+\w+Props\b/.test(content)) {
        this.addIssue(
          fileInfo,
          'props-missing-type-annotation',
          'Props 定义缺少类型注解，建议使用 TypeScript 定义 Props 类型',
          'medium'
        );
      }
    }
  }

  /**
   * 检查 TypeScript 类型安全
   */
  checkTypeSafety(fileInfo) {
    const content = fileInfo.content;

    // 检查是否使用了 TypeScript
    const hasTsSetup = /<script\s+setup\s+lang=["']ts["']/.test(content);
    const hasTsNormal = /<script\s+lang=["']ts["']/.test(content);
    const hasTs = hasTsSetup || hasTsNormal;

    if (!hasTs) {
      this.addIssue(
        fileInfo,
        'missing-typescript',
        '建议使用 TypeScript 以获得更好的类型安全',
        'medium'
      );
    }

    // 检查 defineProps 类型定义
    if (hasTs && /defineProps/.test(content)) {
      // 检查是否为 defineProps 定义了类型
      if (!/(defineProps)<\s*[\w<>{},\[\]\s]+\s*>/.test(content) &&
          !/(interface|type)\s+\w+Props/.test(content)) {
        this.addIssue(
          fileInfo,
          'props-missing-type',
          'Props 缺少明确的类型定义，建议使用接口或泛型定义',
          'high'
        );
      }
    }

    // 检查 defineEmits 类型定义
    if (hasTs && /defineEmits/.test(content)) {
      if (!/(defineEmits)<\s*[\w<>{},\[\]\s]+\s*>/.test(content) &&
          !/(interface|type)\s+\w+Emits/.test(content)) {
        this.addIssue(
          fileInfo,
          'emits-missing-type',
          'Emits 缺少明确的类型定义',
          'medium'
        );
      }
    }
  }

  /**
   * 检查性能问题
   */
  checkPerformanceIssues(fileInfo) {
    const content = fileInfo.content;

    // 检查是否同时使用了 v-if 和 v-for（在同一个元素上）
    if (/<[^>]*v-if[^>]*v-for[^>]*>/.test(content) || /<[^>]*v-for[^>]*v-if[^>]*>/.test(content)) {
      this.addIssue(
        fileInfo,
        'v-if-v-for-together',
        '避免在同一元素上同时使用 v-if 和 v-for，这可能导致性能问题',
        'high'
      );
    }

    // 检查是否使用了深度监听
    if (/watch\s*\([^,]*,[^}]*{[^}]*deep\s*:\s*true/.test(content)) {
      this.addIssue(
        fileInfo,
        'deep-watch',
        '深度监听可能影响性能，请确保确实需要深度监听',
        'medium'
      );
    }

    // 检查是否在模板中使用了复杂表达式
    const complexExpressionRegex = /\{\{[^}]*\([^)]*\)[^{]*\}\}/g;
    const complexMatches = content.match(complexExpressionRegex);
    if (complexMatches && complexMatches.length > 2) {
      this.addIssue(
        fileInfo,
        'complex-expression-in-template',
        `模板中使用了 ${complexMatches.length} 个复杂表达式，建议移至计算属性`,
        'medium'
      );
    }
  }

  /**
   * 检查安全问题
   */
  checkSecurityIssues(fileInfo) {
    const content = fileInfo.content;

    // 检查是否使用了 v-html（可能存在 XSS 风险）
    if (/<[^>]*v-html/.test(content)) {
      this.addIssue(
        fileInfo,
        'potential-xss',
        '使用 v-html 可能导致 XSS 攻击，请谨慎使用并验证内容',
        'critical'
      );
    }

    // 检查是否有直接的 DOM 操作
    if (/\$refs\.[\w]+\.innerHTML/.test(content) ||
        /\$refs\.[\w]+\.outerHTML/.test(content)) {
      this.addIssue(
        fileInfo,
        'potential-dom-xss',
        '直接操作 innerHTML 或 outerHTML 可能导致 XSS，请使用文本赋值代替',
        'high'
      );
    }

    // 检查是否使用了不安全的动态组件
    if (/<component[^>]+:[^>]+>\s*<(\/?)component/.test(content)) {
      this.addIssue(
        fileInfo,
        'dynamic-component-risk',
        '动态组件可能存在安全风险，请确保组件来源可信',
        'medium'
      );
    }
  }

  /**
   * 检查最佳实践
   */
  checkBestPractices(fileInfo) {
    const content = fileInfo.content;

    // 检查组件名是否遵循 PascalCase
    const scriptMatch = content.match(/<script[^>]*>([\s\S]*?)<\/script>/);
    if (scriptMatch) {
      const scriptContent = scriptMatch[1];
      const nameMatch = scriptContent.match(/name:\s*['"]([a-z][^'"]*)['"]/);
      if (nameMatch && /^[a-z]/.test(nameMatch[1])) {
        this.addIssue(
          fileInfo,
          'component-name-case',
          `组件名 "${nameMatch[1]}" 应使用 PascalCase 格式（首字母大写）`,
          'low'
        );
      }
    }

    // 检查是否在模板中使用了索引作为 key
    if (/<[^>]*:key\s*=\s*["']?\w+\.index/.test(content) ||
        /<[^>]*:key\s*=\s*["']?\w+\[['"]?\w+['"]?\]/.test(content)) {
      this.addIssue(
        fileInfo,
        'index-as-key',
        '避免使用数组索引作为 key，这可能导致意外的行为',
        'high'
      );
    }

    // 检查是否有未使用的导入
    // 这个检查比较复杂，这里仅做简单版本
    if (/(import\s+{|import\s+[\w*]+\s+from)/.test(content)) {
      // 在实际实现中需要更复杂的分析
    }
  }

  /**
   * 添加问题到结果中
   */
  addIssue(fileInfo, ruleId, message, severity, meta = {}) {
    const issue = {
      file: fileInfo.relativePath,
      ruleId,
      message,
      severity,
      meta: { ...meta, component: path.basename(fileInfo.path, '.vue') }
    };

    this.results.issues.push(issue);
    this.results.summary.severityCounts[severity]++;
    this.results.summary.totalIssues++;
  }

  /**
   * 生成审查报告
   */
  generateReport() {
    console.log('\n📊 代码审查报告:');
    console.log('=====================');
    console.log(`总文件数: ${this.results.summary.totalFiles}`);
    console.log(`总组件数: ${this.results.summary.totalComponents}`);
    console.log(`总问题数: ${this.results.summary.totalIssues}`);
    console.log(`严重问题: ${this.results.summary.severityCounts.critical}`);
    console.log(`高危问题: ${this.results.summary.severityCounts.high}`);
    console.log(`中等问题: ${this.results.summary.severityCounts.medium}`);
    console.log(`低等问题: ${this.results.summary.severityCounts.low}`);

    if (this.results.issues.length > 0) {
      console.log('\n📝 详细问题:');
      console.log('-------------');

      // 按严重程度排序
      const sortedIssues = this.results.issues.sort((a, b) => {
        const severityOrder = { critical: 4, high: 3, medium: 2, low: 1 };
        return severityOrder[b.severity] - severityOrder[a.severity];
      });

      // 按文件分组显示
      const issuesByFile = {};
      for (const issue of sortedIssues) {
        if (!issuesByFile[issue.file]) {
          issuesByFile[issue.file] = [];
        }
        issuesByFile[issue.file].push(issue);
      }

      for (const [file, fileIssues] of Object.entries(issuesByFile)) {
        console.log(`\n📁 ${file}:`);

        for (const issue of fileIssues) {
          const severitySymbol = {
            critical: '🔴 [CRITICAL]',
            high: '🟠 [HIGH]',
            medium: '🟡 [MEDIUM]',
            low: '🔵 [LOW]'
          }[issue.severity];

          console.log(`   ${severitySymbol} ${issue.message} (${issue.ruleId})`);
        }
      }

      // 显示摘要建议
      console.log('\n💡 改进建议:');
      console.log('-------------');
      if (this.results.summary.severityCounts.critical > 0) {
        console.log('🚨 发现严重问题，建议立即修复');
      }
      if (this.results.summary.severityCounts.high > 0) {
        console.log('⚠️ 发现高危问题，建议尽快修复');
      }
      if (this.results.summary.totalIssues > 0) {
        console.log(`📈 整体代码质量有待提升，共发现 ${this.results.summary.totalIssues} 个问题`);
      } else {
        console.log('✅ 代码质量良好，未发现问题！');
      }
    } else {
      console.log('\n✅ 没有发现问题，代码质量良好！');
    }
  }
}

// 导出类供其他模块使用
export default Vue3CodeReviewer;

// 如果作为脚本运行
if (typeof require !== 'undefined' && require.main === module) {
  // 解析命令行参数
  const args = process.argv.slice(2);

  if (args.includes('--help') || args.includes('-h')) {
    console.log(`
Vue3 代码审查工具

用法:
  node vue3-analyzer.mjs [options] [project-path]

选项:
  --performance       包含性能问题检查
  --security          包含安全问题检查
  --best-practices    包含最佳实践检查
  --help, -h         显示帮助信息

示例:
  node vue3-analyzer.mjs                      # 审查当前目录
  node vue3-analyzer.mjs src/components/      # 审查特定目录
  node vue3-analyzer.mjs --security           # 只检查安全问题
    `);
    process.exit(0);
  }

  // 解析选项
  const options = {
    includePerformance: args.includes('--performance'),
    includeSecurity: args.includes('--security'),
    includeBestPractices: args.includes('--best-practices'),
    projectPath: './'
  };

  // 如果没有指定特殊选项，则全部启用
  if (!args.includes('--performance') &&
      !args.includes('--security') &&
      !args.includes('--best-practices')) {
    options.includePerformance = true;
    options.includeSecurity = true;
    options.includeBestPractices = true;
  }

  // 查找项目路径（非选项参数）
  const pathArg = args.find(arg => !arg.startsWith('--') && arg !== '-h');
  if (pathArg) {
    options.projectPath = pathArg;
  }

  const reviewer = new Vue3CodeReviewer(options);

  reviewer.run(options.projectPath).catch(err => {
    console.error('代码审查失败:', err);
    process.exit(1);
  });
}