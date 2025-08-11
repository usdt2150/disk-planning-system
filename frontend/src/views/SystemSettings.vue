<template>
  <div class="system-settings">
    <!-- 頁面標題 -->
    <div class="page-header">
      <h1 class="page-title">
        <i class="el-icon-setting"></i>
        系統設置
      </h1>
      <p class="page-description">配置系統參數、用戶權限和應用程序設置</p>
    </div>

    <!-- 設置選項卡 -->
    <el-tabs v-model="activeTab" type="card" class="settings-tabs">
      <!-- 基本設置 -->
      <el-tab-pane label="基本設置" name="basic">
        <el-card shadow="hover">
          <template #header>
            <span>系統基本配置</span>
          </template>
          
          <el-form :model="basicSettings" label-width="150px" class="settings-form">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="系統名稱:">
                  <el-input v-model="basicSettings.systemName" placeholder="磁區規劃系統" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="系統版本:">
                  <el-input v-model="basicSettings.version" placeholder="1.0.0" readonly />
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="默認語言:">
                  <el-select v-model="basicSettings.language" style="width: 100%">
                    <el-option label="繁體中文" value="zh-TW" />
                    <el-option label="簡體中文" value="zh-CN" />
                    <el-option label="English" value="en" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="時區設置:">
                  <el-select v-model="basicSettings.timezone" style="width: 100%">
                    <el-option label="台北時間 (UTC+8)" value="Asia/Taipei" />
                    <el-option label="北京時間 (UTC+8)" value="Asia/Shanghai" />
                    <el-option label="東京時間 (UTC+9)" value="Asia/Tokyo" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-form-item label="主題模式:">
              <el-radio-group v-model="basicSettings.theme">
                <el-radio label="light">淺色模式</el-radio>
                <el-radio label="dark">深色模式</el-radio>
                <el-radio label="auto">跟隨系統</el-radio>
              </el-radio-group>
            </el-form-item>
            
            <el-form-item label="自動保存:">
              <el-switch 
                v-model="basicSettings.autoSave" 
                active-text="開啟" 
                inactive-text="關閉"
              />
              <span class="form-help">自動保存用戶操作和設置</span>
            </el-form-item>
            
            <el-form-item label="保存間隔:">
              <el-select v-model="basicSettings.saveInterval" :disabled="!basicSettings.autoSave">
                <el-option label="30秒" :value="30" />
                <el-option label="1分鐘" :value="60" />
                <el-option label="5分鐘" :value="300" />
                <el-option label="10分鐘" :value="600" />
              </el-select>
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>
      
      <!-- 存儲設置 -->
      <el-tab-pane label="存儲設置" name="storage">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>存儲配置</span>
              <el-button type="text" @click="scanStorage">
                <i class="el-icon-refresh"></i>
                掃描存儲
              </el-button>
            </div>
          </template>
          
          <el-form :model="storageSettings" label-width="150px" class="settings-form">
            <el-form-item label="默認存儲路徑:">
              <div class="path-input">
                <el-input v-model="storageSettings.defaultPath" placeholder="選擇默認存儲路徑" />
                <el-button @click="selectPath">瀏覽</el-button>
              </div>
            </el-form-item>
            
            <el-form-item label="臨時文件路徑:">
              <div class="path-input">
                <el-input v-model="storageSettings.tempPath" placeholder="選擇臨時文件路徑" />
                <el-button @click="selectTempPath">瀏覽</el-button>
              </div>
            </el-form-item>
            
            <el-form-item label="備份路徑:">
              <div class="path-input">
                <el-input v-model="storageSettings.backupPath" placeholder="選擇備份路徑" />
                <el-button @click="selectBackupPath">瀏覽</el-button>
              </div>
            </el-form-item>
            
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="磁區掃描深度:">
                  <el-select v-model="storageSettings.scanDepth" style="width: 100%">
                    <el-option label="1層" :value="1" />
                    <el-option label="2層" :value="2" />
                    <el-option label="3層" :value="3" />
                    <el-option label="無限制" :value="-1" />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="文件大小限制:">
                  <el-select v-model="storageSettings.fileSizeLimit" style="width: 100%">
                    <el-option label="100MB" :value="104857600" />
                    <el-option label="500MB" :value="524288000" />
                    <el-option label="1GB" :value="1073741824" />
                    <el-option label="無限制" :value="-1" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
            
            <el-form-item label="自動清理:">
              <el-switch 
                v-model="storageSettings.autoCleanup" 
                active-text="開啟" 
                inactive-text="關閉"
              />
              <span class="form-help">自動清理臨時文件和過期備份</span>
            </el-form-item>
            
            <el-form-item label="清理間隔:">
              <el-select v-model="storageSettings.cleanupInterval" :disabled="!storageSettings.autoCleanup">
                <el-option label="每天" value="daily" />
                <el-option label="每週" value="weekly" />
                <el-option label="每月" value="monthly" />
              </el-select>
            </el-form-item>
            
            <el-form-item label="備份保留天數:">
              <el-input-number 
                v-model="storageSettings.backupRetentionDays" 
                :min="1" 
                :max="365"
                controls-position="right"
              />
            </el-form-item>
          </el-form>
          
          <!-- 存儲統計 -->
          <div class="storage-stats">
            <h4>存儲統計</h4>
            <el-row :gutter="20">
              <el-col :span="8">
                <div class="stat-item">
                  <div class="stat-value">{{ formatBytes(storageStats.totalSpace) }}</div>
                  <div class="stat-label">總空間</div>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="stat-item">
                  <div class="stat-value">{{ formatBytes(storageStats.usedSpace) }}</div>
                  <div class="stat-label">已使用</div>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="stat-item">
                  <div class="stat-value">{{ formatBytes(storageStats.freeSpace) }}</div>
                  <div class="stat-label">可用空間</div>
                </div>
              </el-col>
            </el-row>
          </div>
        </el-card>
      </el-tab-pane>
      
      <!-- 安全設置 -->
      <el-tab-pane label="安全設置" name="security">
        <el-card shadow="hover">
          <template #header>
            <span>安全配置</span>
          </template>
          
          <el-form :model="securitySettings" label-width="150px" class="settings-form">
            <el-form-item label="啟用身份驗證:">
              <el-switch 
                v-model="securitySettings.enableAuth" 
                active-text="開啟" 
                inactive-text="關閉"
              />
            </el-form-item>
            
            <div v-if="securitySettings.enableAuth">
              <el-form-item label="管理員密碼:">
                <el-input 
                  v-model="securitySettings.adminPassword" 
                  type="password" 
                  placeholder="請輸入管理員密碼"
                  show-password
                />
              </el-form-item>
              
              <el-form-item label="會話超時:">
                <el-select v-model="securitySettings.sessionTimeout" style="width: 100%">
                  <el-option label="30分鐘" :value="30" />
                  <el-option label="1小時" :value="60" />
                  <el-option label="2小時" :value="120" />
                  <el-option label="4小時" :value="240" />
                </el-select>
              </el-form-item>
              
              <el-form-item label="最大登錄嘗試:">
                <el-input-number 
                  v-model="securitySettings.maxLoginAttempts" 
                  :min="3" 
                  :max="10"
                  controls-position="right"
                />
              </el-form-item>
              
              <el-form-item label="鎖定時間:">
                <el-select v-model="securitySettings.lockoutDuration" style="width: 100%">
                  <el-option label="5分鐘" :value="5" />
                  <el-option label="15分鐘" :value="15" />
                  <el-option label="30分鐘" :value="30" />
                  <el-option label="1小時" :value="60" />
                </el-select>
              </el-form-item>
            </div>
            
            <el-form-item label="啟用操作日誌:">
              <el-switch 
                v-model="securitySettings.enableAuditLog" 
                active-text="開啟" 
                inactive-text="關閉"
              />
            </el-form-item>
            
            <el-form-item label="日誌保留天數:">
              <el-input-number 
                v-model="securitySettings.auditLogRetentionDays" 
                :min="7" 
                :max="365"
                :disabled="!securitySettings.enableAuditLog"
                controls-position="right"
              />
            </el-form-item>
            
            <el-form-item label="IP白名單:">
              <el-input 
                v-model="securitySettings.ipWhitelist" 
                type="textarea" 
                :rows="3"
                placeholder="每行一個IP地址或IP段，例如：192.168.1.0/24"
              />
            </el-form-item>
          </el-form>
        </el-card>
      </el-tab-pane>
      
      <!-- 通知設置 -->
      <el-tab-pane label="通知設置" name="notification">
        <el-card shadow="hover">
          <template #header>
            <span>通知配置</span>
          </template>
          
          <el-form :model="notificationSettings" label-width="150px" class="settings-form">
            <el-form-item label="啟用通知:">
              <el-switch 
                v-model="notificationSettings.enabled" 
                active-text="開啟" 
                inactive-text="關閉"
              />
            </el-form-item>
            
            <div v-if="notificationSettings.enabled">
              <el-form-item label="通知類型:">
                <el-checkbox-group v-model="notificationSettings.types">
                  <el-checkbox label="system">系統通知</el-checkbox>
                  <el-checkbox label="storage">存儲警告</el-checkbox>
                  <el-checkbox label="backup">備份提醒</el-checkbox>
                  <el-checkbox label="error">錯誤報告</el-checkbox>
                </el-checkbox-group>
              </el-form-item>
              
              <el-form-item label="通知方式:">
                <el-checkbox-group v-model="notificationSettings.methods">
                  <el-checkbox label="browser">瀏覽器通知</el-checkbox>
                  <el-checkbox label="email">郵件通知</el-checkbox>
                  <el-checkbox label="webhook">Webhook</el-checkbox>
                </el-checkbox-group>
              </el-form-item>
              
              <div v-if="notificationSettings.methods.includes('email')">
                <el-form-item label="SMTP服務器:">
                  <el-input v-model="notificationSettings.smtp.host" placeholder="smtp.gmail.com" />
                </el-form-item>
                
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="端口:">
                      <el-input-number 
                        v-model="notificationSettings.smtp.port" 
                        :min="1" 
                        :max="65535"
                        controls-position="right"
                        style="width: 100%"
                      />
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="加密方式:">
                      <el-select v-model="notificationSettings.smtp.security" style="width: 100%">
                        <el-option label="無" value="none" />
                        <el-option label="SSL" value="ssl" />
                        <el-option label="TLS" value="tls" />
                      </el-select>
                    </el-form-item>
                  </el-col>
                </el-row>
                
                <el-row :gutter="20">
                  <el-col :span="12">
                    <el-form-item label="用戶名:">
                      <el-input v-model="notificationSettings.smtp.username" />
                    </el-form-item>
                  </el-col>
                  <el-col :span="12">
                    <el-form-item label="密碼:">
                      <el-input 
                        v-model="notificationSettings.smtp.password" 
                        type="password" 
                        show-password
                      />
                    </el-form-item>
                  </el-col>
                </el-row>
                
                <el-form-item label="收件人:">
                  <el-input 
                    v-model="notificationSettings.smtp.recipients" 
                    placeholder="多個郵箱用逗號分隔"
                  />
                </el-form-item>
              </div>
              
              <div v-if="notificationSettings.methods.includes('webhook')">
                <el-form-item label="Webhook URL:">
                  <el-input v-model="notificationSettings.webhook.url" placeholder="https://example.com/webhook" />
                </el-form-item>
                
                <el-form-item label="請求方法:">
                  <el-select v-model="notificationSettings.webhook.method" style="width: 100%">
                    <el-option label="POST" value="POST" />
                    <el-option label="PUT" value="PUT" />
                  </el-select>
                </el-form-item>
                
                <el-form-item label="請求頭:">
                  <el-input 
                    v-model="notificationSettings.webhook.headers" 
                    type="textarea" 
                    :rows="3"
                    placeholder="JSON格式，例如：{'Authorization': 'Bearer token'}"
                  />
                </el-form-item>
              </div>
            </div>
          </el-form>
        </el-card>
      </el-tab-pane>
      
      <!-- 系統信息 -->
      <el-tab-pane label="系統信息" name="info">
        <el-card shadow="hover">
          <template #header>
            <div class="card-header">
              <span>系統信息</span>
              <el-button type="text" @click="refreshSystemInfo">
                <i class="el-icon-refresh"></i>
                刷新
              </el-button>
            </div>
          </template>
          
          <div class="system-info">
            <el-descriptions :column="2" border>
              <el-descriptions-item label="系統版本">{{ systemInfo.version }}</el-descriptions-item>
              <el-descriptions-item label="構建時間">{{ systemInfo.buildTime }}</el-descriptions-item>
              <el-descriptions-item label="運行時間">{{ formatUptime(systemInfo.uptime) }}</el-descriptions-item>
              <el-descriptions-item label="Node.js版本">{{ systemInfo.nodeVersion }}</el-descriptions-item>
              <el-descriptions-item label="操作系統">{{ systemInfo.platform }}</el-descriptions-item>
              <el-descriptions-item label="CPU架構">{{ systemInfo.arch }}</el-descriptions-item>
              <el-descriptions-item label="內存使用">{{ formatBytes(systemInfo.memoryUsage) }} / {{ formatBytes(systemInfo.totalMemory) }}</el-descriptions-item>
              <el-descriptions-item label="CPU使用率">{{ systemInfo.cpuUsage }}%</el-descriptions-item>
            </el-descriptions>
            
            <div class="system-actions">
              <el-button type="primary" @click="exportSettings">
                <i class="el-icon-download"></i>
                導出設置
              </el-button>
              <el-button @click="importSettings">
                <i class="el-icon-upload2"></i>
                導入設置
              </el-button>
              <el-button type="warning" @click="resetSettings">
                <i class="el-icon-refresh-left"></i>
                重置設置
              </el-button>
              <el-button type="danger" @click="restartSystem">
                <i class="el-icon-refresh-right"></i>
                重啟系統
              </el-button>
            </div>
          </div>
        </el-card>
      </el-tab-pane>
    </el-tabs>
    
    <!-- 保存按鈕 -->
    <div class="save-actions">
      <el-button type="primary" size="large" @click="saveAllSettings" :loading="isSaving">
        <i class="el-icon-check"></i>
        保存所有設置
      </el-button>
      <el-button size="large" @click="resetCurrentTab">
        <i class="el-icon-refresh-left"></i>
        重置當前頁
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useSystemStore } from '@/stores/system'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'
import { gsap } from 'gsap'

