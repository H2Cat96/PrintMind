<template>
  <div class="math-toolbar">
    <div class="toolbar-header">
      <h4 class="text-sm font-medium text-gray-700 mb-2">数学公式工具</h4>
    </div>
    
    <div class="toolbar-content">
      <!-- 基础分数 -->
      <div class="formula-group">
        <h5 class="group-title">分数</h5>
        <div class="formula-buttons">
          <button @click="insertFormula('\\frac{1}{2}')" class="formula-btn" title="二分之一">
            <MathFormula formula="\frac{1}{2}" />
          </button>
          <button @click="insertFormula('\\frac{a}{b}')" class="formula-btn" title="分数模板">
            <MathFormula formula="\frac{a}{b}" />
          </button>
          <button @click="insertFormula('\\frac{x^2}{y}')" class="formula-btn" title="复杂分数">
            <MathFormula formula="\frac{x^2}{y}" />
          </button>
        </div>
      </div>

      <!-- 指数和根号 -->
      <div class="formula-group">
        <h5 class="group-title">指数与根号</h5>
        <div class="formula-buttons">
          <button @click="insertFormula('x^2')" class="formula-btn" title="平方">
            <MathFormula formula="x^2" />
          </button>
          <button @click="insertFormula('x^{n}')" class="formula-btn" title="指数">
            <MathFormula formula="x^{n}" />
          </button>
          <button @click="insertFormula('\\sqrt{x}')" class="formula-btn" title="平方根">
            <MathFormula formula="\sqrt{x}" />
          </button>
          <button @click="insertFormula('\\sqrt[n]{x}')" class="formula-btn" title="n次根">
            <MathFormula formula="\sqrt[n]{x}" />
          </button>
        </div>
      </div>

      <!-- 求和与积分 -->
      <div class="formula-group">
        <h5 class="group-title">求和与积分</h5>
        <div class="formula-buttons">
          <button @click="insertFormula('\\sum_{i=1}^{n}')" class="formula-btn" title="求和">
            <MathFormula formula="\sum_{i=1}^{n}" />
          </button>
          <button @click="insertFormula('\\int_{a}^{b}')" class="formula-btn" title="定积分">
            <MathFormula formula="\int_{a}^{b}" />
          </button>
          <button @click="insertFormula('\\lim_{x \\to 0}')" class="formula-btn" title="极限">
            <MathFormula formula="\lim_{x \to 0}" />
          </button>
        </div>
      </div>

      <!-- 三角函数 -->
      <div class="formula-group">
        <h5 class="group-title">三角函数</h5>
        <div class="formula-buttons">
          <button @click="insertFormula('\\sin(x)')" class="formula-btn" title="正弦">
            <MathFormula formula="\sin(x)" />
          </button>
          <button @click="insertFormula('\\cos(x)')" class="formula-btn" title="余弦">
            <MathFormula formula="\cos(x)" />
          </button>
          <button @click="insertFormula('\\tan(x)')" class="formula-btn" title="正切">
            <MathFormula formula="\tan(x)" />
          </button>
        </div>
      </div>

      <!-- 希腊字母 -->
      <div class="formula-group">
        <h5 class="group-title">希腊字母</h5>
        <div class="formula-buttons">
          <button @click="insertFormula('\\alpha')" class="formula-btn" title="α">
            <MathFormula formula="\alpha" />
          </button>
          <button @click="insertFormula('\\beta')" class="formula-btn" title="β">
            <MathFormula formula="\beta" />
          </button>
          <button @click="insertFormula('\\gamma')" class="formula-btn" title="γ">
            <MathFormula formula="\gamma" />
          </button>
          <button @click="insertFormula('\\delta')" class="formula-btn" title="δ">
            <MathFormula formula="\delta" />
          </button>
          <button @click="insertFormula('\\pi')" class="formula-btn" title="π">
            <MathFormula formula="\pi" />
          </button>
          <button @click="insertFormula('\\theta')" class="formula-btn" title="θ">
            <MathFormula formula="\theta" />
          </button>
        </div>
      </div>

      <!-- 运算符 -->
      <div class="formula-group">
        <h5 class="group-title">运算符</h5>
        <div class="formula-buttons">
          <button @click="insertFormula('\\pm')" class="formula-btn" title="±">
            <MathFormula formula="\pm" />
          </button>
          <button @click="insertFormula('\\times')" class="formula-btn" title="×">
            <MathFormula formula="\times" />
          </button>
          <button @click="insertFormula('\\div')" class="formula-btn" title="÷">
            <MathFormula formula="\div" />
          </button>
          <button @click="insertFormula('\\neq')" class="formula-btn" title="≠">
            <MathFormula formula="\neq" />
          </button>
          <button @click="insertFormula('\\leq')" class="formula-btn" title="≤">
            <MathFormula formula="\leq" />
          </button>
          <button @click="insertFormula('\\geq')" class="formula-btn" title="≥">
            <MathFormula formula="\geq" />
          </button>
        </div>
      </div>

      <!-- 快速插入 -->
      <div class="formula-group">
        <h5 class="group-title">快速插入</h5>
        <div class="formula-buttons">
          <button @click="insertInlineFormula" class="formula-btn-text" title="行内公式">
            行内公式 $...$
          </button>
          <button @click="insertDisplayFormula" class="formula-btn-text" title="块级公式">
            块级公式 $$...$$
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import MathFormula from './MathFormula.vue'

interface Emits {
  (e: 'insert-formula', formula: string): void
}

const emit = defineEmits<Emits>()

const insertFormula = (formula: string) => {
  emit('insert-formula', `$${formula}$`)
}

const insertInlineFormula = () => {
  emit('insert-formula', '$公式$')
}

const insertDisplayFormula = () => {
  emit('insert-formula', '\n$$\n公式\n$$\n')
}
</script>

<style scoped>
.math-toolbar {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 12px;
  max-height: 400px;
  overflow-y: auto;
}

.toolbar-header {
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 8px;
  margin-bottom: 12px;
}

.formula-group {
  margin-bottom: 16px;
}

.group-title {
  font-size: 0.75rem;
  font-weight: 600;
  color: #6b7280;
  margin-bottom: 6px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.formula-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(60px, 1fr));
  gap: 4px;
}

.formula-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px 4px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
  min-height: 36px;
}

.formula-btn:hover {
  background: #f3f4f6;
  border-color: #9ca3af;
}

.formula-btn:active {
  background: #e5e7eb;
}

.formula-btn-text {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6px 8px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.75rem;
  color: #374151;
  grid-column: span 2;
}

.formula-btn-text:hover {
  background: #f3f4f6;
  border-color: #9ca3af;
}

/* 滚动条样式 */
.math-toolbar::-webkit-scrollbar {
  width: 6px;
}

.math-toolbar::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.math-toolbar::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.math-toolbar::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
