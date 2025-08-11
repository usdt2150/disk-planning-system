<template>
  <div class="not-found">
    <div class="error-container">
      <!-- 404動畫圖標 -->
      <div class="error-animation">
        <div class="error-number">
          <span class="digit" ref="digit1">4</span>
          <div class="disk-icon" ref="diskIcon">
            <div class="disk-outer">
              <div class="disk-inner"></div>
              <div class="disk-hole"></div>
            </div>
            <div class="disk-arm"></div>
          </div>
          <span class="digit" ref="digit2">4</span>
        </div>
        
        <!-- 浮動粒子效果 -->
        <div class="particles">
          <div v-for="i in 20" :key="i" class="particle" :style="getParticleStyle(i)"></div>
        </div>
      </div>
      
      <!-- 錯誤信息 -->
      <div class="error-content">
        <h1 class="error-title">頁面未找到</h1>
        <p class="error-description">
          抱歉，您訪問的頁面不存在或已被移動。
          <br>
          請檢查URL是否正確，或返回首頁繼續瀏覽。
        </p>
        
        <!-- 建議操作 -->
        <div class="error-suggestions">
          <h3>您可以嘗試：</h3>
          <ul>
            <li>檢查URL拼寫是否正確</li>
            <li>返回上一頁繼續瀏覽</li>
            <li>訪問系統首頁</li>
            <li>使用搜索功能查找內容</li>
          </ul>
        </div>
        
        <!-- 操作按鈕 -->
        <div class="error-actions">
          <el-button type="primary" size="large" @click="goHome">
            <i class="el-icon-house"></i>
            返回首頁
          </el-button>
          <el-button size="large" @click="goBack">
            <i class="el-icon-back"></i>
            返回上頁
          </el-button>
          <el-button size="large" @click="refreshPage">
            <i class="el-icon-refresh"></i>
            刷新頁面
          </el-button>
        </div>
        
        <!-- 快速導航 -->
        <div class="quick-nav">
          <h3>快速導航：</h3>
          <div class="nav-links">
            <router-link to="/dashboard" class="nav-link">
              <i class="el-icon-data-board"></i>
              <span>系統概覽</span>
            </router-link>
            <router-link to="/file-manager" class="nav-link">
              <i class="el-icon-folder"></i>
              <span>文件管理</span>
            </router-link>
            <router-link to="/disk-monitor" class="nav-link">
              <i class="el-icon-monitor"></i>
              <span>磁區監控</span>
            </router-link>
            <router-link to="/dataease-bi" class="nav-link">
              <i class="el-icon-data-analysis"></i>
              <span>BI分析</span>
            </router-link>
            <router-link to="/settings" class="nav-link">
              <i class="el-icon-setting"></i>
              <span>系統設置</span>
            </router-link>
          </div>
        </div>
      </div>
      
      <!-- 系統狀態 -->
      <div class="system-status">
        <div class="status-item">
          <i class="el-icon-circle-check status-icon online"></i>
          <span>系統運行正常</span>
        </div>
        <div class="status-item">
          <i class="el-icon-time status-icon"></i>
          <span>{{ currentTime }}</span>
        </div>
      </div>
    </div>
    
    <!-- 背景裝飾 -->
    <div class="background-decoration">
      <div class="decoration-circle circle-1"></div>
      <div class="decoration-circle circle-2"></div>
      <div class="decoration-circle circle-3"></div>
      <div class="decoration-lines">
        <div v-for="i in 10" :key="i" class="line" :style="getLineStyle(i)"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { gsap } from 'gsap'

const router = useRouter()

// 響應式數據
const currentTime = ref('')
const digit1 = ref(null)
const digit2 = ref(null)
const diskIcon = ref(null)

// 時間更新
const updateTime = () => {
  currentTime.value = new Date().toLocaleString('zh-TW')
}

// 定時器
let timeInterval = null

// 方法
const goHome = () => {
  router.push('/dashboard')
}

const goBack = () => {
  if (window.history.length > 1) {
    router.go(-1)
  } else {
    router.push('/dashboard')
  }
}

const refreshPage = () => {
  window.location.reload()
}

// 粒子樣式生成
const getParticleStyle = (index) => {
  const angle = (index * 18) % 360
  const distance = 100 + (index % 3) * 50
  const size = 4 + (index % 3) * 2
  
  return {
    '--angle': `${angle}deg`,
    '--distance': `${distance}px`,
    '--size': `${size}px`,
    '--delay': `${index * 0.1}s`
  }
}

