<template>
  <div class="dataease-bi">
    <!-- 頁面標題 -->
    <div class="page-header">
      <h1 class="page-title">
        <i class="el-icon-data-board"></i>
        DataEase BI 分析
      </h1>
      <p class="page-description">集成DataEase商業智能平台，提供數據可視化和分析功能</p>
    </div>

    <!-- DataEase狀態卡片 -->
    <div class="status-section">
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="8">
          <el-card class="status-card" shadow="hover">
            <div class="card-content">
              <div class="status-icon" :class="dataEaseStatus">
                <i :class="getStatusIcon(dataEaseStatus)"></i>
              </div>
              <div class="status-info">
                <h3>{{ getStatusText(dataEaseStatus) }}</h3>
                <p>DataEase 服務狀態</p>
                <el-button 
                  v-if="dataEaseStatus === 'offline'"
                  type="primary" 
                  size="small" 
                  @click="startDataEase"
                  :loading="isStarting"
                >
                  啟動服務
                </el-button>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="8">
          <el-card class="status-card" shadow="hover">
            <div class="card-content">
              <div class="status-icon online">
                <i class="el-icon-connection"></i>
              </div>
              <div class="status-info">
                <h3>{{ dataSourceCount }}</h3>
                <p>數據源連接</p>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="8">
          <el-card class="status-card" shadow="hover">
            <div class="card-content">
              <div class="status-icon online">
                <i class="el-icon-data-analysis"></i>
              </div>
              <div class="status-info">
                <h3>{{ dashboardCount }}</h3>
                <p>儀表板數量</p>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 快速訪問 -->
    <div class="quick-access">
      <el-card shadow="hover">
        <template #header>
          <span>快速訪問</span>
        </template>
        <div class="access-grid">
          <div class="access-item" @click="openDataEase">
            <div class="access-icon">
              <i class="el-icon-monitor"></i>
            </div>
            <div class="access-info">
              <h4>DataEase 控制台</h4>
              <p>訪問完整的BI分析平台</p>
            </div>
            <div class="access-action">
              <i class="el-icon-right"></i>
            </div>
          </div>
          
          <div class="access-item" @click="createDashboard">
            <div class="access-icon">
              <i class="el-icon-plus"></i>
            </div>
            <div class="access-info">
              <h4>創建儀表板</h4>
              <p>快速創建新的數據儀表板</p>
            </div>
            <div class="access-action">
              <i class="el-icon-right"></i>
            </div>
          </div>
          
          <div class="access-item" @click="manageDataSources">
            <div class="access-icon">
              <i class="el-icon-connection"></i>
            </div>
            <div class="access-info">
              <h4>數據源管理</h4>
              <p>配置和管理數據連接</p>
            </div>
            <div class="access-action">
              <i class="el-icon-right"></i>
            </div>
          </div>
          
          <div class="access-item" @click="viewReports">
            <div class="access-icon">
              <i class="el-icon-document"></i>
            </div>
            <div class="access-info">
              <h4>報表中心</h4>
              <p>查看和管理所有報表</p>
            </div>
            <div class="access-action">
              <i class="el-icon-right"></i>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 集成配置 -->
    <div class="integration-config">
      <el-card shadow="hover">
        <template #header>
          <div class="card-header">
            <span>集成配置</span>
            <el-button type="text" @click="refreshConfig">
              <i class="el-icon-refresh"></i>
              刷新
            </el-button>
          </div>
        </template>
        
        <div class="config-form">
          <el-form :model="config" label-width="120px">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="服務地址:">
                  <el-input v-model="config.url" placeholder="http://localhost:8081" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="API端口:">
                  <el-input v-model="config.apiPort" placeholder="8081" />
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="用戶名:">
                  <el-input v-model="config.username" placeholder="admin" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="密碼:">
                  <el-input 
                    v-model="config.password" 
                    type="password" 
                    placeholder="請輸入密碼"
                    show-password
                  />
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-form-item label="自動同步:">
              <el-switch 
                v-model="config.autoSync" 
                active-text="開啟" 
                inactive-text="關閉"
              />
              <span class="form-help">自動同步磁區規劃數據到DataEase</span>
            </el-form-item>
            
            <el-form-item label="同步間隔:">
              <el-select v-model="config.syncInterval" :disabled="!config.autoSync">
                <el-option label="5分鐘" :value="5" />
                <el-option label="15分鐘" :value="15" />
                <el-option label="30分鐘" :value="30" />
                <el-option label="1小時" :value="60" />
              </el-select>
            </el-form-item>
            
            <el-form-item>
              <el-button type="primary" @click="saveConfig" :loading="isSaving">
                保存配置
              </el-button>
              <el-button @click="testConnection" :loading="isTesting">
                測試連接
              </el-button>
              <el-button @click="syncData" :loading="isSyncing">
                立即同步
              </el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-card>
    </div>

    <!-- 數據同步狀態 -->
    <div class="sync-status">
      <el-card shadow="hover">
        <template #header>
          <span>數據同步狀態</span>
        </template>
        
        <div class="sync-timeline">
          <el-timeline>
            <el-timeline-item 
              v-for="(item, index) in syncHistory" 
              :key="index"
              :timestamp="formatTime(item.timestamp)"
              :type="getSyncStatusType(item.status)"
            >
              <div class="sync-item">
                <h4>{{ item.title }}</h4>
                <p>{{ item.description }}</p>
                <div v-if="item.details" class="sync-details">
                  <el-tag 
                    v-for="detail in item.details" 
                    :key="detail.key"
                    size="small"
                    :type="detail.type"
                  >
                    {{ detail.label }}: {{ detail.value }}
                  </el-tag>
                </div>
              </div>
            </el-timeline-item>
          </el-timeline>
          
          <div v-if="syncHistory.length === 0" class="empty-sync">
            <i class="el-icon-info"></i>
            <p>暫無同步記錄</p>
          </div>
        </div>
      </el-card>
    </div>

    <!-- DataEase嵌入式儀表板 -->
    <div v-if="dataEaseStatus === 'online'" class="embedded-dashboard">
      <el-card shadow="hover">
        <template #header>
          <div class="card-header">
            <span>磁區規劃儀表板</span>
            <div class="header-actions">
              <el-button type="text" @click="refreshDashboard">
                <i class="el-icon-refresh"></i>
                刷新
              </el-button>
              <el-button type="text" @click="openInNewTab">
                <i class="el-icon-top-right"></i>
                新窗口打開
              </el-button>
            </div>
          </div>
        </template>
        
        <div class="dashboard-container">
          <iframe 
            ref="dashboardFrame"
            :src="dashboardUrl"
            frameborder="0"
            width="100%"
            height="600px"
            @load="onDashboardLoad"
          ></iframe>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useSystemStore } from '@/stores/system'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'