const systemStore = useSystemStore()

// 響應式數據
const activeTab = ref('basic')
const isSaving = ref(false)

// 設置數據
const basicSettings = reactive({
  systemName: '磁區規劃系統',
  version: '1.0.0',
  language: 'zh-TW',
  timezone: 'Asia/Taipei',
  theme: 'light',
  autoSave: true,
  saveInterval: 300
})

const storageSettings = reactive({
  defaultPath: 'D:\\磁區規劃\\data',
  tempPath: 'D:\\磁區規劃\\temp',
  backupPath: 'D:\\磁區規劃\\backup',
  scanDepth: 3,
  fileSizeLimit: 1073741824,
  autoCleanup: true,
  cleanupInterval: 'weekly',
  backupRetentionDays: 30
})

const securitySettings = reactive({
  enableAuth: false,
  adminPassword: '',
  sessionTimeout: 60,
  maxLoginAttempts: 5,
  lockoutDuration: 15,
  enableAuditLog: true,
  auditLogRetentionDays: 90,
  ipWhitelist: ''
})

const notificationSettings = reactive({
  enabled: true,
  types: ['system', 'storage', 'error'],
  methods: ['browser'],
  smtp: {
    host: '',
    port: 587,
    security: 'tls',
    username: '',
    password: '',
    recipients: ''
  },
  webhook: {
    url: '',
    method: 'POST',
    headers: ''
  }
})