// 背景線條樣式
const getLineStyle = (index) => {
  const angle = (index * 36) % 360
  const length = 50 + (index % 4) * 30
  
  return {
    '--angle': `${angle}deg`,
    '--length': `${length}px`,
    '--delay': `${index * 0.2}s`
  }
}

// 動畫效果
const initAnimations = () => {
  // 數字動畫
  gsap.fromTo([digit1.value, digit2.value], 
    { 
      y: 100, 
      opacity: 0, 
      rotation: 180 
    },
    { 
      y: 0, 
      opacity: 1, 
      rotation: 0, 
      duration: 1.2, 
      ease: 'elastic.out(1, 0.5)',
      stagger: 0.2
    }
  )
  
  // 磁盤圖標動畫
  gsap.fromTo(diskIcon.value, 
    { 
      scale: 0, 
      rotation: -180 
    },
    { 
      scale: 1, 
      rotation: 0, 
      duration: 1.5, 
      ease: 'back.out(1.7)',
      delay: 0.5
    }
  )
  
  // 磁盤旋轉動畫
  gsap.to(diskIcon.value.querySelector('.disk-outer'), {
    rotation: 360,
    duration: 3,
    ease: 'none',
    repeat: -1
  })
  
  // 磁盤臂擺動
  gsap.to(diskIcon.value.querySelector('.disk-arm'), {
    rotation: 15,
    duration: 2,
    ease: 'power2.inOut',
    yoyo: true,
    repeat: -1
  })
  
  // 內容動畫
  gsap.fromTo('.error-content', 
    { y: 50, opacity: 0 },
    { y: 0, opacity: 1, duration: 1, ease: 'power2.out', delay: 1 }
  )
  
  // 粒子動畫
  gsap.to('.particle', {
    rotation: 360,
    duration: 10,
    ease: 'none',
    repeat: -1,
    stagger: {
      each: 0.1,
      from: 'random'
    }
  })
  
  // 背景裝飾動畫
  gsap.to('.decoration-circle', {
    rotation: 360,
    duration: 20,
    ease: 'none',
    repeat: -1,
    stagger: 2
  })
  
  gsap.to('.line', {
    scaleX: 1.5,
    duration: 3,
    ease: 'power2.inOut',
    yoyo: true,
    repeat: -1,
    stagger: 0.2
  })
}

// 生命週期
onMounted(() => {
  updateTime()
  timeInterval = setInterval(updateTime, 1000)
  
  // 延遲啟動動畫確保DOM已渲染
  setTimeout(initAnimations, 100)
})

onUnmounted(() => {
  if (timeInterval) {
    clearInterval(timeInterval)
  }
})
</script>

