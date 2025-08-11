<template>
  <div class="disk-monitor">
    <!-- 頁面標題 -->
    <div class="page-header">
      <h1 class="page-title">
        <i class="el-icon-pie-chart"></i>
        磁碟監控
      </h1>
      <p class="page-description">實時監控系統磁碟使用情況，提供詳細的存儲空間分析</p>
    </div>

    <!-- 總覽卡片 -->
    <div class="overview-cards">
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="overview-card total-space" shadow="hover">
            <div class="card-content">
              <div class="card-icon">
                <i class="el-icon-coin"></i>
              </div>
              <div class="card-info">
                <h3>{{ formatBytes(totalSpace) }}</h3>
                <p>總容量</p>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="overview-card used-space" shadow="hover">
            <div class="card-content">
              <div class="card-icon">
                <i class="el-icon-data-analysis"></i>
              </div>
              <div class="card-info">
                <h3>{{ formatBytes(usedSpace) }}</h3>
                <p>已使用</p>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="overview-card free-space" shadow="hover">
            <div class="card-content">
              <div class="card-icon">
                <i class="el-icon-box"></i>
              </div>
              <div class="card-info">
                <h3>{{ formatBytes(freeSpace) }}</h3>
                <p>可用空間</p>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :sm="12" :md="6">
          <el-card class="overview-card usage-percent" shadow="hover">
            <div class="card-content">
              <div class="card-icon">
                <i class="el-icon-pie-chart"></i>
              </div>
              <div class="card-info">
                <h3>{{ averageUsage }}%</h3>
                <p>平均使用率</p>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 磁碟列表 -->
    <div class="disk-list">
      <el-card shadow="hover">
        <template #header>
          <div class="card-header">
            <span>磁碟詳情</span>
            <div class="header-actions">
              <el-button type="text" @click="refreshData">
                <i class="el-icon-refresh"></i>
                刷新
              </el-button>
              <el-button type="text" @click="toggleAutoRefresh">
                <i :class="autoRefresh ? 'el-icon-video-pause' : 'el-icon-video-play'"></i>
                {{ autoRefresh ? '停止' : '開始' }}自動刷新
              </el-button>
            </div>
          </div>
        </template>
        
        <div v-if="isLoading" class="loading-container">
          <el-skeleton :rows="3" animated />
        </div>
        
        <div v-else-if="diskList.length === 0" class="empty-state">
          <i class="el-icon-warning"></i>
          <h3>無法獲取磁碟信息</h3>
          <p>請檢查系統權限或稍後重試</p>
        </div>
        
        <div v-else class="disk-items">
          <div 
            v-for="disk in diskList" 
            :key="disk.drive"
            class="disk-item"
            :class="getDiskStatusClass(disk.percent)"
          >
            <div class="disk-header">
              <div class="disk-info">
                <h4 class="disk-name">
                  <i class="el-icon-coin"></i>
                  {{ disk.drive }} ({{ disk.filesystem }})
                </h4>
                <div class="disk-status">
                  <el-tag 
                    :type="getDiskTagType(disk.percent)" 
                    size="small"
                  >
                    {{ getDiskStatus(disk.percent) }}
                  </el-tag>
                </div>
              </div>
              <div class="disk-usage">
                <span class="usage-text">{{ disk.percent }}%</span>
              </div>
            </div>
            
            <div class="disk-progress">
              <el-progress 
                :percentage="disk.percent" 
                :color="getProgressColor(disk.percent)"
                :stroke-width="12"
                :show-text="false"
              />
            </div>
            
            <div class="disk-details">
              <div class="detail-item">
                <span class="label">總容量:</span>
                <span class="value">{{ formatBytes(disk.total) }}</span>
              </div>
              <div class="detail-item">
                <span class="label">已使用:</span>
                <span class="value">{{ formatBytes(disk.used) }}</span>
              </div>
              <div class="detail-item">
                <span class="label">可用:</span>
                <span class="value">{{ formatBytes(disk.free) }}</span>
              </div>
              <div class="detail-item">
                <span class="label">文件系統:</span>
                <span class="value">{{ disk.filesystem }}</span>
              </div>
            </div>
            
            <!-- 磁碟操作 -->
            <div class="disk-actions">
              <el-button size="small" @click="analyzeDisk(disk)">
                <i class="el-icon-data-analysis"></i>
                分析
              </el-button>
              <el-button size="small" @click="cleanupDisk(disk)" :disabled="disk.percent < 80">
                <i class="el-icon-delete"></i>
                清理
              </el-button>
              <el-button size="small" @click="viewDiskDetails(disk)">
                <i class="el-icon-view"></i>
                詳情
              </el-button>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 磁碟使用趨勢圖表 -->
    <div class="usage-chart">
      <el-card shadow="hover">
        <template #header>
          <div class="card-header">
            <span>使用趨勢</span>
            <el-select v-model="chartTimeRange" @change="updateChart">
              <el-option label="最近1小時" value="1h" />
              <el-option label="最近6小時" value="6h" />
              <el-option label="最近24小時" value="24h" />
              <el-option label="最近7天" value="7d" />
            </el-select>
          </div>
        </template>
        
        <div class="chart-container">
          <canvas ref="usageChart" width="800" height="400"></canvas>
        </div>
      </el-card>
    </div>

    <!-- 磁碟詳情對話框 -->
    <el-dialog v-model="detailDialogVisible" title="磁碟詳情" width="60%">
      <div v-if="selectedDisk" class="disk-detail-content">
        <div class="detail-header">
          <h3>{{ selectedDisk.drive }} 磁碟詳情</h3>
          <el-tag :type="getDiskTagType(selectedDisk.percent)">
            {{ getDiskStatus(selectedDisk.percent) }}
          </el-tag>
        </div>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="detail-section">
              <h4>基本信息</h4>
              <div class="info-list">
                <div class="info-item">
                  <span class="label">磁碟標識:</span>
                  <span class="value">{{ selectedDisk.drive }}</span>
                </div>
                <div class="info-item">
                  <span class="label">文件系統:</span>
                  <span class="value">{{ selectedDisk.filesystem }}</span>
                </div>
                <div class="info-item">
                  <span class="label">總容量:</span>
                  <span class="value">{{ formatBytes(selectedDisk.total) }}</span>
                </div>
                <div class="info-item">
                  <span class="label">已使用:</span>
                  <span class="value">{{ formatBytes(selectedDisk.used) }}</span>
                </div>
                <div class="info-item">
                  <span class="label">可用空間:</span>
                  <span class="value">{{ formatBytes(selectedDisk.free) }}</span>
                </div>
                <div class="info-item">
                  <span class="label">使用率:</span>
                  <span class="value">{{ selectedDisk.percent }}%</span>
                </div>
              </div>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="detail-section">
              <h4>使用情況分布</h4>
              <div class="usage-chart-small">
                <canvas ref="detailChart" width="300" height="300"></canvas>
              </div>
            </div>
          </el-col>
        </el-row>
        
        <div class="detail-actions">
          <el-button type="primary" @click="analyzeDisk(selectedDisk)">
            <i class="el-icon-data-analysis"></i>
            深度分析
          </el-button>
          <el-button @click="cleanupDisk(selectedDisk)" :disabled="selectedDisk.percent < 80">
            <i class="el-icon-delete"></i>
            磁碟清理
          </el-button>
          <el-button @click="exportDiskReport(selectedDisk)">
            <i class="el-icon-download"></i>
            導出報告
          </el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useSystemStore } from '@/stores/system'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Chart, registerables } from 'chart.js'