const storageStats = reactive({
  totalSpace: 0,
  usedSpace: 0,
  freeSpace: 0
})

const systemInfo = reactive({
  version: '1.0.0',
  buildTime: '2024-01-01 00:00:00',
  uptime: 0,
  nodeVersion: '',
  platform: '',
  arch: '',
  memoryUsage: 0,
  totalMemory: 0,
  cpuUsage: 0
})

// 方法
const loadSettings = async () => {
  try {
    const response = await axios.get('/api/settings')
    
    if (response.data.success) {
      const settings = response.data.settings
      
      // 更新各個設置
      Object.assign(basicSettings, settings.basic || {})
      Object.assign(storageSettings, settings.storage || {})
      Object.assign(securitySettings, settings.security || {})
      Object.assign(notificationSettings, settings.notification || {})
    }
  } catch (error) {
    console.error('加載設置失敗:', error)
    ElMessage.error('加載設置失敗')
  }
}

const saveAllSettings = async () => {
  isSaving.value = true
  
  try {
    const settings = {
      basic: basicSettings,
      storage: storageSettings,
      security: securitySettings,
      notification: notificationSettings
    }
    
    const response = await axios.post('/api/settings', { settings })
    
    if (response.data.success) {
      ElMessage.success('設置保存成功')
      systemStore.addNotification({
        type: 'success',
        title: '設置更新',
        message: '系統設置已成功保存'
      })
    } else {
      throw new Error(response.data.error || '保存設置失敗')
    }
  } catch (error) {
    console.error('保存設置失敗:', error)
    ElMessage.error(error.message || '保存設置失敗')
  } finally {
    isSaving.value = false
  }
}

