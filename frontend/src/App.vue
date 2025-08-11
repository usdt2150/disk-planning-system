<template>
  <div id="app" class="app-container">
    <!-- 加載動畫 -->
    <Transition name="fade" appear>
      <div v-if="!isLoading" class="main-content">
        <!-- 頂部導航 -->
        <header class="app-header">
          <div class="header-content">
            <div class="logo-section">
              <div class="logo-icon animate__animated animate__bounceIn">
                <i class="el-icon-folder"></i>
              </div>
              <h1 class="app-title animate__animated animate__fadeInLeft">
                磁區規劃管理系統
              </h1>
            </div>
            <nav class="nav-menu">
              <router-link 
                v-for="route in navRoutes" 
                :key="route.path"
                :to="route.path"
                class="nav-item"
                :class="{ active: $route.path === route.path }"
              >
                <i :class="route.icon"></i>
                <span>{{ route.name }}</span>
              </router-link>
            </nav>
          </div>
        </header>

        <!-- 主要內容區域 -->
        <main class="app-main">
          <router-view v-slot="{ Component, route }">
            <Transition 
              :name="getTransitionName(route)"
              mode="out-in"
              appear
            >
              <component :is="Component" :key="route.path" />
            </Transition>
          </router-view>
        </main>

        <!-- 底部信息 -->
        <footer class="app-footer">
          <div class="footer-content">
            <div class="system-info">
              <span class="version">v2.0</span>
              <span class="separator">|</span>
              <span class="status" :class="systemStatus.class">
                {{ systemStatus.text }}
              </span>
            </div>
            <div class="copyright">
              © 2024 磁區規劃管理系統 - 現代化數據管理解決方案
            </div>
          </div>
        </footer>
      </div>
    </Transition>

    <!-- 全局加載遮罩 -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-content">
        <div class="loading-spinner"></div>
        <h2 class="loading-text animate__animated animate__pulse animate__infinite">
          正在載入系統...
        </h2>
        <p class="loading-subtitle">請稍候，正在初始化數據管理界面</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useSystemStore } from '@/stores/system'

const router = useRouter()
const route = useRoute()
const systemStore = useSystemStore()

// 響應式數據
const isLoading = ref(true)

// 導航路由配置
const navRoutes = [
  { path: '/', name: '儀表板', icon: 'el-icon-data-analysis' },
  { path: '/files', name: '文件管理', icon: 'el-icon-folder' },
  { path: '/disk', name: '磁碟監控', icon: 'el-icon-pie-chart' },
  { path: '/dataease', name: 'BI分析', icon: 'el-icon-data-board' },
  { path: '/settings', name: '系統設置', icon: 'el-icon-setting' }
]

// 計算屬性
const systemStatus = computed(() => {
  const status = systemStore.systemStatus
  if (status === 'running') {
    return { text: '系統運行中', class: 'status-running' }
  } else if (status === 'warning') {
    return { text: '系統警告', class: 'status-warning' }
  } else {
    return { text: '系統離線', class: 'status-offline' }
  }
})

// 方法
const getTransitionName = (route) => {
  // 根據路由路徑決定過渡動畫
  if (route.path === '/') return 'slide-fade'
  if (route.path.includes('disk')) return 'zoom-fade'
  if (route.path.includes('dataease')) return 'flip-fade'
  return 'fade'
}

// 生命週期
onMounted(async () => {
  try {
    // 初始化系統數據
    await systemStore.initializeSystem()
    
    // 模擬加載時間，展示動畫效果
    setTimeout(() => {
      isLoading.value = false
    }, 2000)
  } catch (error) {
    console.error('系統初始化失敗:', error)
    isLoading.value = false
  }
})
</script>

<style lang="scss" scoped>
.app-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: 'Microsoft YaHei', 'Helvetica Neue', Arial, sans-serif;
}

.main-content {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

// 頂部導航樣式
.app-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;

  .header-content {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 70px;
  }

  .logo-section {
    display: flex;
    align-items: center;
    gap: 15px;

    .logo-icon {
      width: 45px;
      height: 45px;
      background: linear-gradient(135deg, #667eea, #764ba2);
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: 20px;
    }

    .app-title {
      font-size: 24px;
      font-weight: 600;
      color: #2c3e50;
      margin: 0;
    }
  }

  .nav-menu {
    display: flex;
    gap: 10px;

    .nav-item {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 10px 16px;
      border-radius: 8px;
      text-decoration: none;
      color: #606266;
      transition: all 0.3s ease;
      font-weight: 500;

      &:hover {
        background: rgba(102, 126, 234, 0.1);
        color: #667eea;
        transform: translateY(-2px);
      }

      &.active {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
      }
    }
  }
}

// 主要內容區域
.app-main {
  flex: 1;
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

// 底部樣式
.app-footer {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(0, 0, 0, 0.1);
  padding: 20px 0;

  .footer-content {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 15px;
  }

  .system-info {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 14px;

    .version {
      background: #667eea;
      color: white;
      padding: 2px 8px;
      border-radius: 4px;
      font-weight: 500;
    }

    .separator {
      color: #ddd;
    }

    .status {
      font-weight: 500;
      
      &.status-running {
        color: #67c23a;
      }
      
      &.status-warning {
        color: #e6a23c;
      }
      
      &.status-offline {
        color: #f56c6c;
      }
    }
  }

  .copyright {
    color: #909399;
    font-size: 14px;
  }
}

// 加載遮罩樣式
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;

  .loading-content {
    text-align: center;
    color: white;

    .loading-spinner {
      width: 60px;
      height: 60px;
      border: 4px solid rgba(255, 255, 255, 0.3);
      border-top: 4px solid white;
      border-radius: 50%;
      animation: spin 1s linear infinite;
      margin: 0 auto 30px;
    }

    .loading-text {
      font-size: 28px;
      font-weight: 600;
      margin: 0 0 10px;
    }

    .loading-subtitle {
      font-size: 16px;
      opacity: 0.8;
      margin: 0;
    }
  }
}

// 動畫定義
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

// 過渡動畫
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.slide-fade-enter-active {
  transition: all 0.6s ease;
}
.slide-fade-leave-active {
  transition: all 0.4s ease;
}
.slide-fade-enter-from {
  transform: translateX(30px);
  opacity: 0;
}
.slide-fade-leave-to {
  transform: translateX(-30px);
  opacity: 0;
}

.zoom-fade-enter-active {
  transition: all 0.5s ease;
}
.zoom-fade-leave-active {
  transition: all 0.3s ease;
}
.zoom-fade-enter-from {
  transform: scale(0.9);
  opacity: 0;
}
.zoom-fade-leave-to {
  transform: scale(1.1);
  opacity: 0;
}

.flip-fade-enter-active {
  transition: all 0.6s ease;
}
.flip-fade-leave-active {
  transition: all 0.4s ease;
}
.flip-fade-enter-from {
  transform: rotateY(90deg);
  opacity: 0;
}
.flip-fade-leave-to {
  transform: rotateY(-90deg);
  opacity: 0;
}

// 響應式設計
@media (max-width: 768px) {
  .app-header {
    .header-content {
      flex-direction: column;
      height: auto;
      padding: 15px 20px;
      gap: 15px;
    }

    .nav-menu {
      flex-wrap: wrap;
      justify-content: center;
    }
  }

  .app-main {
    padding: 15px;
  }

  .app-footer {
    .footer-content {
      flex-direction: column;
      text-align: center;
    }
  }
}
</style>