<template>
  <div class="file-manager">
    <!-- 頁面標題 -->
    <div class="page-header">
      <h1 class="page-title">
        <i class="el-icon-folder"></i>
        文件管理
      </h1>
      <p class="page-description">管理磁區規劃相關文件，支持上傳、下載、編輯和刪除操作</p>
    </div>

    <!-- 操作工具欄 -->
    <div class="toolbar">
      <div class="toolbar-left">
        <el-button type="primary" @click="uploadFile">
          <i class="el-icon-upload"></i>
          上傳文件
        </el-button>
        <el-button @click="createFolder">
          <i class="el-icon-folder-add"></i>
          新建文件夾
        </el-button>
        <el-button @click="refreshFiles">
          <i class="el-icon-refresh"></i>
          刷新
        </el-button>
      </div>
      <div class="toolbar-right">
        <el-input
          v-model="searchQuery"
          placeholder="搜索文件..."
          prefix-icon="el-icon-search"
          clearable
          @input="handleSearch"
        />
        <el-select v-model="viewMode" @change="handleViewModeChange">
          <el-option label="列表視圖" value="list" />
          <el-option label="網格視圖" value="grid" />
        </el-select>
      </div>
    </div>

    <!-- 面包屑導航 -->
    <div class="breadcrumb">
      <el-breadcrumb separator="/">
        <el-breadcrumb-item @click="navigateToPath('')">根目錄</el-breadcrumb-item>
        <el-breadcrumb-item 
          v-for="(path, index) in breadcrumbPaths" 
          :key="index"
          @click="navigateToPath(path.fullPath)"
        >
          {{ path.name }}
        </el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <!-- 文件列表 -->
    <div class="file-list" :class="viewMode">
      <div v-if="isLoading" class="loading-container">
        <el-skeleton :rows="5" animated />
      </div>
      
      <div v-else-if="filteredFiles.length === 0" class="empty-state">
        <i class="el-icon-folder-opened"></i>
        <h3>{{ searchQuery ? '未找到匹配的文件' : '文件夾為空' }}</h3>
        <p>{{ searchQuery ? '請嘗試其他搜索關鍵詞' : '點擊上傳按鈕添加文件' }}</p>
      </div>
      
      <div v-else>
        <!-- 列表視圖 -->
        <el-table 
          v-if="viewMode === 'list'"
          :data="filteredFiles"
          @row-click="handleFileClick"
          @selection-change="handleSelectionChange"
        >
          <el-table-column type="selection" width="55" />
          <el-table-column label="名稱" min-width="200">
            <template #default="{ row }">
              <div class="file-item">
                <i :class="getFileIcon(row)" class="file-icon"></i>
                <span class="file-name">{{ row.name }}</span>
                <el-tag v-if="row.isNew" type="success" size="small">新</el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="大小" width="120">
            <template #default="{ row }">
              {{ row.type === 'directory' ? '-' : formatFileSize(row.size) }}
            </template>
          </el-table-column>
          <el-table-column label="修改時間" width="180">
            <template #default="{ row }">
              {{ formatDate(row.modified) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200">
            <template #default="{ row }">
              <el-button-group>
                <el-button size="small" @click.stop="downloadFile(row)" v-if="row.type !== 'directory'">
                  <i class="el-icon-download"></i>
                </el-button>
                <el-button size="small" @click.stop="editFile(row)" v-if="isEditableFile(row)">
                  <i class="el-icon-edit"></i>
                </el-button>
                <el-button size="small" @click.stop="renameFile(row)">
                  <i class="el-icon-edit-outline"></i>
                </el-button>
                <el-button size="small" type="danger" @click.stop="deleteFile(row)">
                  <i class="el-icon-delete"></i>
                </el-button>
              </el-button-group>
            </template>
          </el-table-column>
        </el-table>
        
        <!-- 網格視圖 -->
        <div v-else class="grid-view">
          <div 
            v-for="file in filteredFiles" 
            :key="file.name"
            class="grid-item"
            :class="{ selected: selectedFiles.includes(file) }"
            @click="handleFileClick(file)"
            @dblclick="openFile(file)"
          >
            <div class="grid-item-icon">
              <i :class="getFileIcon(file)"></i>
            </div>
            <div class="grid-item-name">{{ file.name }}</div>
            <div class="grid-item-info">
              <span v-if="file.type !== 'directory'">{{ formatFileSize(file.size) }}</span>
              <span>{{ formatDate(file.modified) }}</span>
            </div>
            <div class="grid-item-actions">
              <el-button size="mini" circle @click.stop="downloadFile(file)" v-if="file.type !== 'directory'">
                <i class="el-icon-download"></i>
              </el-button>
              <el-button size="mini" circle @click.stop="editFile(file)" v-if="isEditableFile(file)">
                <i class="el-icon-edit"></i>
              </el-button>
              <el-button size="mini" circle type="danger" @click.stop="deleteFile(file)">
                <i class="el-icon-delete"></i>
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 批量操作欄 -->
    <div v-if="selectedFiles.length > 0" class="batch-actions">
      <div class="batch-info">
        已選擇 {{ selectedFiles.length }} 個項目
      </div>
      <div class="batch-buttons">
        <el-button @click="batchDownload" :disabled="!canBatchDownload">
          <i class="el-icon-download"></i>
          批量下載
        </el-button>
        <el-button type="danger" @click="batchDelete">
          <i class="el-icon-delete"></i>
          批量刪除
        </el-button>
        <el-button @click="clearSelection">
          取消選擇
        </el-button>
      </div>
    </div>

    <!-- 文件上傳對話框 -->
    <el-dialog v-model="uploadDialogVisible" title="上傳文件" width="500px">
      <el-upload
        ref="uploadRef"
        :action="uploadUrl"
        :headers="uploadHeaders"
        :data="uploadData"
        :on-success="handleUploadSuccess"
        :on-error="handleUploadError"
        :before-upload="beforeUpload"
        multiple
        drag
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">將文件拖到此處，或<em>點擊上傳</em></div>
        <template #tip>
          <div class="el-upload__tip">
            支持多文件上傳，單個文件大小不超過 100MB
          </div>
        </template>
      </el-upload>
    </el-dialog>

    <!-- 文件編輯對話框 -->
    <el-dialog v-model="editDialogVisible" title="編輯文件" width="80%" top="5vh">
      <div class="editor-container">
        <div class="editor-toolbar">
          <el-button type="primary" @click="saveFile">
            <i class="el-icon-check"></i>
            保存
          </el-button>
          <el-button @click="editDialogVisible = false">
            <i class="el-icon-close"></i>
            取消
          </el-button>
        </div>
        <el-input
          v-model="editContent"
          type="textarea"
          :rows="20"
          placeholder="文件內容..."
          class="editor-textarea"
        />
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useSystemStore } from '@/stores/system'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'
import { gsap } from 'gsap'

const systemStore = useSystemStore()

// 響應式數據
const isLoading = ref(false)
const files = ref([])
const selectedFiles = ref([])
const currentPath = ref('')
const searchQuery = ref('')
const viewMode = ref('list')
const uploadDialogVisible = ref(false)
const editDialogVisible = ref(false)
const editContent = ref('')
const editingFile = ref(null)

// 上傳相關
const uploadRef = ref(null)
const uploadUrl = '/api/files/upload'
const uploadHeaders = {}
const uploadData = computed(() => ({ path: currentPath.value }))

// 計算屬性
const filteredFiles = computed(() => {
  if (!searchQuery.value) return files.value
  
  const query = searchQuery.value.toLowerCase()
  return files.value.filter(file => 
    file.name.toLowerCase().includes(query)
  )
})

const breadcrumbPaths = computed(() => {
  if (!currentPath.value) return []
  
  const paths = currentPath.value.split('/').filter(Boolean)
  return paths.map((name, index) => ({
    name,
    fullPath: paths.slice(0, index + 1).join('/')
  }))
})

const canBatchDownload = computed(() => {
  return selectedFiles.value.some(file => file.type !== 'directory')
})

// 方法
const loadFiles = async (path = '') => {
  isLoading.value = true
  
  try {
    const response = await axios.get('/api/files', {
      params: { path }
    })
    
    if (response.data.success) {
      files.value = response.data.files || []
      currentPath.value = path
      
      // 添加動畫效果
      await nextTick()
      animateFileList()
    } else {
      throw new Error(response.data.error || '獲取文件列表失敗')
    }
  } catch (error) {
    console.error('加載文件失敗:', error)
    ElMessage.error(error.message || '加載文件失敗')
  } finally {
    isLoading.value = false
  }
}

const refreshFiles = () => {
  loadFiles(currentPath.value)
}

const navigateToPath = (path) => {
  loadFiles(path)
}

const handleFileClick = (file) => {
  if (file.type === 'directory') {
    const newPath = currentPath.value ? `${currentPath.value}/${file.name}` : file.name
    navigateToPath(newPath)
  } else {
    // 單擊文件時選中/取消選中
    const index = selectedFiles.value.findIndex(f => f.name === file.name)
    if (index > -1) {
      selectedFiles.value.splice(index, 1)
    } else {
      selectedFiles.value.push(file)
    }
  }
}

const openFile = (file) => {
  if (file.type === 'directory') {
    handleFileClick(file)
  } else if (isEditableFile(file)) {
    editFile(file)
  } else {
    downloadFile(file)
  }
}

const handleSelectionChange = (selection) => {
  selectedFiles.value = selection
}

const handleSearch = () => {
  // 搜索邏輯已在計算屬性中處理
}

const handleViewModeChange = () => {
  // 視圖模式切換後重新應用動畫
  setTimeout(() => {
    animateFileList()
  }, 100)
}

const uploadFile = () => {
  uploadDialogVisible.value = true
}

const createFolder = async () => {
  try {
    const { value: folderName } = await ElMessageBox.prompt('請輸入文件夾名稱', '新建文件夾', {
      confirmButtonText: '確定',
      cancelButtonText: '取消',
      inputPattern: /^[^\\/:*?"<>|]+$/,
      inputErrorMessage: '文件夾名稱不能包含特殊字符'
    })
    
    const response = await axios.post('/api/files/mkdir', {
      path: currentPath.value,
      name: folderName
    })
    
    if (response.data.success) {
      ElMessage.success('文件夾創建成功')
      refreshFiles()
    } else {
      throw new Error(response.data.error || '創建文件夾失敗')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '創建文件夾失敗')
    }
  }
}

const downloadFile = async (file) => {
  try {
    const filePath = currentPath.value ? `${currentPath.value}/${file.name}` : file.name
    const response = await axios.get('/api/files/download', {
      params: { path: filePath },
      responseType: 'blob'
    })
    
    // 創建下載鏈接
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', file.name)
    document.body.appendChild(link)
    link.click()
    link.remove()
    window.URL.revokeObjectURL(url)
    
    ElMessage.success('文件下載成功')
  } catch (error) {
    console.error('下載文件失敗:', error)
    ElMessage.error('下載文件失敗')
  }
}

const editFile = async (file) => {
  try {
    const filePath = currentPath.value ? `${currentPath.value}/${file.name}` : file.name
    const response = await axios.get('/api/files/content', {
      params: { path: filePath }
    })
    
    if (response.data.success) {
      editContent.value = response.data.content
      editingFile.value = file
      editDialogVisible.value = true
    } else {
      throw new Error(response.data.error || '讀取文件內容失敗')
    }
  } catch (error) {
    console.error('編輯文件失敗:', error)
    ElMessage.error(error.message || '編輯文件失敗')
  }
}

const saveFile = async () => {
  if (!editingFile.value) return
  
  try {
    const filePath = currentPath.value ? `${currentPath.value}/${editingFile.value.name}` : editingFile.value.name
    const response = await axios.post('/api/files/save', {
      path: filePath,
      content: editContent.value
    })
    
    if (response.data.success) {
      ElMessage.success('文件保存成功')
      editDialogVisible.value = false
      refreshFiles()
    } else {
      throw new Error(response.data.error || '保存文件失敗')
    }
  } catch (error) {
    console.error('保存文件失敗:', error)
    ElMessage.error(error.message || '保存文件失敗')
  }
}

const renameFile = async (file) => {
  try {
    const { value: newName } = await ElMessageBox.prompt('請輸入新名稱', '重命名', {
      confirmButtonText: '確定',
      cancelButtonText: '取消',
      inputValue: file.name,
      inputPattern: /^[^\\/:*?"<>|]+$/,
      inputErrorMessage: '文件名不能包含特殊字符'
    })
    
    if (newName === file.name) return
    
    const oldPath = currentPath.value ? `${currentPath.value}/${file.name}` : file.name
    const newPath = currentPath.value ? `${currentPath.value}/${newName}` : newName
    
    const response = await axios.post('/api/files/rename', {
      oldPath,
      newPath
    })
    
    if (response.data.success) {
      ElMessage.success('重命名成功')
      refreshFiles()
    } else {
      throw new Error(response.data.error || '重命名失敗')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '重命名失敗')
    }
  }
}

const deleteFile = async (file) => {
  try {
    await ElMessageBox.confirm(
      `確定要刪除 "${file.name}" 嗎？此操作不可恢復。`,
      '確認刪除',
      {
        confirmButtonText: '確定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    const filePath = currentPath.value ? `${currentPath.value}/${file.name}` : file.name
    const response = await axios.delete('/api/files/delete', {
      data: { path: filePath }
    })
    
    if (response.data.success) {
      ElMessage.success('刪除成功')
      refreshFiles()
    } else {
      throw new Error(response.data.error || '刪除失敗')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '刪除失敗')
    }
  }
}

const batchDownload = async () => {
  const downloadableFiles = selectedFiles.value.filter(file => file.type !== 'directory')
  
  if (downloadableFiles.length === 0) {
    ElMessage.warning('沒有可下載的文件')
    return
  }
  
  // 逐個下載文件
  for (const file of downloadableFiles) {
    await downloadFile(file)
  }
  
  clearSelection()
}

const batchDelete = async () => {
  try {
    await ElMessageBox.confirm(
      `確定要刪除選中的 ${selectedFiles.value.length} 個項目嗎？此操作不可恢復。`,
      '確認批量刪除',
      {
        confirmButtonText: '確定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    const deletePaths = selectedFiles.value.map(file => 
      currentPath.value ? `${currentPath.value}/${file.name}` : file.name
    )
    
    const response = await axios.delete('/api/files/batch-delete', {
      data: { paths: deletePaths }
    })
    
    if (response.data.success) {
      ElMessage.success('批量刪除成功')
      clearSelection()
      refreshFiles()
    } else {
      throw new Error(response.data.error || '批量刪除失敗')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '批量刪除失敗')
    }
  }
}

const clearSelection = () => {
  selectedFiles.value = []
}

// 上傳相關方法
const beforeUpload = (file) => {
  const isLt100M = file.size / 1024 / 1024 < 100
  
  if (!isLt100M) {
    ElMessage.error('文件大小不能超過 100MB!')
  }
  
  return isLt100M
}

const handleUploadSuccess = (response, file) => {
  if (response.success) {
    ElMessage.success(`${file.name} 上傳成功`)
  } else {
    ElMessage.error(`${file.name} 上傳失敗: ${response.error}`)
  }
}

const handleUploadError = (error, file) => {
  console.error('上傳錯誤:', error)
  ElMessage.error(`${file.name} 上傳失敗`)
}

// 工具方法
const getFileIcon = (file) => {
  if (file.type === 'directory') {
    return 'el-icon-folder'
  }
  
  const ext = file.name.split('.').pop()?.toLowerCase()
  const iconMap = {
    // 文檔
    'txt': 'el-icon-document',
    'md': 'el-icon-document',
    'doc': 'el-icon-document',
    'docx': 'el-icon-document',
    'pdf': 'el-icon-document',
    
    // 圖片
    'jpg': 'el-icon-picture',
    'jpeg': 'el-icon-picture',
    'png': 'el-icon-picture',
    'gif': 'el-icon-picture',
    'svg': 'el-icon-picture',
    
    // 代碼
    'js': 'el-icon-document-copy',
    'ts': 'el-icon-document-copy',
    'vue': 'el-icon-document-copy',
    'html': 'el-icon-document-copy',
    'css': 'el-icon-document-copy',
    'scss': 'el-icon-document-copy',
    'py': 'el-icon-document-copy',
    
    // 壓縮包
    'zip': 'el-icon-box',
    'rar': 'el-icon-box',
    '7z': 'el-icon-box',
    
    // 音視頻
    'mp3': 'el-icon-headset',
    'wav': 'el-icon-headset',
    'mp4': 'el-icon-video-camera',
    'avi': 'el-icon-video-camera'
  }
  
  return iconMap[ext] || 'el-icon-document'
}

const isEditableFile = (file) => {
  if (file.type === 'directory') return false
  
  const ext = file.name.split('.').pop()?.toLowerCase()
  const editableExts = ['txt', 'md', 'js', 'ts', 'vue', 'html', 'css', 'scss', 'json', 'xml', 'py', 'bat', 'sh']
  
  return editableExts.includes(ext)
}

const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

const formatDate = (timestamp) => {
  return new Date(timestamp).toLocaleString('zh-TW')
}

// 動畫效果
const animateFileList = () => {
  if (viewMode.value === 'list') {
    gsap.fromTo('.el-table__row', 
      { x: -50, opacity: 0 },
      { x: 0, opacity: 1, duration: 0.3, stagger: 0.05, ease: 'power2.out' }
    )
  } else {
    gsap.fromTo('.grid-item', 
      { scale: 0.8, opacity: 0 },
      { scale: 1, opacity: 1, duration: 0.4, stagger: 0.08, ease: 'back.out(1.7)' }
    )
  }
}

// 監聽上傳對話框關閉
watch(uploadDialogVisible, (visible) => {
  if (!visible) {
    // 刷新文件列表
    setTimeout(() => {
      refreshFiles()
    }, 1000)
  }
})

// 生命週期
onMounted(() => {
  loadFiles()
})
</script>

<style lang="scss" scoped>
.file-manager {
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
  
  .toolbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    padding: 15px;
    background: white;
    border-radius: 8px;
    box-shadow: var(--shadow-base);
    
    .toolbar-left {
      display: flex;
      gap: 10px;
    }
    
    .toolbar-right {
      display: flex;
      gap: 10px;
      align-items: center;
    }
  }
  
  .breadcrumb {
    margin-bottom: 20px;
    padding: 10px 15px;
    background: white;
    border-radius: 8px;
    box-shadow: var(--shadow-base);
    
    :deep(.el-breadcrumb__item) {
      .el-breadcrumb__inner {
        cursor: pointer;
        
        &:hover {
          color: var(--primary-color);
        }
      }
    }
  }
  
  .file-list {
    background: white;
    border-radius: 8px;
    box-shadow: var(--shadow-base);
    overflow: hidden;
    
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
    
    // 列表視圖樣式
    &.list {
      .file-item {
        display: flex;
        align-items: center;
        
        .file-icon {
          font-size: 1.2rem;
          margin-right: 8px;
          color: var(--primary-color);
        }
        
        .file-name {
          flex: 1;
        }
      }
      
      :deep(.el-table__row) {
        cursor: pointer;
        
        &:hover {
          background-color: var(--bg-page);
        }
      }
    }
    
    // 網格視圖樣式
    &.grid {
      .grid-view {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 20px;
        padding: 20px;
        
        .grid-item {
          display: flex;
          flex-direction: column;
          align-items: center;
          padding: 20px;
          border: 1px solid var(--border-lighter);
          border-radius: 8px;
          cursor: pointer;
          transition: all 0.3s ease;
          position: relative;
          
          &:hover {
            border-color: var(--primary-color);
            box-shadow: var(--shadow-light);
            transform: translateY(-2px);
            
            .grid-item-actions {
              opacity: 1;
            }
          }
          
          &.selected {
            border-color: var(--primary-color);
            background-color: rgba(64, 158, 255, 0.1);
          }
          
          .grid-item-icon {
            font-size: 3rem;
            color: var(--primary-color);
            margin-bottom: 10px;
          }
          
          .grid-item-name {
            font-weight: 500;
            text-align: center;
            margin-bottom: 5px;
            word-break: break-all;
            line-height: 1.4;
          }
          
          .grid-item-info {
            font-size: 0.8rem;
            color: var(--text-secondary);
            text-align: center;
            
            span {
              display: block;
            }
          }
          
          .grid-item-actions {
            position: absolute;
            top: 5px;
            right: 5px;
            opacity: 0;
            transition: opacity 0.3s ease;
            
            .el-button {
              margin-left: 2px;
            }
          }
        }
      }
    }
  }
  
  .batch-actions {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 15px 20px;
    background: white;
    border-radius: 25px;
    box-shadow: var(--shadow-dark);
    z-index: 1000;
    
    .batch-info {
      color: var(--text-primary);
      font-weight: 500;
    }
    
    .batch-buttons {
      display: flex;
      gap: 10px;
    }
  }
  
  .editor-container {
    .editor-toolbar {
      margin-bottom: 15px;
      display: flex;
      gap: 10px;
    }
    
    .editor-textarea {
      :deep(.el-textarea__inner) {
        font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
        font-size: 14px;
        line-height: 1.5;
      }
    }
  }
}

// 響應式設計
@media (max-width: 768px) {
  .file-manager {
    padding: 10px;
    
    .toolbar {
      flex-direction: column;
      gap: 15px;
      
      .toolbar-left,
      .toolbar-right {
        width: 100%;
        justify-content: center;
      }
    }
    
    .file-list.grid .grid-view {
      grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
      gap: 15px;
      padding: 15px;
    }
    
    .batch-actions {
      flex-direction: column;
      gap: 10px;
      
      .batch-buttons {
        flex-wrap: wrap;
        justify-content: center;
      }
    }
  }
}
</style>