const resetCurrentTab = async () => {
  try {
    await ElMessageBox.confirm(
      '確定要重置當前頁面的設置嗎？此操作不可撤銷。',
      '確認重置',
      {
        confirmButtonText: '確定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    // 根據當前選項卡重置對應設置
    switch (activeTab.value) {
      case 'basic':
        Object.assign(basicSettings, {
          systemName: '磁區規劃系統',
          language: 'zh-TW',
          timezone: 'Asia/Taipei',
          theme: 'light',
          autoSave: true,
          saveInterval: 300
        })
        break
      case 'storage':
        Object.assign(storageSettings, {
          scanDepth: 3,
          fileSizeLimit: 1073741824,
          autoCleanup: true,
          cleanupInterval: 'weekly',
          backupRetentionDays: 30
        })
        break
      case 'security':
        Object.assign(securitySettings, {
          enableAuth: false,
          sessionTimeout: 60,
          maxLoginAttempts: 5,
          lockoutDuration: 15,
          enableAuditLog: true,
          auditLogRetentionDays: 90
        })
        break
      case 'notification':
        Object.assign(notificationSettings, {
          enabled: true,
          types: ['system', 'storage', 'error'],
          methods: ['browser']
        })
        break
    }
    
    ElMessage.success('設置已重置')
  } catch {
    // 用戶取消操作
  }
}

const selectPath = async () => {
  // 這裡應該調用文件選擇對話框
  ElMessage.info('請在後端實現文件路徑選擇功能')
}

const selectTempPath = async () => {
  ElMessage.info('請在後端實現文件路徑選擇功能')
}

const selectBackupPath = async () => {
  ElMessage.info('請在後端實現文件路徑選擇功能')
}

const scanStorage = async () => {
  try {
    const response = await axios.get('/api/storage/scan')
    
    if (response.data.success) {
      Object.assign(storageStats, response.data.stats)
      ElMessage.success('存儲掃描完成')
    }
  } catch (error) {
    console.error('存儲掃描失敗:', error)
    ElMessage.error('存儲掃描失敗')
  }
}

const refreshSystemInfo = async () => {
  try {
    const response = await axios.get('/api/system/info')
    
    if (response.data.success) {
      Object.assign(systemInfo, response.data.info)
    }
  } catch (error) {
    console.error('獲取系統信息失敗:', error)
    ElMessage.error('獲取系統信息失敗')
  }
}

const exportSettings = () => {
  const settings = {
    basic: basicSettings,
    storage: storageSettings,
    security: { ...securitySettings, adminPassword: '' }, // 不導出密碼
    notification: notificationSettings
  }
  
  const dataStr = JSON.stringify(settings, null, 2)
  const dataBlob = new Blob([dataStr], { type: 'application/json' })
  
  const link = document.createElement('a')
  link.href = URL.createObjectURL(dataBlob)
  link.download = `system-settings-${new Date().toISOString().split('T')[0]}.json`
  link.click()
  
  ElMessage.success('設置已導出')
}

const importSettings = () => {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = '.json'
  
  input.onchange = (event) => {
    const file = event.target.files[0]
    if (!file) return
    
    const reader = new FileReader()
    reader.onload = (e) => {
      try {
        const settings = JSON.parse(e.target.result)
        
        // 驗證設置格式
        if (settings.basic) Object.assign(basicSettings, settings.basic)
        if (settings.storage) Object.assign(storageSettings, settings.storage)
        if (settings.security) Object.assign(securitySettings, settings.security)
        if (settings.notification) Object.assign(notificationSettings, settings.notification)
        
        ElMessage.success('設置已導入')
      } catch (error) {
        console.error('導入設置失敗:', error)
        ElMessage.error('設置文件格式錯誤')
      }
    }
    
    reader.readAsText(file)
  }
  
  input.click()
}

const resetSettings = async () => {
  try {
    await ElMessageBox.confirm(
      '確定要重置所有設置嗎？此操作將恢復系統默認設置，不可撤銷。',
      '確認重置',
      {
        confirmButtonText: '確定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    const response = await axios.post('/api/settings/reset')
    
    if (response.data.success) {
      await loadSettings()
      ElMessage.success('設置已重置')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('重置設置失敗:', error)
      ElMessage.error('重置設置失敗')
    }
  }
}

const restartSystem = async () => {
  try {
    await ElMessageBox.confirm(
      '確定要重啟系統嗎？這將中斷所有正在進行的操作。',
      '確認重啟',
      {
        confirmButtonText: '確定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    const response = await axios.post('/api/system/restart')
    
    if (response.data.success) {
      ElMessage.success('系統正在重啟...')
      
      // 5秒後刷新頁面
      setTimeout(() => {
        window.location.reload()
      }, 5000)
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('重啟系統失敗:', error)
      ElMessage.error('重啟系統失敗')
    }
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

const formatUptime = (seconds) => {
  const days = Math.floor(seconds / 86400)
  const hours = Math.floor((seconds % 86400) / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  
  if (days > 0) {
    return `${days}天 ${hours}小時 ${minutes}分鐘`
  } else if (hours > 0) {
    return `${hours}小時 ${minutes}分鐘`
  } else {
    return `${minutes}分鐘`
  }
}

// 動畫效果
const animateCards = () => {
  gsap.fromTo('.el-card', 
    { y: 30, opacity: 0 },
    { y: 0, opacity: 1, duration: 0.6, stagger: 0.1, ease: 'power2.out' }
  )
}

// 生命週期
onMounted(async () => {
  await loadSettings()
  await scanStorage()
  await refreshSystemInfo()
  
  // 啟動動畫
  animateCards()
})
</script>

<style lang="scss" scoped>
.system-settings {
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
  
  .settings-tabs {
    margin-bottom: 30px;
    
    :deep(.el-tabs__header) {
      background: white;
      border-radius: 8px;
      padding: 10px;
      box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
    }
    
    :deep(.el-card) {
      border: none;
      border-radius: 12px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
  }
  
  .settings-form {
    .form-help {
      margin-left: 10px;
      color: var(--text-secondary);
      font-size: 0.8rem;
    }
    
    .path-input {
      display: flex;
      gap: 10px;
      
      .el-input {
        flex: 1;
      }
    }
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: bold;
    color: var(--text-primary);
  }
  
  .storage-stats {
    margin-top: 30px;
    padding-top: 20px;
    border-top: 1px solid var(--border-lighter);
    
    h4 {
      margin-bottom: 20px;
      color: var(--text-primary);
    }
    
    .stat-item {
      text-align: center;
      padding: 20px;
      background: rgba(64, 158, 255, 0.05);
      border-radius: 8px;
      
      .stat-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: var(--primary-color);
        margin-bottom: 5px;
      }
      
      .stat-label {
        color: var(--text-secondary);
        font-size: 0.9rem;
      }
    }
  }
  
  .system-info {
    .system-actions {
      margin-top: 30px;
      padding-top: 20px;
      border-top: 1px solid var(--border-lighter);
      display: flex;
      gap: 15px;
      flex-wrap: wrap;
    }
  }
  
  .save-actions {
    text-align: center;
    padding: 30px 0;
    
    .el-button {
      margin: 0 10px;
      padding: 12px 30px;
      font-size: 1rem;
    }
  }
}

// 響應式設計
@media (max-width: 768px) {
  .system-settings {
    padding: 10px;
    
    .settings-form {
      :deep(.el-row) {
        .el-col {
          width: 100% !important;
          margin-bottom: 15px;
        }
      }
      
      .path-input {
        flex-direction: column;
      }
    }
    
    .storage-stats {
      .el-row .el-col {
        margin-bottom: 15px;
      }
    }
    
    .system-actions {
      flex-direction: column;
      
      .el-button {
        width: 100%;
        margin-bottom: 10px;
      }
    }
    
    .save-actions {
      .el-button {
        width: 100%;
        margin: 5px 0;
      }
    }
  }
}
</style>