<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 顶部导航 -->
    <header class="bg-white shadow-sm border-b">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center">
            <h1 class="text-2xl font-bold text-gray-900">PrintMind</h1>
            <span class="ml-2 text-sm text-gray-500">智能排版工具</span>
          </div>
          <div class="flex items-center space-x-4">
            <router-link to="/" class="btn-secondary">返回首页</router-link>
          </div>
        </div>
      </div>
    </header>

    <!-- 关于内容 -->
    <main class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="card p-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-6">关于 PrintMind</h1>

        <div class="prose prose-lg max-w-none">
          <p class="text-lg text-gray-600 mb-6">
            PrintMind 是一款智能排版工具，专为现代文档处理而设计。它结合了先进的AI技术和专业的排版功能，为用户提供高质量的文档排版体验。
          </p>

          <h2 class="text-2xl font-semibold text-gray-900 mb-4">主要功能</h2>
          <ul class="space-y-2 mb-6">
            <li class="flex items-start">
              <span class="text-blue-500 mr-2">•</span>
              <span>支持 Markdown、Word、文本文件的导入和处理</span>
            </li>
            <li class="flex items-start">
              <span class="text-blue-500 mr-2">•</span>
              <span>智能图片处理和嵌入功能</span>
            </li>
            <li class="flex items-start">
              <span class="text-blue-500 mr-2">•</span>
              <span>专业级PDF生成和排版</span>
            </li>
            <li class="flex items-start">
              <span class="text-blue-500 mr-2">•</span>
              <span>AI驱动的排版优化建议</span>
            </li>
            <li class="flex items-start">
              <span class="text-blue-500 mr-2">•</span>
              <span>实时预览和编辑功能</span>
            </li>
          </ul>

          <h2 class="text-2xl font-semibold text-gray-900 mb-4">技术栈</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <h3 class="text-lg font-medium text-gray-900 mb-2">前端技术</h3>
              <ul class="space-y-1 text-gray-600">
                <li>Vue 3 + TypeScript</li>
                <li>Tailwind CSS</li>
                <li>Vite 构建工具</li>
              </ul>
            </div>
            <div>
              <h3 class="text-lg font-medium text-gray-900 mb-2">后端技术</h3>
              <ul class="space-y-1 text-gray-600">
                <li>FastAPI + Python</li>
                <li>ReportLab PDF生成</li>
                <li>DeepSeek AI集成</li>
              </ul>
            </div>
          </div>

          <h2 class="text-2xl font-semibold text-gray-900 mb-4">版本信息</h2>
          <p class="text-gray-600">
            当前版本：v1.0.0<br>
            最后更新：2024年12月6日
          </p>
        </div>
      </div>
    </main>
  </div>
</template>
