<template>
  <div class="math-test-view p-8 max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-8 text-center">LaTeX数学公式测试</h1>
    
    <!-- 基础分数测试 -->
    <div class="test-section mb-8">
      <h2 class="text-xl font-semibold mb-4">基础分数</h2>
      <div class="grid grid-cols-2 gap-4">
        <div class="formula-card">
          <h3 class="text-sm font-medium text-gray-600 mb-2">行内分数</h3>
          <MarkdownRenderer content="这是一个分数：$\frac{1}{2}$，还有 $\frac{3}{4}$" />
        </div>
        <div class="formula-card">
          <h3 class="text-sm font-medium text-gray-600 mb-2">块级分数</h3>
          <MarkdownRenderer content="$$\frac{a}{b} = \frac{c}{d}$$" />
        </div>
      </div>
    </div>

    <!-- 复杂分数测试 -->
    <div class="test-section mb-8">
      <h2 class="text-xl font-semibold mb-4">复杂分数</h2>
      <div class="grid grid-cols-1 gap-4">
        <div class="formula-card">
          <h3 class="text-sm font-medium text-gray-600 mb-2">分数运算</h3>
          <MarkdownRenderer content="$$\frac{1}{2} + \frac{1}{3} = \frac{3 + 2}{6} = \frac{5}{6}$$" />
        </div>
        <div class="formula-card">
          <h3 class="text-sm font-medium text-gray-600 mb-2">复杂分数</h3>
          <MarkdownRenderer content="$$\frac{x^2 + 2x + 1}{x - 1} = \frac{(x+1)^2}{x-1}$$" />
        </div>
      </div>
    </div>

    <!-- 算数题示例 -->
    <div class="test-section mb-8">
      <h2 class="text-xl font-semibold mb-4">算数题示例</h2>
      <div class="grid grid-cols-1 gap-4">
        <div class="formula-card">
          <h3 class="text-sm font-medium text-gray-600 mb-2">整数运算</h3>
          <MarkdownRenderer content="**第1题：** $6 \times 7 = 42$

**第2题：** $15 + 28 = 43$

**第3题：** $84 \div 12 = 7$" />
        </div>
        <div class="formula-card">
          <h3 class="text-sm font-medium text-gray-600 mb-2">分数运算</h3>
          <MarkdownRenderer content="**第1题：** $\frac{1}{2} + \frac{1}{4} = \frac{3}{4}$

**第2题：** $\frac{2}{3} \times \frac{3}{5} = \frac{2}{5}$

**第3题：** $\frac{3}{4} \div \frac{1}{2} = \frac{3}{2}$" />
        </div>
      </div>
    </div>

    <!-- 数学符号测试 -->
    <div class="test-section mb-8">
      <h2 class="text-xl font-semibold mb-4">数学符号</h2>
      <div class="grid grid-cols-2 gap-4">
        <div class="formula-card">
          <h3 class="text-sm font-medium text-gray-600 mb-2">希腊字母</h3>
          <MarkdownRenderer content="$\alpha, \beta, \gamma, \delta, \pi, \theta, \lambda, \sigma$" />
        </div>
        <div class="formula-card">
          <h3 class="text-sm font-medium text-gray-600 mb-2">运算符</h3>
          <MarkdownRenderer content="$\pm, \times, \div, \neq, \leq, \geq, \approx$" />
        </div>
      </div>
    </div>

    <!-- 高级数学 -->
    <div class="test-section mb-8">
      <h2 class="text-xl font-semibold mb-4">高级数学</h2>
      <div class="grid grid-cols-1 gap-4">
        <div class="formula-card">
          <h3 class="text-sm font-medium text-gray-600 mb-2">求和与积分</h3>
          <MarkdownRenderer content="$$\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$$

$$\int_{a}^{b} f(x) dx$$" />
        </div>
        <div class="formula-card">
          <h3 class="text-sm font-medium text-gray-600 mb-2">极限与根号</h3>
          <MarkdownRenderer content="$$\lim_{x \to 0} \frac{\sin x}{x} = 1$$

$$\sqrt{x^2 + y^2} = \sqrt[n]{x^n + y^n}$$" />
        </div>
      </div>
    </div>

    <!-- 数学工具栏测试 -->
    <div class="test-section mb-8">
      <h2 class="text-xl font-semibold mb-4">数学工具栏测试</h2>
      <div class="bg-gray-50 p-4 rounded-lg">
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            测试输入区域（点击下方工具栏按钮插入公式）：
          </label>
          <textarea
            v-model="testInput"
            class="w-full h-32 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="在此输入数学公式..."
          ></textarea>
        </div>
        
        <div class="mb-4">
          <MathToolbar @insert-formula="insertTestFormula" />
        </div>
        
        <div class="bg-white p-4 border rounded-lg">
          <h4 class="text-sm font-medium text-gray-700 mb-2">预览效果：</h4>
          <MarkdownRenderer :content="testInput" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import MarkdownRenderer from '@/components/MarkdownRenderer.vue'
import MathToolbar from '@/components/MathToolbar.vue'

const testInput = ref(`# 数学公式测试

这是一个行内公式：$\\frac{1}{2} + \\frac{1}{3} = \\frac{5}{6}$

这是一个块级公式：
$$\\sum_{i=1}^{n} i^2 = \\frac{n(n+1)(2n+1)}{6}$$

算数题示例：
**第1题：** $6 \\times 7 = 42$
**第2题：** $\\frac{3}{4} + \\frac{1}{8} = \\frac{7}{8}$`)

const insertTestFormula = (formula: string) => {
  testInput.value += formula
}
</script>

<style scoped>
.test-section {
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 2rem;
}

.formula-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.formula-card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.2s;
}
</style>