import { gsap } from 'gsap'
import axios from 'axios'

// 註冊Chart.js組件
Chart.register(...registerables)

const systemStore = useSystemStore()

// 響應式數據
const isLoading = ref(false)
const diskList = ref([])
const autoRefresh = ref(true)
const refreshInterval = ref(null)
const chartTimeRange = ref('24h')
const detailDialogVisible = ref(false)
const selectedDisk = ref(null)

// 圖表引用
const usageChart = ref(null)
const detailChart = ref(null)
let usageChartInstance = null
let detailChartInstance = null

// 計算屬性
const totalSpace = computed(() => {
  return diskList.value.reduce((total, disk) => total + (disk.total || 0), 0)
})

const usedSpace = computed(() => {
  return diskList.value.reduce((total, disk) => total + (disk.used || 0), 0)
})

const freeSpace = computed(() => {
  return diskList.value.reduce((total, disk) => total + (disk.free || 0), 0)
})

const averageUsage = computed(() => {
  if (diskList.value.length === 0) return 0
  const totalPercent = diskList.value.reduce((total, disk) => total + (disk.percent || 0), 0)
  return Math.round(totalPercent / diskList.value.length)
})

// 方法
const loadDiskData = async () => {
  isLoading.value = true
  
  try {
    const response = await axios.get('/api/disk-usage')
    
    if (response.data.success) {
      const drives = response.data.drives || {}
      diskList.value = Object.entries(drives).map(([key, disk]) => ({
        drive: key,
        ...disk
      }))
      
      // 更新系統store
      systemStore.diskUsage = drives
      
      // 添加動畫效果
      await nextTick()
      animateDiskItems()
    } else {
      throw new Error(response.data.error || '獲取磁碟信息失敗')
    }
  } catch (error) {
    console.error('加載磁碟數據失敗:', error)
    ElMessage.error(error.message || '加載磁碟數據失敗')
  } finally {
    isLoading.value = false
  }
}

