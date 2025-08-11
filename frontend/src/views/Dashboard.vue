<template>
  <div class="dashboard">
    <!-- 系統狀態卡片 -->
    <div class="status-cards">
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="6" v-for="card in statusCards" :key="card.title">
          <el-card class="status-card" :class="card.type" shadow="hover">
            <div class="card-content">
              <div class="card-icon">
                <i :class="card.icon"></i>
              </div>
              <div class="card-info">
                <h3>{{ card.value }}</h3>
                <p>{{ card.title }}</p>
                <span class="card-trend" :class="card.trend">
                  <i :class="card.trendIcon"></i>
                  {{ card.trendText }}
                </span>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 圖表區域 -->
    <div class="charts-section">
      <el-row :gutter="20">
        <!-- 磁碟使用情況圖表 -->
        <el-col :xs="24" :lg="12">
          <el-card class="chart-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <span>磁碟使用情況</span>
                <el-button type="text" @click="refreshDiskData">
                  <i class="el-icon-refresh"></i>
                </el-button>
              </div>
            </template>
            <div class="chart-container">
              <canvas ref="diskChart" width="400" height="300"></canvas>
            </div>
          </el-card>
        </el-col>

        <!-- 系統性能監控 -->
        <el-col :xs="24" :lg="12">
          <el-card class="chart-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <span>系統性能趨勢</span>
                <el-button type="text" @click="refreshPerformanceData">
                  <i class="el-icon-refresh"></i>
                </el-button>
              </div>
            </template>
            <div class="chart-container">
              <canvas ref="performanceChart" width="400" height="300"></canvas>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 快速操作區域 -->
    <div class="quick-actions">
      <el-card class="actions-card" shadow="hover">
        <template #header>
          <span>快速操作</span>
        </template>
        <div class="actions-grid">
          <div 
            v-for="action in quickActions" 
            :key="action.name"
            class="action-item"
            :class="{ disabled: action.disabled }"
            @click="handleQuickAction(action)"
          >
            <div class="action-icon">
              <i :class="action.icon"></i>
            </div>
            <div class="action-info">
              <h4>{{ action.name }}</h4>
              <p>{{ action.description }}</p>
            </div>
            <div class="action-status" v-if="action.status">
              <el-tag :type="action.statusType" size="small">{{ action.status }}</el-tag>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 最近活動 -->
    <div class="recent-activities">
      <el-card class="activities-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span>最近活動</span>
            <el-button type="text" @click="clearActivities">
              <i class="el-icon-delete"></i> 清空
            </el-button>
          </div>
        </template>
        <div class="activities-list">
          <div 
            v-for="activity in recentActivities" 
            :key="activity.id"
            class="activity-item"
            :class="activity.type"
          >
            <div class="activity-icon">
              <i :class="activity.icon"></i>
            </div>
            <div class="activity-content">
              <h5>{{ activity.title }}</h5>
              <p>{{ activity.description }}</p>
              <span class="activity-time">{{ formatTime(activity.timestamp) }}</span>
            </div>
          </div>
          <div v-if="recentActivities.length === 0" class="no-activities">
            <i class="el-icon-info"></i>
            <p>暫無活動記錄</p>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useSystemStore } from '@/stores/system'
import { Chart, registerables } from 'chart.js'
import { ElMessage, ElMessageBox } from 'element-plus'
import { gsap } from 'gsap'

// 註冊Chart.js組件
Chart.register(...registerables)

const router = useRouter()
const systemStore = useSystemStore()

// 圖表引用
const diskChart = ref(null)
const performanceChart = ref(null)
let diskChartInstance = null
let performanceChartInstance = null

// 定時器
let refreshTimer = null