import { gsap } from 'gsap'

const systemStore = useSystemStore()

// 響應式數據
const dataEaseStatus = ref('offline') // 'online', 'offline', 'error'
const dataSourceCount = ref(0)
const dashboardCount = ref(0)
const isStarting = ref(false)
const isSaving = ref(false)
const isTesting = ref(false)
const isSyncing = ref(false)
const syncHistory = ref([])
const dashboardFrame = ref(null)

// 配置數據
const config = ref({
  url: 'http://localhost:8081',
  apiPort: '8081',
  username: 'admin',
  password: '',
  autoSync: false,
  syncInterval: 30
})

// 計算屬性
const dashboardUrl = computed(() => {
  if (dataEaseStatus.value !== 'online') return ''
  return `${config.value.url}/dashboard/磁區規劃概覽`
})

// 方法
const checkDataEaseStatus = async () => {
  try {
    const response = await axios.get('/api/dataease/status')
    
    if (response.data.success) {
      dataEaseStatus.value = response.data.status
      dataSourceCount.value = response.data.dataSources || 0
      dashboardCount.value = response.data.dashboards || 0
    } else {
      dataEaseStatus.value = 'offline'
    }
  } catch (error) {
    console.error('檢查DataEase狀態失敗:', error)
    dataEaseStatus.value = 'error'
  }
}

const startDataEase = async () => {
  isStarting.value = true
  
  try {
    const response = await axios.post('/api/dataease/start')
    
    if (response.data.success) {
      ElMessage.success('DataEase服務啟動成功')
      
      // 等待服務完全啟動
      setTimeout(async () => {
        await checkDataEaseStatus()
      }, 5000)
    } else {
      throw new Error(response.data.error || 'DataEase啟動失敗')
    }
  } catch (error) {
    console.error('啟動DataEase失敗:', error)
    ElMessage.error(error.message || 'DataEase啟動失敗')
  } finally {
    isStarting.value = false
  }
}

const openDataEase = () => {
  if (dataEaseStatus.value === 'online') {
    window.open(config.value.url, '_blank')
  } else {
    ElMessage.warning('DataEase服務未運行，請先啟動服務')
  }
}

const createDashboard = () => {
  if (dataEaseStatus.value === 'online') {
    window.open(`${config.value.url}/dashboard/create`, '_blank')
  } else {
    ElMessage.warning('DataEase服務未運行，請先啟動服務')
  }
}

const manageDataSources = () => {
  if (dataEaseStatus.value === 'online') {
    window.open(`${config.value.url}/datasource`, '_blank')
  } else {
    ElMessage.warning('DataEase服務未運行，請先啟動服務')
  }
}

