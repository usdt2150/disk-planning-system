import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'

// 樣式導入
import 'element-plus/dist/index.css'
import 'animate.css'
import './styles/main.scss'

// 創建應用實例
const app = createApp(App)

// 使用插件
app.use(createPinia())
app.use(router)

// 全局配置
app.config.globalProperties.$apiBase = '/api'

// 掛載應用
app.mount('#app')

// 開發環境日誌
if (import.meta.env.DEV) {
  console.log('🚀 磁區規劃管理系統 - 前端應用已啟動')
  console.log('📊 Vue版本:', app.version)
  console.log('🌐 API基礎路徑:', '/api')
}