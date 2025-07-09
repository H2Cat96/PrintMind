<template>
  <span 
    ref="mathRef" 
    :class="['math-formula', { 'math-display': displayMode, 'math-inline': !displayMode }]"
  ></span>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from 'vue'
import katex from 'katex'
import 'katex/dist/katex.min.css'

interface Props {
  formula: string
  displayMode?: boolean
  throwOnError?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  displayMode: false,
  throwOnError: false
})

const mathRef = ref<HTMLElement>()

const renderMath = async () => {
  if (!mathRef.value || !props.formula) return

  try {
    await nextTick()
    katex.render(props.formula, mathRef.value, {
      displayMode: props.displayMode,
      throwOnError: props.throwOnError,
      strict: false,
      trust: false,
      macros: {
        "\\frac": "\\frac{#1}{#2}",
        "\\dfrac": "\\dfrac{#1}{#2}",
        "\\tfrac": "\\tfrac{#1}{#2}",
        "\\sqrt": "\\sqrt{#1}",
        "\\sum": "\\sum",
        "\\int": "\\int",
        "\\lim": "\\lim",
        "\\sin": "\\sin",
        "\\cos": "\\cos",
        "\\tan": "\\tan",
        "\\log": "\\log",
        "\\ln": "\\ln",
        "\\pi": "\\pi",
        "\\alpha": "\\alpha",
        "\\beta": "\\beta",
        "\\gamma": "\\gamma",
        "\\delta": "\\delta",
        "\\theta": "\\theta",
        "\\lambda": "\\lambda",
        "\\mu": "\\mu",
        "\\sigma": "\\sigma",
        "\\phi": "\\phi",
        "\\omega": "\\omega"
      }
    })
  } catch (error) {
    console.error('KaTeX rendering error:', error)
    if (mathRef.value) {
      mathRef.value.textContent = props.formula
      mathRef.value.style.color = 'red'
      mathRef.value.title = `数学公式渲染错误: ${error}`
    }
  }
}

onMounted(() => {
  renderMath()
})

watch(() => props.formula, () => {
  renderMath()
})

watch(() => props.displayMode, () => {
  renderMath()
})
</script>

<style scoped>
.math-formula {
  font-family: 'KaTeX_Main', 'Times New Roman', serif;
}

.math-inline {
  display: inline;
  vertical-align: baseline;
}

.math-display {
  display: block;
  text-align: center;
  margin: 1em 0;
}

/* 确保KaTeX样式正确加载 */
:deep(.katex) {
  font-size: inherit;
}

:deep(.katex-display) {
  margin: 1em 0;
  text-align: center;
}

:deep(.katex-html) {
  white-space: nowrap;
}

/* 错误状态样式 */
.math-formula[style*="color: red"] {
  background-color: #fee;
  padding: 2px 4px;
  border-radius: 3px;
  border: 1px solid #fcc;
}
</style>