const refreshData = async () => {
  await loadDiskData()
  updateChart()
  
  systemStore.addNotification({
    type: 'success',
    title: '數據刷新',
    message: '磁碟使用情況已更新',
    duration: 2000
  })
}

const toggleAutoRefresh = () => {
  autoRefresh.value = !autoRefresh.value
  
  if (autoRefresh.value) {
    startAutoRefresh()
    ElMessage.success('已開啟自動刷新')
  } else {
    stopAutoRefresh()
    ElMessage.info('已停止自動刷新')
  }
}

const startAutoRefresh = () => {
  if (refreshInterval.value) return
  
  refreshInterval.value = setInterval(() => {
    if (!isLoading.value) {
      loadDiskData()
    }
  }, 30000) // 30秒刷新一次
}

const stopAutoRefresh = () => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
    refreshInterval.value = null
  }
}

const analyzeDisk = async (disk) => {
  try {
    ElMessage.info('正在分析磁碟...')
    
    // 這裡可以調用後端API進行磁碟分析
    const response = await axios.post('/api/disk/analyze', {
      drive: disk.drive
    })
    
    if (response.data.success) {
      ElMessage.success('磁碟分析完成')
      // 可以顯示分析結果
    } else {
      throw new Error(response.data.error || '磁碟分析失敗')
    }
  } catch (error) {
    console.error('磁碟分析失敗:', error)
    ElMessage.error(error.message || '磁碟分析失敗')
  }
}

const cleanupDisk = async (disk) => {
  try {
    await ElMessageBox.confirm(
      `確定要清理 ${disk.drive} 磁碟嗎？這將刪除臨時文件和回收站內容。`,
      '確認清理',
      {
        confirmButtonText: '確定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    ElMessage.info('正在清理磁碟...')
    
    const response = await axios.post('/api/disk/cleanup', {
      drive: disk.drive
    })
    
    if (response.data.success) {
      ElMessage.success('磁碟清理完成')
      await refreshData()
    } else {
      throw new Error(response.data.error || '磁碟清理失敗')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('磁碟清理失敗:', error)
      ElMessage.error(error.message || '磁碟清理失敗')
    }
  }
}

const viewDiskDetails = (disk) => {
  selectedDisk.value = disk
  detailDialogVisible.value = true
  
  // 延遲初始化詳情圖表
  setTimeout(() => {
    initDetailChart()
  }, 300)
}

const exportDiskReport = async (disk) => {
  try {
    const response = await axios.get('/api/disk/report', {
      params: { drive: disk.drive },
      responseType: 'blob'
    })
    
    // 創建下載鏈接
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `disk_report_${disk.drive.replace(':', '')}.pdf`)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
    
    ElMessage.success('報告導出成功')
  } catch (error) {
    console.error('導出報告失敗:', error)
    ElMessage.error('導出報告失敗')
  }
}

// 工具方法
const formatBytes = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const getDiskStatus = (percent) => {
  if (percent >= 90) return '嚴重'
  if (percent >= 80) return '警告'
  if (percent >= 60) return '注意'
  return '正常'
}

const getDiskTagType = (percent) => {
  if (percent >= 90) return 'danger'
  if (percent >= 80) return 'warning'
  if (percent >= 60) return 'info'
  return 'success'
}

const getDiskStatusClass = (percent) => {
  if (percent >= 90) return 'critical'
  if (percent >= 80) return 'warning'
  if (percent >= 60) return 'caution'
  return 'normal'
}

const getProgressColor = (percent) => {
  if (percent >= 90) return '#F56C6C'
  if (percent >= 80) return '#E6A23C'
  if (percent >= 60) return '#409EFF'
  return '#67C23A'
}

// 圖表相關
const initUsageChart = () => {
  if (!usageChart.value) return
  
  const ctx = usageChart.value.getContext('2d')
  
  // 模擬歷史數據
  const labels = Array.from({length: 24}, (_, i) => `${i}:00`)
  const datasets = diskList.value.map((disk, index) => ({
    label: disk.drive,
    data: Array.from({length: 24}, () => Math.random() * 20 + disk.percent - 10),
    borderColor: getProgressColor(disk.percent),
    backgroundColor: getProgressColor(disk.percent) + '20',
    fill: false,
    tension: 0.4
  }))
  
  usageChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          title: {
            display: true,
            text: '使用率 (%)'
          }
        },
        x: {
          title: {
            display: true,
            text: '時間'
          }
        }
      },
      plugins: {
        legend: {
          position: 'top'
        },
        tooltip: {
          mode: 'index',
          intersect: false
        }
      }
    }
  })
}

