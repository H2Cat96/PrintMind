import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    host: '0.0.0.0', // 允许外部访问
    port: 5176,
    allowedHosts: true, // 禁用主机检查
    proxy: {
      '/api': {
        target: process.env.VITE_API_BASE_URL || 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      }
    }
  },
  build: {
    outDir: 'dist',
    sourcemap: false,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'vue-router'],
        }
      }
    }
  },
  base: './',
  define: {
    __VUE_PROD_DEVTOOLS__: false,
  }
})