<style lang="scss" scoped>
.not-found {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
  
  .error-container {
    text-align: center;
    z-index: 10;
    position: relative;
    max-width: 800px;
    padding: 40px 20px;
    
    .error-animation {
      position: relative;
      margin-bottom: 40px;
      
      .error-number {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        margin-bottom: 30px;
        
        .digit {
          font-size: 8rem;
          font-weight: bold;
          color: white;
          text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
          
          @media (max-width: 768px) {
            font-size: 4rem;
          }
        }
        
        .disk-icon {
          position: relative;
          width: 120px;
          height: 120px;
          
          @media (max-width: 768px) {
            width: 80px;
            height: 80px;
          }
          
          .disk-outer {
            width: 100%;
            height: 100%;
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            border-radius: 50%;
            position: relative;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
            
            .disk-inner {
              position: absolute;
              top: 10px;
              left: 10px;
              right: 10px;
              bottom: 10px;
              background: linear-gradient(45deg, #feca57, #ff9ff3);
              border-radius: 50%;
            }
            
            .disk-hole {
              position: absolute;
              top: 50%;
              left: 50%;
              width: 20px;
              height: 20px;
              background: #333;
              border-radius: 50%;
              transform: translate(-50%, -50%);
            }
          }
          
          .disk-arm {
            position: absolute;
            top: 20px;
            right: -10px;
            width: 4px;
            height: 60px;
            background: #333;
            border-radius: 2px;
            transform-origin: top center;
            
            &::after {
              content: '';
              position: absolute;
              bottom: -5px;
              left: -3px;
              width: 10px;
              height: 10px;
              background: #666;
              border-radius: 50%;
            }
          }
        }
      }
      
      .particles {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        
        .particle {
          position: absolute;
          width: var(--size);
          height: var(--size);
          background: rgba(255, 255, 255, 0.6);
          border-radius: 50%;
          transform: rotate(var(--angle)) translateX(var(--distance));
          animation: float 3s ease-in-out infinite var(--delay);
        }
      }
    }
    
    .error-content {
      color: white;
      
      .error-title {
        font-size: 3rem;
        margin-bottom: 20px;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        
        @media (max-width: 768px) {
          font-size: 2rem;
        }
      }
      
      .error-description {
        font-size: 1.2rem;
        margin-bottom: 30px;
        line-height: 1.6;
        opacity: 0.9;
        
        @media (max-width: 768px) {
          font-size: 1rem;
        }
      }
      
      .error-suggestions {
        text-align: left;
        max-width: 400px;
        margin: 0 auto 30px;
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 12px;
        backdrop-filter: blur(10px);
        
        h3 {
          margin-bottom: 15px;
          color: #feca57;
        }
        
        ul {
          list-style: none;
          padding: 0;
          
          li {
            padding: 5px 0;
            position: relative;
            padding-left: 20px;
            
            &::before {
              content: '•';
              position: absolute;
              left: 0;
              color: #feca57;
              font-weight: bold;
            }
          }
        }
      }
      
      .error-actions {
        display: flex;
        gap: 15px;
        justify-content: center;
        margin-bottom: 40px;
        flex-wrap: wrap;
        
        .el-button {
          padding: 12px 24px;
          font-size: 1rem;
          border-radius: 25px;
          transition: all 0.3s ease;
          
          &:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
          }
        }
      }
      
      .quick-nav {
        text-align: left;
        max-width: 600px;
        margin: 0 auto;
        background: rgba(255, 255, 255, 0.1);
        padding: 25px;
        border-radius: 12px;
        backdrop-filter: blur(10px);
        
        h3 {
          margin-bottom: 20px;
          color: #feca57;
          text-align: center;
        }
        
        .nav-links {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 15px;
          
          .nav-link {
            display: flex;
            align-items: center;
            padding: 15px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            text-decoration: none;
            color: white;
            transition: all 0.3s ease;
            
            &:hover {
              background: rgba(255, 255, 255, 0.2);
              transform: translateY(-2px);
            }
            
            i {
              font-size: 1.5rem;
              margin-right: 10px;
              color: #feca57;
            }
            
            span {
              font-weight: 500;
            }
          }
        }
      }
    }
    
    .system-status {
      position: absolute;
      bottom: 20px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      gap: 30px;
      color: rgba(255, 255, 255, 0.8);
      font-size: 0.9rem;
      
      .status-item {
        display: flex;
        align-items: center;
        gap: 8px;
        
        .status-icon {
          font-size: 1.2rem;
          
          &.online {
            color: #2ed573;
          }
        }
      }
    }
  }
  
  .background-decoration {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    
    .decoration-circle {
      position: absolute;
      border: 2px solid rgba(255, 255, 255, 0.1);
      border-radius: 50%;
      
      &.circle-1 {
        width: 200px;
        height: 200px;
        top: 10%;
        left: 10%;
      }
      
      &.circle-2 {
        width: 300px;
        height: 300px;
        top: 60%;
        right: 10%;
      }
      
      &.circle-3 {
        width: 150px;
        height: 150px;
        bottom: 20%;
        left: 20%;
      }
    }
    
    .decoration-lines {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      
      .line {
        position: absolute;
        width: var(--length);
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transform: rotate(var(--angle));
        transform-origin: left center;
      }
    }
  }
}

// 動畫關鍵幀
@keyframes float {
  0%, 100% {
    transform: rotate(var(--angle)) translateX(var(--distance)) translateY(0);
  }
  50% {
    transform: rotate(var(--angle)) translateX(var(--distance)) translateY(-10px);
  }
}

// 響應式設計
@media (max-width: 768px) {
  .not-found {
    .error-container {
      padding: 20px 10px;
      
      .error-content {
        .error-actions {
          flex-direction: column;
          align-items: center;
          
          .el-button {
            width: 200px;
          }
        }
        
        .quick-nav {
          .nav-links {
            grid-template-columns: 1fr;
          }
        }
      }
      
      .system-status {
        flex-direction: column;
        gap: 10px;
        text-align: center;
      }
    }
  }
}
</style>