// 狀態卡片數據
const statusCards = computed(() => [
  {
    title: '系統狀態',
    value: systemStore.systemStatus === 'running' ? '正常運行' : 
           systemStore.systemStatus === 'warning' ? '警告' : '離線',
    icon: 'el-icon-monitor',
    type: systemStore.systemStatus,
    trend: 'up',
    trendIcon: 'el-icon-top',
    trendText: '穩定'
  },
  {
    title: '磁碟使用率',
    value: `${systemStore.averageUsagePercent}%`,
    icon: 'el-icon-pie-chart',
    type: systemStore.averageUsagePercent > 80 ? 'warning' : 'running',
    trend: systemStore.averageUsagePercent > 70 ? 'up' : 'down',
    trendIcon: systemStore.averageUsagePercent > 70 ? 'el-icon-top' : 'el-icon-bottom',
    trendText: systemStore.averageUsagePercent > 70 ? '偏高' : '正常'
  },
  {
    title: '總容量',
    value: formatBytes(systemStore.totalDiskSpace),
    icon: 'el-icon-coin',
    type: 'running',
    trend: 'stable',
    trendIcon: 'el-icon-minus',
    trendText: '穩定'
  },
  {
    title: '已使用',
    value: formatBytes(systemStore.totalUsedSpace),
    icon: 'el-icon-data-analysis',
    type: 'running',
    trend: 'up',
    trendIcon: 'el-icon-top',
    trendText: '增長中'
  }
])

// 快速操作
const quickActions = ref([
  {
    name: '文件管理',
    description: '管理磁區規劃文件',
    icon: 'el-icon-folder',
    route: '/files',
    disabled: false,
    status: '可用',
    statusType: 'success'
  },
  {
    name: '磁碟監控',
    description: '查看磁碟使用情況',
    icon: 'el-icon-pie-chart',
    route: '/disk',
    disabled: false,
    status: '實時',
    statusType: 'info'
  },
  {
    name: 'BI分析',
    description: 'DataEase商業智能',
    icon: 'el-icon-data-board',
    route: '/dataease',
    disabled: false,
    status: '集成',
    statusType: 'warning'
  },
  {
    name: '系統設置',
    description: '配置系統參數',
    icon: 'el-icon-setting',
    route: '/settings',
    disabled: false,
    status: '配置',
    statusType: 'info'
  },
  {
    name: '創建備份',
    description: '備份系統數據',
    icon: 'el-icon-download',
    action: 'backup',
    disabled: systemStore.isLoading,
    status: systemStore.isLoading ? '處理中' : '就緒',
    statusType: systemStore.isLoading ? 'warning' : 'success'
  },
  {
    name: '刷新數據',
    description: '更新系統信息',
    icon: 'el-icon-refresh',
    action: 'refresh',
    disabled: systemStore.isLoading,
    status: systemStore.isLoading ? '刷新中' : '就緒',
    statusType: systemStore.isLoading ? 'warning' : 'success'
  }
])

// 最近活動
const recentActivities = computed(() => {
  return systemStore.notifications.slice(0, 5).map(notification => ({
    id: notification.id,
    title: notification.title,
    description: notification.message,
    timestamp: notification.timestamp,
    type: notification.type,
    icon: getActivityIcon(notification.type)
  }))
})