const initDetailChart = () => {
  if (!detailChart.value || !selectedDisk.value) return
  
  const ctx = detailChart.value.getContext('2d')
  const disk = selectedDisk.value
  
  if (detailChartInstance) {
    detailChartInstance.destroy()
  }
  
  detailChartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['已使用', '可用空間'],
      datasets: [{
        data: [disk.used, disk.free],
        backgroundColor: [
          getProgressColor(disk.percent),
          '#E4E7ED'
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
              const value = context.parsed
              const total = disk.total
              const percent = ((value / total) * 100).toFixed(1)
              return `${context.label}: ${formatBytes(value)} (${percent}%)`
            }
          }
        }
      }
    }
  })
}

const updateChart = () => {
  if (usageChartInstance) {
    usageChartInstance.destroy()
  }
  initUsageChart()
}

// 動畫效果
const animateDiskItems = () => {
  gsap.fromTo('.disk-item', 
    { x: -50, opacity: 0 },
    { x: 0, opacity: 1, duration: 0.5, stagger: 0.1, ease: 'power2.out' }
  )
  
  gsap.fromTo('.overview-card', 
    { y: -30, opacity: 0 },
    { y: 0, opacity: 1, duration: 0.6, stagger: 0.1, ease: 'back.out(1.7)' }
  )
}

// 生命週期
onMounted(async () => {
  await loadDiskData()
  
  // 初始化圖表
  await nextTick()
  initUsageChart()
  
  // 開始自動刷新
  if (autoRefresh.value) {
    startAutoRefresh()
  }
})

onUnmounted(() => {
  stopAutoRefresh()
  
  // 銷毀圖表實例
  if (usageChartInstance) {
    usageChartInstance.destroy()
  }
  if (detailChartInstance) {
    detailChartInstance.destroy()
  }
})
</script>

