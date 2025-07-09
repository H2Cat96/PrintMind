<template>
  <div class="markdown-renderer" v-html="renderedContent"></div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import katex from 'katex'
import 'katex/dist/katex.min.css'

interface Props {
  content: string
}

const props = defineProps<Props>()

// 渲染LaTeX数学公式的函数
const renderMathInHTML = (html: string): string => {
  // 处理行内数学公式 $...$
  html = html.replace(/\$([^$\n]+?)\$/g, (match, formula) => {
    try {
      return katex.renderToString(formula, {
        displayMode: false,
        throwOnError: false,
        strict: false
      })
    } catch (error) {
      console.warn('Inline math rendering error:', error)
      return `<span class="math-error" title="数学公式错误: ${error}">${match}</span>`
    }
  })

  // 处理块级数学公式 $$...$$
  html = html.replace(/\$\$([^$]+?)\$\$/g, (match, formula) => {
    try {
      return `<div class="math-display">${katex.renderToString(formula, {
        displayMode: true,
        throwOnError: false,
        strict: false
      })}</div>`
    } catch (error) {
      console.warn('Display math rendering error:', error)
      return `<div class="math-error" title="数学公式错误: ${error}">${match}</div>`
    }
  })

  return html
}

// 基础Markdown渲染函数
const renderMarkdown = (content: string): string => {
  let html = content

  // 标题
  html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>')
  html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>')
  html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>')

  // 粗体和斜体
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
  html = html.replace(/\*(.*?)\*/g, '<em>$1</em>')

  // 行内代码
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>')

  // 代码块
  html = html.replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code class="language-$1">$2</code></pre>')

  // 链接
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>')

  // 无序列表
  html = html.replace(/^\s*[-*+]\s+(.*)$/gm, '<li>$1</li>')
  html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')

  // 有序列表
  html = html.replace(/^\s*\d+\.\s+(.*)$/gm, '<li>$1</li>')

  // 段落
  html = html.replace(/\n\n/g, '</p><p>')
  html = '<p>' + html + '</p>'

  // 清理空段落
  html = html.replace(/<p><\/p>/g, '')
  html = html.replace(/<p>(<h[1-6]>)/g, '$1')
  html = html.replace(/(<\/h[1-6]>)<\/p>/g, '$1')
  html = html.replace(/<p>(<ul>)/g, '$1')
  html = html.replace(/(<\/ul>)<\/p>/g, '$1')
  html = html.replace(/<p>(<pre>)/g, '$1')
  html = html.replace(/(<\/pre>)<\/p>/g, '$1')

  return html
}

const renderedContent = computed(() => {
  if (!props.content) return ''
  
  // 先渲染基础Markdown
  let html = renderMarkdown(props.content)
  
  // 然后渲染数学公式
  html = renderMathInHTML(html)
  
  return html
})
</script>

<style scoped>
.markdown-renderer {
  line-height: 1.6;
  color: #333;
}

:deep(h1) {
  font-size: 2em;
  font-weight: bold;
  margin: 1em 0 0.5em 0;
  color: #2c3e50;
}

:deep(h2) {
  font-size: 1.5em;
  font-weight: bold;
  margin: 1em 0 0.5em 0;
  color: #34495e;
}

:deep(h3) {
  font-size: 1.2em;
  font-weight: bold;
  margin: 1em 0 0.5em 0;
  color: #34495e;
}

:deep(p) {
  margin: 0.5em 0;
}

:deep(strong) {
  font-weight: bold;
}

:deep(em) {
  font-style: italic;
}

:deep(code) {
  background-color: #f4f4f4;
  padding: 2px 4px;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  font-size: 0.9em;
}

:deep(pre) {
  background-color: #f8f8f8;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 1em;
  overflow-x: auto;
  margin: 1em 0;
}

:deep(pre code) {
  background: none;
  padding: 0;
  border-radius: 0;
}

:deep(ul) {
  margin: 1em 0;
  padding-left: 2em;
}

:deep(li) {
  margin: 0.25em 0;
  list-style-type: disc;
}

:deep(a) {
  color: #3498db;
  text-decoration: none;
}

:deep(a:hover) {
  text-decoration: underline;
}

/* 数学公式样式 */
:deep(.math-display) {
  margin: 1em 0;
  text-align: center;
  overflow-x: auto;
}

:deep(.katex) {
  font-size: inherit;
}

:deep(.katex-display) {
  margin: 1em 0;
  text-align: center;
}

/* 数学公式错误样式 */
:deep(.math-error) {
  background-color: #fee;
  color: #c33;
  padding: 2px 4px;
  border-radius: 3px;
  border: 1px solid #fcc;
  font-family: monospace;
  cursor: help;
}
</style>