// 工具函數
const formatBytes = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now - date
  
  if (diff < 60000) return '剛剛'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分鐘前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小時前`
  return date.toLocaleDateString('zh-TW')
}

const getActivityIcon = (type) => {
  const icons = {
    success: 'el-icon-success',
    error: 'el-icon-error',
    warning: 'el-icon-warning',
    info: 'el-icon-info'
  }
  return icons[type] || 'el-icon-info'
}

// 事件處理
const handleQuickAction = async (action) => {
  if (action.disabled) return
  
  if (action.route) {
    router.push(action.route)
  } else if (action.action === 'backup') {
    try {
      await ElMessageBox.confirm('確定要創建系統備份嗎？', '確認操作', {
        confirmButtonText: '確定',
        cancelButtonText: '取消',
        type: 'info'
      })
      
      await systemStore.createBackup()
    } catch (error) {
      if (error !== 'cancel') {
        ElMessage.error('備份操作失敗')
      }
    }
  } else if (action.action === 'refresh') {
    await systemStore.refreshSystemData()
    await refreshCharts()
  }
}

const refreshDiskData = async () => {
  await systemStore.fetchDiskUsage()
  updateDiskChart()
}

const refreshPerformanceData = async () => {
  // 這裡可以添加性能數據獲取邏輯
  updatePerformanceChart()
}

const clearActivities = () => {
  systemStore.clearNotifications()
}

// 圖表相關
const initDiskChart = () => {
  if (!diskChart.value) return
  
  const ctx = diskChart.value.getContext('2d')
  const diskData = Object.values(systemStore.diskUsage)
  
  diskChartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: diskData.map(disk => disk.drive || 'Unknown'),
      datasets: [{
        data: diskData.map(disk => disk.used || 0),
        backgroundColor: [
          '#409EFF',
          '#67C23A',
          '#E6A23C',
          '#F56C6C',
          '#909399'
        ],
        borderWidth: 2,
        borderColor: '#fff'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom'
        },
        tooltip: {
          callbacks: {
            label: (context) => {
              const disk = diskData[context.dataIndex]
              return `${context.label}: ${formatBytes(disk.used)} / ${formatBytes(disk.total)} (${disk.percent}%)`
            }
          }
        }
      }
    }
  })
}

const initPerformanceChart = () => {
  if (!performanceChart.value) return
  
  const ctx = performanceChart.value.getContext('2d')
  
  // 模擬性能數據
  const labels = Array.from({length: 24}, (_, i) => `${i}:00`)
  const data = Array.from({length: 24}, () => Math.random() * 100)
  
  performanceChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: 'CPU使用率 (%)',
        data,
        borderColor: '#409EFF',
        backgroundColor: 'rgba(64, 158, 255, 0.1)',
        fill: true,
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          max: 100
        }
      },
      plugins: {
        legend: {
          position: 'top'
        }
      }
    }
  })
}

const updateDiskChart = () => {
  if (!diskChartInstance) return
  
  const diskData = Object.values(systemStore.diskUsage)
  diskChartInstance.data.labels = diskData.map(disk => disk.drive || 'Unknown')
  diskChartInstance.data.datasets[0].data = diskData.map(disk => disk.used || 0)
  diskChartInstance.update()
}

const updatePerformanceChart = () => {
  if (!performanceChartInstance) return
  
  // 更新性能數據（這裡使用模擬數據）
  const newData = Array.from({length: 24}, () => Math.random() * 100)
  performanceChartInstance.data.datasets[0].data = newData
  performanceChartInstance.update()
}

const refreshCharts = async () => {
  updateDiskChart()
  updatePerformanceChart()
}

// 動畫效果
const animateCards = () => {
  gsap.fromTo('.status-card', 
    { y: 50, opacity: 0 },
    { y: 0, opacity: 1, duration: 0.6, stagger: 0.1, ease: 'power2.out' }
  )
  
  gsap.fromTo('.chart-card', 
    { scale: 0.9, opacity: 0 },
    { scale: 1, opacity: 1, duration: 0.8, delay: 0.3, stagger: 0.2, ease: 'back.out(1.7)' }
  )
  
  gsap.fromTo('.actions-card', 
    { x: -50, opacity: 0 },
    { x: 0, opacity: 1, duration: 0.7, delay: 0.5, ease: 'power2.out' }
  )
  
  gsap.fromTo('.activities-card', 
    { x: 50, opacity: 0 },
    { x: 0, opacity: 1, duration: 0.7, delay: 0.6, ease: 'power2.out' }
  )
}

// 生命週期
onMounted(async () => {
  // 初始化系統
  if (!systemStore.isInitialized) {
    await systemStore.initializeSystem()
  }
  
  // 等待DOM更新後初始化圖表
  await nextTick()
  initDiskChart()
  initPerformanceChart()
  
  // 啟動動畫
  animateCards()
  
  // 設置定時刷新
  refreshTimer = setInterval(() => {
    if (!systemStore.isLoading) {
      systemStore.refreshSystemData()
      refreshCharts()
    }
  }, 30000) // 30秒刷新一次
})

onUnmounted(() => {
  // 清理定時器
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
  
  // 銷毀圖表實例
  if (diskChartInstance) {
    diskChartInstance.destroy()
  }
  if (performanceChartInstance) {
    performanceChartInstance.destroy()
  }
})
</script>

<style lang="scss" scoped>
.dashboard {
  padding: 20px;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  
  .status-cards {
    margin-bottom: 30px;
    
    .status-card {
      border: none;
      border-radius: 12px;
      transition: all 0.3s ease;
      
      &:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
      }
      
      &.running {
        border-left: 4px solid #67C23A;
      }
      
      &.warning {
        border-left: 4px solid #E6A23C;
      }
      
      &.offline {
        border-left: 4px solid #F56C6C;
      }
      
      .card-content {
        display: flex;
        align-items: center;
        
        .card-icon {
          font-size: 2.5rem;
          margin-right: 15px;
          color: #409EFF;
        }
        
        .card-info {
          flex: 1;
          
          h3 {
            margin: 0 0 5px 0;
            font-size: 1.8rem;
            font-weight: bold;
            color: #303133;
          }
          
          p {
            margin: 0 0 8px 0;
            color: #606266;
            font-size: 0.9rem;
          }
          
          .card-trend {
            font-size: 0.8rem;
            
            &.up {
              color: #F56C6C;
            }
            
            &.down {
              color: #67C23A;
            }
            
            &.stable {
              color: #909399;
            }
          }
        }
      }
    }
  }
  
  .charts-section {
    margin-bottom: 30px;
    
    .chart-card {
      border: none;
      border-radius: 12px;
      
      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: bold;
        color: #303133;
      }
      
      .chart-container {
        height: 300px;
        position: relative;
      }
    }
  }
  
  .quick-actions {
    margin-bottom: 30px;
    
    .actions-card {
      border: none;
      border-radius: 12px;
      
      .actions-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 15px;
        
        .action-item {
          display: flex;
          align-items: center;
          padding: 15px;
          border: 1px solid #EBEEF5;
          border-radius: 8px;
          cursor: pointer;
          transition: all 0.3s ease;
          
          &:hover:not(.disabled) {
            border-color: #409EFF;
            background: #f0f9ff;
            transform: translateY(-2px);
          }
          
          &.disabled {
            opacity: 0.5;
            cursor: not-allowed;
          }
          
          .action-icon {
            font-size: 2rem;
            margin-right: 15px;
            color: #409EFF;
          }
          
          .action-info {
            flex: 1;
            
            h4 {
              margin: 0 0 5px 0;
              color: #303133;
            }
            
            p {
              margin: 0;
              color: #606266;
              font-size: 0.9rem;
            }
          }
          
          .action-status {
            margin-left: 10px;
          }
        }
      }
    }
  }
  
  .recent-activities {
    .activities-card {
      border: none;
      border-radius: 12px;
      
      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: bold;
        color: #303133;
      }
      
      .activities-list {
        max-height: 400px;
        overflow-y: auto;
        
        .activity-item {
          display: flex;
          align-items: flex-start;
          padding: 15px 0;
          border-bottom: 1px solid #F2F6FC;
          
          &:last-child {
            border-bottom: none;
          }
          
          .activity-icon {
            font-size: 1.2rem;
            margin-right: 12px;
            margin-top: 2px;
            
            &.success { color: #67C23A; }
            &.error { color: #F56C6C; }
            &.warning { color: #E6A23C; }
            &.info { color: #409EFF; }
          }
          
          .activity-content {
            flex: 1;
            
            h5 {
              margin: 0 0 5px 0;
              color: #303133;
              font-size: 0.95rem;
            }
            
            p {
              margin: 0 0 5px 0;
              color: #606266;
              font-size: 0.85rem;
              line-height: 1.4;
            }
            
            .activity-time {
              color: #C0C4CC;
              font-size: 0.8rem;
            }
          }
        }
        
        .no-activities {
          text-align: center;
          padding: 40px 20px;
          color: #C0C4CC;
          
          i {
            font-size: 3rem;
            margin-bottom: 10px;
            display: block;
          }
        }
      }
    }
  }
}

// 響應式設計
@media (max-width: 768px) {
  .dashboard {
    padding: 10px;
    
    .actions-grid {
      grid-template-columns: 1fr !important;
    }
  }
}
</style>