const viewReports = () => {
  if (dataEaseStatus.value === 'online') {
    window.open(`${config.value.url}/report`, '_blank')
  } else {
    ElMessage.warning('DataEase服務未運行，請先啟動服務')
  }
}

const refreshConfig = async () => {
  try {
    const response = await axios.get('/api/dataease/config')
    
    if (response.data.success) {
      config.value = { ...config.value, ...response.data.config }
      ElMessage.success('配置刷新成功')
    }
  } catch (error) {
    console.error('刷新配置失敗:', error)
    ElMessage.error('刷新配置失敗')
  }
}

const saveConfig = async () => {
  isSaving.value = true
  
  try {
    const response = await axios.post('/api/dataease/config', config.value)
    
    if (response.data.success) {
      ElMessage.success('配置保存成功')
      await checkDataEaseStatus()
    } else {
      throw new Error(response.data.error || '保存配置失敗')
    }
  } catch (error) {
    console.error('保存配置失敗:', error)
    ElMessage.error(error.message || '保存配置失敗')
  } finally {
    isSaving.value = false
  }
}

const testConnection = async () => {
  isTesting.value = true
  
  try {
    const response = await axios.post('/api/dataease/test', {
      url: config.value.url,
      username: config.value.username,
      password: config.value.password
    })
    
    if (response.data.success) {
      ElMessage.success('連接測試成功')
    } else {
      throw new Error(response.data.error || '連接測試失敗')
    }
  } catch (error) {
    console.error('連接測試失敗:', error)
    ElMessage.error(error.message || '連接測試失敗')
  } finally {
    isTesting.value = false
  }
}

const syncData = async () => {
  isSyncing.value = true
  
  try {
    const response = await axios.post('/api/dataease/sync')
    
    if (response.data.success) {
      ElMessage.success('數據同步成功')
      
      // 添加同步記錄
      syncHistory.value.unshift({
        timestamp: new Date().toISOString(),
        status: 'success',
        title: '手動數據同步',
        description: '磁區規劃數據已成功同步到DataEase',
        details: [
          { key: 'files', label: '文件數量', value: response.data.syncedFiles || 0, type: 'info' },
          { key: 'size', label: '數據大小', value: formatBytes(response.data.syncedSize || 0), type: 'info' }
        ]
      })
      
      await loadSyncHistory()
    } else {
      throw new Error(response.data.error || '數據同步失敗')
    }
  } catch (error) {
    console.error('數據同步失敗:', error)
    ElMessage.error(error.message || '數據同步失敗')
    
    // 添加失敗記錄
    syncHistory.value.unshift({
      timestamp: new Date().toISOString(),
      status: 'error',
      title: '數據同步失敗',
      description: error.message || '同步過程中發生錯誤'
    })
  } finally {
    isSyncing.value = false
  }
}

const loadSyncHistory = async () => {
  try {
    const response = await axios.get('/api/dataease/sync-history')
    
    if (response.data.success) {
      syncHistory.value = response.data.history || []
    }
  } catch (error) {
    console.error('加載同步歷史失敗:', error)
  }
}

const refreshDashboard = () => {
  if (dashboardFrame.value) {
    dashboardFrame.value.src = dashboardFrame.value.src
  }
}

const openInNewTab = () => {
  if (dashboardUrl.value) {
    window.open(dashboardUrl.value, '_blank')
  }
}

const onDashboardLoad = () => {
  console.log('儀表板加載完成')
}

// 工具方法
const getStatusIcon = (status) => {
  const icons = {
    online: 'el-icon-success',
    offline: 'el-icon-error',
    error: 'el-icon-warning'
  }
  return icons[status] || 'el-icon-info'
}

const getStatusText = (status) => {
  const texts = {
    online: '在線',
    offline: '離線',
    error: '錯誤'
  }
  return texts[status] || '未知'
}

const getSyncStatusType = (status) => {
  const types = {
    success: 'success',
    error: 'danger',
    warning: 'warning',
    info: 'info'
  }
  return types[status] || 'info'
}

const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleString('zh-TW')
}

const formatBytes = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 動畫效果
const animateCards = () => {
  gsap.fromTo('.status-card', 
    { y: 30, opacity: 0 },
    { y: 0, opacity: 1, duration: 0.6, stagger: 0.1, ease: 'power2.out' }
  )
  
  gsap.fromTo('.access-item', 
    { x: -30, opacity: 0 },
    { x: 0, opacity: 1, duration: 0.5, stagger: 0.1, ease: 'power2.out', delay: 0.3 }
  )
}

