import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

// 系統狀態管理
export const useSystemStore = defineStore('system', () => {
  // 狀態定義
  const isInitialized = ref(false)
  const isLoading = ref(false)
  const systemStatus = ref('offline') // 'running', 'warning', 'offline'
  const currentRoute = ref(null)
  const systemInfo = ref({
    version: '2.0',
    lastUpdated: null,
    overallProgress: 0,
    executionStatus: 'planning'
  })
  
  const diskUsage = ref({})
  const fileList = ref({})
  const notifications = ref([])
  const errors = ref([])
  
  // 計算屬性
  const isSystemHealthy = computed(() => {
    return systemStatus.value === 'running'
  })
  
  const totalDiskSpace = computed(() => {
    return Object.values(diskUsage.value).reduce((total, disk) => {
      return total + (disk.total || 0)
    }, 0)
  })
  
  const totalUsedSpace = computed(() => {
    return Object.values(diskUsage.value).reduce((total, disk) => {
      return total + (disk.used || 0)
    }, 0)
  })
  
  const averageUsagePercent = computed(() => {
    const disks = Object.values(diskUsage.value)
    if (disks.length === 0) return 0
    
    const totalPercent = disks.reduce((sum, disk) => sum + (disk.percent || 0), 0)
    return Math.round(totalPercent / disks.length)
  })
  
  // Actions
  const initializeSystem = async () => {
    if (isInitialized.value) return
    
    isLoading.value = true
    
    try {
      // 並行獲取系統數據
      const [statusResponse, diskResponse, filesResponse] = await Promise.allSettled([
        fetchSystemStatus(),
        fetchDiskUsage(),
        fetchFileList()
      ])
      
      // 處理結果
      if (statusResponse.status === 'fulfilled') {
        systemInfo.value = statusResponse.value
        systemStatus.value = 'running'
      }
      
      if (diskResponse.status === 'fulfilled') {
        diskUsage.value = diskResponse.value
      }
      
      if (filesResponse.status === 'fulfilled') {
        fileList.value = filesResponse.value
      }
      
      isInitialized.value = true
      
      // 添加成功通知
      addNotification({
        type: 'success',
        title: '系統初始化成功',
        message: '磁區規劃管理系統已準備就緒',
        duration: 3000
      })
      
    } catch (error) {
      console.error('系統初始化失敗:', error)
      systemStatus.value = 'offline'
      
      addError({
        type: 'initialization',
        message: '系統初始化失敗',
        error: error.message,
        timestamp: new Date().toISOString()
      })
      
      addNotification({
        type: 'error',
        title: '系統初始化失敗',
        message: '請檢查後端服務是否正常運行',
        duration: 5000
      })
    } finally {
      isLoading.value = false
    }
  }
  
  const fetchSystemStatus = async () => {
    try {
      const response = await axios.get('/api/status')
      return response.data
    } catch (error) {
      throw new Error(`獲取系統狀態失敗: ${error.message}`)
    }
  }
  
  const fetchDiskUsage = async () => {
    try {
      const response = await axios.get('/api/disk-usage')
      if (response.data.success) {
        return response.data.drives
      } else {
        throw new Error(response.data.error || '獲取磁碟信息失敗')
      }
    } catch (error) {
      throw new Error(`獲取磁碟使用情況失敗: ${error.message}`)
    }
  }
  
  const fetchFileList = async () => {
    try {
      const response = await axios.get('/api/files')
      return response.data
    } catch (error) {
      throw new Error(`獲取文件列表失敗: ${error.message}`)
    }
  }
  
  const refreshSystemData = async () => {
    isLoading.value = true
    
    try {
      await Promise.all([
        fetchSystemStatus().then(data => {
          systemInfo.value = data
          systemStatus.value = 'running'
        }),
        fetchDiskUsage().then(data => {
          diskUsage.value = data
        }),
        fetchFileList().then(data => {
          fileList.value = data
        })
      ])
      
      addNotification({
        type: 'success',
        title: '數據刷新成功',
        message: '系統數據已更新到最新狀態',
        duration: 2000
      })
      
    } catch (error) {
      console.error('刷新系統數據失敗:', error)
      systemStatus.value = 'warning'
      
      addNotification({
        type: 'warning',
        title: '數據刷新失敗',
        message: '部分數據可能不是最新的',
        duration: 3000
      })
    } finally {
      isLoading.value = false
    }
  }
  
  const updateProgress = async (progressData) => {
    try {
      const response = await axios.post('/api/progress/update', progressData)
      if (response.data.success) {
        systemInfo.value = { ...systemInfo.value, ...progressData }
        
        addNotification({
          type: 'info',
          title: '進度更新',
          message: '系統進度已更新',
          duration: 2000
        })
      }
    } catch (error) {
      console.error('更新進度失敗:', error)
      addError({
        type: 'progress_update',
        message: '進度更新失敗',
        error: error.message,
        timestamp: new Date().toISOString()
      })
    }
  }
  
  const createBackup = async () => {
    try {
      isLoading.value = true
      const response = await axios.post('/api/backup/create')
      
      if (response.data.success) {
        addNotification({
          type: 'success',
          title: '備份創建成功',
          message: `備份已保存到: ${response.data.backup_path}`,
          duration: 5000
        })
        return response.data
      }
    } catch (error) {
      console.error('創建備份失敗:', error)
      addNotification({
        type: 'error',
        title: '備份創建失敗',
        message: error.response?.data?.error || error.message,
        duration: 5000
      })
      throw error
    } finally {
      isLoading.value = false
    }
  }
  
  const setCurrentRoute = (route) => {
    currentRoute.value = route
  }
  
  const addNotification = (notification) => {
    const id = Date.now() + Math.random()
    const newNotification = {
      id,
      timestamp: new Date().toISOString(),
      ...notification
    }
    
    notifications.value.unshift(newNotification)
    
    // 自動移除通知
    if (notification.duration) {
      setTimeout(() => {
        removeNotification(id)
      }, notification.duration)
    }
    
    // 限制通知數量
    if (notifications.value.length > 10) {
      notifications.value = notifications.value.slice(0, 10)
    }
  }
  
  const removeNotification = (id) => {
    const index = notifications.value.findIndex(n => n.id === id)
    if (index > -1) {
      notifications.value.splice(index, 1)
    }
  }
  
  const clearNotifications = () => {
    notifications.value = []
  }
  
  const addError = (error) => {
    errors.value.unshift({
      id: Date.now() + Math.random(),
      ...error
    })
    
    // 限制錯誤記錄數量
    if (errors.value.length > 50) {
      errors.value = errors.value.slice(0, 50)
    }
  }
  
  const clearErrors = () => {
    errors.value = []
  }
  
  // 返回狀態和方法
  return {
    // 狀態
    isInitialized,
    isLoading,
    systemStatus,
    currentRoute,
    systemInfo,
    diskUsage,
    fileList,
    notifications,
    errors,
    
    // 計算屬性
    isSystemHealthy,
    totalDiskSpace,
    totalUsedSpace,
    averageUsagePercent,
    
    // 方法
    initializeSystem,
    refreshSystemData,
    updateProgress,
    createBackup,
    setCurrentRoute,
    addNotification,
    removeNotification,
    clearNotifications,
    addError,
    clearErrors,
    fetchSystemStatus,
    fetchDiskUsage,
    fetchFileList
  }
})