<style lang="scss" scoped>
.disk-monitor {
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
  
  .overview-cards {
    margin-bottom: 30px;
    
    .overview-card {
      border: none;
      border-radius: 12px;
      transition: all 0.3s ease;
      
      &:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
      }
      
      &.total-space {
        border-left: 4px solid #409EFF;
      }
      
      &.used-space {
        border-left: 4px solid #E6A23C;
      }
      
      &.free-space {
        border-left: 4px solid #67C23A;
      }
      
      &.usage-percent {
        border-left: 4px solid #F56C6C;
      }
      
      .card-content {
        display: flex;
        align-items: center;
        
        .card-icon {
          font-size: 2.5rem;
          margin-right: 15px;
          color: var(--primary-color);
        }
        
        .card-info {
          flex: 1;
          
          h3 {
            margin: 0 0 5px 0;
            font-size: 1.8rem;
            font-weight: bold;
            color: var(--text-primary);
          }
          
          p {
            margin: 0;
            color: var(--text-secondary);
            font-size: 0.9rem;
          }
        }
      }
    }
  }
  
  .disk-list {
    margin-bottom: 30px;
    
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
    
    .loading-container {
      padding: 20px;
    }
    
    .empty-state {
      text-align: center;
      padding: 60px 20px;
      color: var(--text-secondary);
      
      i {
        font-size: 4rem;
        margin-bottom: 20px;
        opacity: 0.5;
      }
      
      h3 {
        margin-bottom: 10px;
        color: var(--text-primary);
      }
    }
    
    .disk-items {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
      
      @media (max-width: 1200px) {
        grid-template-columns: repeat(2, 1fr);
      }
      
      @media (max-width: 768px) {
        grid-template-columns: 1fr;
      }
      
      .disk-item {
        padding: 20px;
        border: 1px solid var(--border-lighter);
        border-radius: 12px;
        background: white;
        transition: all 0.3s ease;
        display: flex;
        flex-direction: column;
        height: fit-content;
        
        &:hover {
          box-shadow: var(--shadow-light);
          transform: translateY(-2px);
        }
        
        &.normal {
          border-left: 4px solid #67C23A;
        }
        
        &.caution {
          border-left: 4px solid #409EFF;
        }
        
        &.warning {
          border-left: 4px solid #E6A23C;
        }
        
        &.critical {
          border-left: 4px solid #F56C6C;
        }
        
        .disk-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 15px;
          
          .disk-info {
            display: flex;
            align-items: center;
            gap: 15px;
            
            .disk-name {
              margin: 0;
              font-size: 1.2rem;
              color: var(--text-primary);
              
              i {
                color: var(--primary-color);
                margin-right: 8px;
              }
            }
          }
          
          .disk-usage {
            .usage-text {
              font-size: 1.5rem;
              font-weight: bold;
              color: var(--text-primary);
            }
          }
        }
        
        .disk-progress {
          margin-bottom: 15px;
        }
        
        .disk-details {
          display: grid;
          grid-template-columns: 1fr;
          gap: 8px;
          margin-bottom: 15px;
          
          .detail-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid var(--border-extra-light);
            
            .label {
              color: var(--text-secondary);
              font-size: 0.9rem;
            }
            
            .value {
              color: var(--text-primary);
              font-weight: 500;
            }
          }
        }
        
        .disk-actions {
          display: flex;
          gap: 8px;
          justify-content: center;
          margin-top: auto;
          
          .el-button {
            flex: 1;
            font-size: 0.85rem;
          }
        }
      }
    }
  }
  
  .usage-chart {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: bold;
      color: var(--text-primary);
    }
    
    .chart-container {
      height: 400px;
      position: relative;
    }
  }
  
  // 對話框樣式
  .disk-detail-content {
    .detail-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      padding-bottom: 15px;
      border-bottom: 1px solid var(--border-lighter);
      
      h3 {
        margin: 0;
        color: var(--text-primary);
      }
    }
    
    .detail-section {
      margin-bottom: 20px;
      
      h4 {
        margin-bottom: 15px;
        color: var(--text-primary);
        border-bottom: 2px solid var(--primary-color);
        padding-bottom: 5px;
      }
      
      .info-list {
        .info-item {
          display: flex;
          justify-content: space-between;
          padding: 10px 0;
          border-bottom: 1px solid var(--border-extra-light);
          
          &:last-child {
            border-bottom: none;
          }
          
          .label {
            color: var(--text-secondary);
            font-weight: 500;
          }
          
          .value {
            color: var(--text-primary);
            font-weight: 600;
          }
        }
      }
      
      .usage-chart-small {
        height: 300px;
        position: relative;
      }
    }
    
    .detail-actions {
      margin-top: 20px;
      padding-top: 15px;
      border-top: 1px solid var(--border-lighter);
      display: flex;
      gap: 10px;
      justify-content: center;
    }
  }
}

// 響應式設計
@media (max-width: 768px) {
  .disk-monitor {
    padding: 10px;
    
    .disk-items .disk-item {
      .disk-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 10px;
      }
      
      .disk-details {
        grid-template-columns: 1fr;
      }
      
      .disk-actions {
        justify-content: center;
        flex-wrap: wrap;
      }
    }
    
    .usage-chart .card-header {
      flex-direction: column;
      gap: 10px;
    }
  }
}
</style>