// 生命週期
onMounted(async () => {
  await checkDataEaseStatus()
  await loadSyncHistory()
  
  // 啟動動畫
  animateCards()
  
  // 定期檢查狀態
  const statusInterval = setInterval(() => {
    checkDataEaseStatus()
  }, 30000) // 30秒檢查一次
  
  // 清理定時器
  onUnmounted(() => {
    clearInterval(statusInterval)
  })
})
</script>

<style lang="scss" scoped>
.dataease-bi {
  padding: 20px;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  
  .page-header {
    margin-bottom: 30px;
    
    .page-title {
      font-size: 2rem;
      color: var(--text-primary);
      margin-bottom: 8px;
      
      i {
        color: var(--primary-color);
        margin-right: 10px;
      }
    }
    
    .page-description {
      color: var(--text-secondary);
      font-size: 1rem;
    }
  }
  
  .status-section {
    margin-bottom: 30px;
    
    .status-card {
      border: none;
      border-radius: 12px;
      transition: all 0.3s ease;
      
      &:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
      }
      
      .card-content {
        display: flex;
        align-items: center;
        
        .status-icon {
          font-size: 2.5rem;
          margin-right: 15px;
          border-radius: 50%;
          width: 60px;
          height: 60px;
          display: flex;
          align-items: center;
          justify-content: center;
          
          &.online {
            background: rgba(103, 194, 58, 0.1);
            color: #67C23A;
          }
          
          &.offline {
            background: rgba(245, 108, 108, 0.1);
            color: #F56C6C;
          }
          
          &.error {
            background: rgba(230, 162, 60, 0.1);
            color: #E6A23C;
          }
        }
        
        .status-info {
          flex: 1;
          
          h3 {
            margin: 0 0 5px 0;
            font-size: 1.8rem;
            font-weight: bold;
            color: var(--text-primary);
          }
          
          p {
            margin: 0 0 10px 0;
            color: var(--text-secondary);
            font-size: 0.9rem;
          }
        }
      }
    }
  }
  
  .quick-access {
    margin-bottom: 30px;
    
    .access-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 15px;
      
      .access-item {
        display: flex;
        align-items: center;
        padding: 20px;
        border: 1px solid var(--border-lighter);
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        
        &:hover {
          border-color: var(--primary-color);
          background: rgba(64, 158, 255, 0.05);
          transform: translateY(-2px);
        }
        
        .access-icon {
          font-size: 2rem;
          color: var(--primary-color);
          margin-right: 15px;
        }
        
        .access-info {
          flex: 1;
          
          h4 {
            margin: 0 0 5px 0;
            color: var(--text-primary);
          }
          
          p {
            margin: 0;
            color: var(--text-secondary);
            font-size: 0.9rem;
          }
        }
        
        .access-action {
          color: var(--text-placeholder);
          font-size: 1.2rem;
        }
      }
    }
  }
  
  .integration-config {
    margin-bottom: 30px;
    
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: bold;
      color: var(--text-primary);
    }
    
    .config-form {
      .form-help {
        margin-left: 10px;
        color: var(--text-secondary);
        font-size: 0.8rem;
      }
    }
  }
  
  .sync-status {
    margin-bottom: 30px;
    
    .sync-timeline {
      max-height: 400px;
      overflow-y: auto;
      
      .sync-item {
        h4 {
          margin: 0 0 5px 0;
          color: var(--text-primary);
        }
        
        p {
          margin: 0 0 10px 0;
          color: var(--text-secondary);
          font-size: 0.9rem;
        }
        
        .sync-details {
          display: flex;
          gap: 8px;
          flex-wrap: wrap;
        }
      }
      
      .empty-sync {
        text-align: center;
        padding: 40px 20px;
        color: var(--text-secondary);
        
        i {
          font-size: 3rem;
          margin-bottom: 10px;
          display: block;
        }
      }
    }
  }
  
  .embedded-dashboard {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: bold;
      color: var(--text-primary);
      
      .header-actions {
        display: flex;
        gap: 10px;
      }
    }
    
    .dashboard-container {
      border-radius: 8px;
      overflow: hidden;
      border: 1px solid var(--border-lighter);
      
      iframe {
        display: block;
        width: 100%;
        min-height: 600px;
      }
    }
  }
}

// 響應式設計
@media (max-width: 768px) {
  .dataease-bi {
    padding: 10px;
    
    .access-grid {
      grid-template-columns: 1fr !important;
    }
    
    .config-form {
      :deep(.el-row) {
        .el-col {
          width: 100% !important;
          margin-bottom: 15px;
        }
      }
    }
    
    .embedded-dashboard {
      .dashboard-container iframe {
        min-height: 400px;
      }
    }
  }
}
</style>