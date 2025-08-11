import { createRouter, createWebHistory } from 'vue-router'
import { useSystemStore } from '@/stores/system'

// 路由組件懶加載
const Dashboard = () => import('@/views/Dashboard.vue')
const FileManager = () => import('@/views/FileManager.vue')
const DiskMonitor = () => import('@/views/DiskMonitor.vue')
const DataEaseBI = () => import('@/views/DataEaseBI.vue')
const SystemSettings = () => import('@/views/SystemSettings.vue')
const NotFound = () => import('@/views/NotFound.vue')

// 路由配置
const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard,
    meta: {
      title: '儀表板',
      icon: 'el-icon-data-analysis',
      description: '系統概覽和關鍵指標監控',
      requiresAuth: false
    }
  },
  {
    path: '/files',
    name: 'FileManager',
    component: FileManager,
    meta: {
      title: '文件管理',
      icon: 'el-icon-folder',
      description: '磁區規劃文件的管理和編輯',
      requiresAuth: false
    }
  },
  {
    path: '/disk',
    name: 'DiskMonitor',
    component: DiskMonitor,
    meta: {
      title: '磁碟監控',
      icon: 'el-icon-pie-chart',
      description: '實時磁碟使用情況監控',
      requiresAuth: false
    }
  },
  {
    path: '/dataease',
    name: 'DataEaseBI',
    component: DataEaseBI,
    meta: {
      title: 'BI分析',
      icon: 'el-icon-data-board',
      description: 'DataEase商業智能分析平台',
      requiresAuth: false
    }
  },
  {
    path: '/settings',
    name: 'SystemSettings',
    component: SystemSettings,
    meta: {
      title: '系統設置',
      icon: 'el-icon-setting',
      description: '系統配置和參數設置',
      requiresAuth: false
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
    meta: {
      title: '頁面未找到',
      hidden: true
    }
  }
]

// 創建路由實例
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // 路由切換時的滾動行為
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0, behavior: 'smooth' }
    }
  }
})

// 全局前置守衛
router.beforeEach(async (to, from, next) => {
  const systemStore = useSystemStore()
  
  // 設置頁面標題
  if (to.meta.title) {
    document.title = `${to.meta.title} - 磁區規劃管理系統`
  } else {
    document.title = '磁區規劃管理系統'
  }
  
  // 檢查系統狀態
  if (!systemStore.isInitialized) {
    try {
      await systemStore.initializeSystem()
    } catch (error) {
      console.warn('系統初始化警告:', error)
    }
  }
  
  // 路由權限檢查（目前所有路由都開放）
  if (to.meta.requiresAuth) {
    // 這裡可以添加身份驗證邏輯
    // 目前系統不需要登入，所以直接通過
  }
  
  // 記錄路由跳轉（開發環境）
  if (import.meta.env.DEV) {
    console.log(`🚀 路由跳轉: ${from.path} → ${to.path}`)
  }
  
  next()
})

// 全局後置鉤子
router.afterEach((to, from) => {
  // 路由跳轉完成後的處理
  const systemStore = useSystemStore()
  
  // 更新當前路由信息
  systemStore.setCurrentRoute({
    path: to.path,
    name: to.name,
    meta: to.meta
  })
  
  // 頁面訪問統計（可選）
  if (import.meta.env.PROD) {
    // 這裡可以添加頁面訪問統計邏輯
  }
})

// 路由錯誤處理
router.onError((error) => {
  console.error('路由錯誤:', error)
  
  // 可以在這裡添加錯誤上報邏輯
  if (import.meta.env.PROD) {
    // 生產環境錯誤上報
  }
})

export default router

// 導出路由配置供其他組件使用
export { routes }