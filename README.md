# 🗂️ 磁區規劃管理系統 v2.0 (Disk Planning Management System)

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.0+-green.svg)](https://vuejs.org/)
[![DataEase](https://img.shields.io/badge/DataEase-BI-orange.svg)](https://dataease.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 系統概述

**磁區規劃管理系統**是一個現代化的磁碟空間管理和開發環境優化解決方案，整合了Vue.js前端、Flask API後端、DataEase BI分析、Docker容器化部署等技術，提供完整的企業級磁碟資源管理平台。

### 🆕 v2.0 新功能
- 🎨 **Vue.js 3前端** - 現代化響應式用戶界面
- 🐳 **Docker容器化** - 一鍵部署和擴展
- 🧪 **完整測試覆蓋** - 單元測試和集成測試
- 📊 **增強BI功能** - 更豐富的數據分析和視覺化
- 🔧 **系統監控** - 健康檢查和性能指標
- 💾 **自動備份** - 數據安全保障

### ✨ 核心特色
- 🌐 **Web界面管理**：直觀的瀏覽器界面，支援即時監控和操作
- 📊 **BI數據分析**：整合DataEase，提供專業的數據視覺化
- 🤖 **自動化執行**：一鍵式腳本執行，減少手動操作錯誤
- 🔄 **即時監控**：30秒自動更新，掌握磁碟使用狀況
- 📱 **響應式設計**：支援多裝置存取，隨時隨地管理
- 🛡️ **安全可靠**：完整的錯誤處理和資料備份機制

## 🏗️ 系統架構

```
磁區規劃管理系統 v2.0
├── 🎨 Vue.js 3前端 (frontend/)
│   ├── src/views/          # 頁面組件
│   ├── src/router/         # 路由配置
│   ├── src/stores/         # 狀態管理
│   └── package.json        # 前端依賴
├── 🔧 Flask API後端 (api.py)
├── 💾 資料庫層 (SQLite/MySQL)
├── 📊 DataEase BI整合 (dataease_integration.py)
├── 🐳 Docker容器化 (docker-compose.yml)
├── 🧪 測試套件 (test_api.py)
├── 🤖 自動化腳本 (*.bat)
└── 📋 文檔系統 (docs/)
```

### 🔧 技術棧
| 層級 | 技術選型 | 版本要求 |
|------|---------|----------|
| **前端** | Vue.js + Vite | 3.0+ |
| **後端** | Python Flask | 2.3+ |
| **資料庫** | SQLite/MySQL | 最新穩定版 |
| **BI平台** | DataEase | 最新版本 |
| **容器化** | Docker + Compose | 最新版本 |
| **測試** | pytest | 最新版本 |

## 📋 項目結構說明

### 🎯 核心系統檔案
| 檔案/目錄 | 功能說明 | 類型 |
|---------|---------|------|
| `frontend/` | Vue.js 3前端應用，現代化用戶界面 | 前端 |
| `api.py` | Flask後端服務，RESTful API | 後端 |
| `test_api.py` | 完整的API單元測試套件 | 測試 |
| `deploy.py` | 自動化部署和維護腳本 | 部署 |
| `docker-compose.yml` | Docker容器編排配置 | 容器化 |
| `config.json` | 系統配置文件 | 配置 |
| `requirements.txt` | Python依賴套件清單 | 配置 |
| `.gitignore` | Git版本控制忽略規則 | 版控 |

### 🚀 啟動腳本系列
| 腳本名稱 | 功能描述 | 適用場景 |
|---------|---------|----------|
| `啟動資料管理系統.bat` | 完整系統啟動（推薦） | 日常使用 |
| `啟動系統.bat` | 快速啟動版本 | 簡單啟動 |
| `安裝DataEase.bat` | DataEase BI系統安裝 | BI分析需求 |

### 🔧 管理工具腳本
| 工具名稱 | 主要功能 | 使用時機 |
|---------|---------|----------|
| `磁區規劃實施腳本.bat` | 自動化建立開發環境目錄結構 | 新環境建置 |
| `複製到其他磁區.bat` | 快速複製整個系統到其他磁區 | 系統遷移 |

### 📊 BI數據分析模組
| 組件名稱 | 功能說明 | 輸出格式 |
|---------|---------|----------|
| `dataease_integration.py` | DataEase整合模組，增強數據處理 | JSON/CSV |
| `dataease_dashboard_template.json` | 儀表板模板配置 | JSON |
| `dataease_export/` | 數據導出目錄 | 多格式 |
| **新增功能** | | |
| 實時數據同步 | 自動數據收集和更新 | 實時流 |
| 高級分析 | 趨勢分析和預測模型 | 報表 |
| 自定義儀表板 | 拖拽式圖表建立 | 互動式 |

### 📚 文檔系統 (docs/)
| 文檔名稱 | 內容概述 | 目標讀者 |
|---------|---------|----------|
| `磁區規劃系統使用說明.md` | 完整的系統使用指南 | 所有用戶 |
| `磁區規劃方案.md` | 磁區規劃策略和實施方案 | 系統管理員 |
| `磁區規劃優化建議.md` | 雲端和AI專案優化建議 | 開發者 |
| `AI語音客戶服務中心架構規劃.md` | AI專案架構設計 | 架構師 |
| `磁區規劃中英文對照表.md` | 國際化命名對照 | 國際化團隊 |
| **新增文檔** | | |
| `API文檔.md` | RESTful API完整說明 | 開發者 |
| `Docker部署指南.md` | 容器化部署詳細說明 | DevOps |
| `測試指南.md` | 測試策略和執行指南 | QA工程師 |

## 🚀 快速開始指南

### 🌟 方法一：Docker一鍵部署（推薦）

```bash
# 1. 克隆項目
git clone <repository-url>
cd 磁區規劃管理系統

# 2. 啟動完整環境
docker-compose up -d

# 3. 訪問應用
# 前端: http://localhost:3002
# API: http://localhost:5000
# DataEase: http://localhost:8081
```

### 🔧 方法二：傳統批次檔啟動

```bash
# 1. 雙擊執行啟動腳本
啟動資料管理系統.bat
```

**執行流程：**
1. 🔍 **環境檢查**：自動檢測Python環境和版本
2. 📦 **依賴安裝**：自動安裝Flask、Flask-CORS等必要套件
3. 🔧 **系統初始化**：檢查核心檔案完整性
4. 🚀 **服務啟動**：啟動Flask API服務（4個步驟）
5. 🌐 **界面開啟**：自動開啟瀏覽器管理界面

**功能特色：**
- ✅ 完整的錯誤診斷和解決建議
- ✅ 詳細的進度顯示和狀態回饋
- ✅ 自動化環境配置和相依性處理

### ⚡ 方法二：快速啟動（適合熟悉用戶）

```bash
# 1. 雙擊執行快速啟動
啟動系統.bat
```

**特點：**
- 🔥 更快的啟動速度
- 📊 系統資訊詳細顯示
- 🎯 適合日常快速使用

### 🛠️ 方法三：開發者模式（手動控制）

```bash
# 1. 後端設置
pip install -r requirements.txt
python api.py

# 2. 前端設置（新終端）
cd frontend
npm install
npm run dev

# 3. 訪問地址
# 前端界面：http://localhost:3002
# API服務：http://localhost:5000
# 健康檢查：http://localhost:5000/api/health
```

### 🧪 方法四：測試和驗證

```bash
# 運行單元測試
python -m pytest test_api.py -v

# 系統健康檢查
python deploy.py health

# 創建系統備份
python deploy.py backup
```

**適用場景：**
- 🔧 需要自定義配置
- 🐛 除錯和開發測試
- 🔍 深度系統分析

## 📊 DataEase BI 數據分析平台

### 🔧 安裝配置流程

#### Docker方式（推薦）
```bash
# 1. 使用Docker Compose啟動
docker-compose up -d dataease

# 2. 訪問DataEase
# http://localhost:8081
# 默認帳號: admin / dataease
```

#### 傳統安裝方式
```bash
# 1. 執行自動安裝腳本
安裝DataEase.bat
```

**安裝選項：**
1. **🆕 全新安裝 DataEase** - 完整安裝BI平台
2. **🔄 升級現有版本** - 更新到最新版本
3. **▶️ 啟動 DataEase 服務** - 啟動已安裝的服務
4. **⏹️ 停止 DataEase 服務** - 停止運行中的服務
5. **🗑️ 完全移除 DataEase** - 清理所有相關檔案
6. **❌ 退出安裝程序** - 取消安裝

### 📈 數據分析工作流程

#### 步驟 1：數據收集
```
管理界面 → 📊 DataEase BI → 📊 收集數據
```
- 🔍 自動掃描磁碟使用情況
- 📊 生成項目統計報告
- 💾 儲存至SQLite資料庫

#### 步驟 2：數據導出
```
管理界面 → 📊 DataEase BI → 📤 導出數據
```
- 📄 生成CSV格式數據檔案
- 📋 創建JSON格式配置檔案
- 📁 儲存至 `dataease_export/` 目錄

#### 步驟 3：BI平台分析
```
管理界面 → 📊 DataEase BI → 🌐 打開 DataEase
```
- 🔐 **登入資訊**：`admin` / `dataease`
- 📊 **存取位址**：`http://localhost:8081`
- 🎯 **功能特色**：拖拉式圖表建立、即時數據更新

### 🎨 儀表板建立指南

1. **📥 數據源導入**
   - 選擇CSV檔案作為數據源
   - 配置數據連接參數
   - 驗證數據完整性

2. **📊 圖表設計**
   - 使用預設模板快速建立
   - 自定義圖表樣式和配色
   - 設定數據篩選和排序規則

3. **🎯 分析維度**
   - 磁碟使用量趨勢分析
   - 專案類型分布統計
   - 空間使用效率評估

## 🔄 系統遷移與部署

### 🐳 Docker部署（推薦）

```bash
# 1. 生產環境部署
docker-compose -f docker-compose.prod.yml up -d

# 2. 擴展服務
docker-compose scale api=3

# 3. 監控服務狀態
docker-compose ps
```

### 📦 傳統遷移方案

```bash
# 1. 執行複製腳本
複製到其他磁區.bat
```

**遷移流程：**
1. 🎯 **選擇目標磁區**：支援所有可用磁碟機
2. 📁 **複製系統檔案**：完整複製所有核心檔案
3. 🔧 **自動配置調整**：更新磁區代號和路徑設定
4. ✅ **完整性驗證**：確保所有檔案正確複製

### 🏗️ 開發環境建置

```bash
# 1. 執行環境建置腳本
磁區規劃實施腳本.bat
```

**建置選項：**
- 🌐 **中文目錄結構**：適合中文環境開發者
- 🔤 **英文目錄結構**：符合國際化標準
- 🎯 **專案分類管理**：Web、Mobile、AI、Data Science
- ☁️ **雲端整合支援**：GitHub、Google Cloud、CI/CD

## 🔧 系統需求規格

### 💻 基本系統需求
| 組件 | 最低需求 | 建議配置 | Docker需求 |
|------|---------|---------|------------|
| **作業系統** | Windows 10 / Linux | Windows 11 / Ubuntu 20.04+ | Docker支援 |
| **處理器** | Intel i3 / AMD 同等級 | Intel i5 / AMD Ryzen 5 | 多核心處理 |
| **記憶體** | 8GB RAM | 16GB RAM | 容器化需更多記憶體 |
| **磁碟空間** | 5GB 可用空間 | 20GB 可用空間 | Docker映像和數據 |
| **網路** | 穩定網路連線 | 高速網路 | 容器映像下載 |

### 🐍 開發環境需求
| 項目 | 版本需求 | 自動檢查 | 備註 |
|------|---------|---------|------|
| **Python** | 3.8+ | ✅ | 後端API服務 |
| **Node.js** | 16+ | ✅ | 前端構建工具 |
| **Docker** | 20.10+ | ✅ | 容器化部署 |
| **Docker Compose** | 2.0+ | ✅ | 服務編排 |
| **Git** | 2.30+ | ✅ | 版本控制 |

### 🌐 瀏覽器相容性
| 瀏覽器 | 最低版本 | 推薦版本 | 功能支援 |
|--------|---------|---------|----------|
| **Chrome** | 80+ | 最新版本 | 完整功能支援 |
| **Firefox** | 75+ | 最新版本 | 完整功能支援 |
| **Edge** | 80+ | 最新版本 | 完整功能支援 |
| **Safari** | 13+ | 最新版本 | 基本功能支援 |

### 🐳 容器化部署需求
| 組件 | 需求規格 | 說明 |
|------|---------|------|
| **Docker Desktop** | 最新穩定版 | 容器化平台 |
| **記憶體** | 12GB+ RAM | 多容器運行需求 |
| **磁碟空間** | 15GB+ 可用 | 映像和數據儲存 |
| **網路連線** | 穩定高速網路 | 映像下載和更新 |

### 🔌 端口配置
| 服務 | 端口 | 說明 |
|------|------|------|
| **前端** | 3002 | Vue.js開發服務器 |
| **API** | 5000 | Flask後端服務 |
| **DataEase** | 8081 | BI分析平台 |
| **MySQL** | 3307 | 資料庫服務 |
| **Redis** | 6379 | 快取服務（可選） |

## ⚠️ 重要注意事項

### 🛡️ 安全性考量
- 🔒 **權限管理**：Docker需要適當的系統權限
- 💾 **資料備份**：使用 `python deploy.py backup` 定期備份
- 🔐 **端口安全**：生產環境請配置防火牆規則
- 🛡️ **容器安全**：定期更新Docker映像和基礎系統
- 🔑 **密碼管理**：使用環境變量管理敏感信息

### 🔧 系統配置建議
- 📁 **磁碟空間**：確保有足夠空間存放Docker映像
- 🌐 **網路環境**：穩定網路連線下載容器映像
- 💻 **系統更新**：保持作業系統和Docker為最新版本
- 🔄 **服務管理**：使用 `docker-compose` 管理服務生命週期
- 📊 **監控設置**：配置系統監控和日誌收集

### 🐛 常見問題排除

#### Docker相關問題
```bash
# 檢查Docker狀態
docker --version
docker-compose --version

# 查看容器狀態
docker-compose ps

# 查看容器日誌
docker-compose logs api
docker-compose logs frontend

# 重新構建容器
docker-compose build --no-cache
```

#### 端口占用問題
```bash
# 檢查端口占用
netstat -tulpn | grep :5000
netstat -tulpn | grep :3002

# 停止所有服務
docker-compose down

# 清理未使用的容器
docker system prune -f
```

#### 前端構建問題
```bash
# 清理node_modules
cd frontend
rm -rf node_modules package-lock.json
npm install

# 重新構建
npm run build
```

## 📞 技術支援與維護

### 🆘 獲取幫助
- 📋 **系統日誌**：`docker-compose logs` 查看詳細日誌
- 🔍 **健康檢查**：`http://localhost:5000/api/health` 檢查系統狀態
- 📊 **系統指標**：`http://localhost:5000/api/metrics` 查看性能指標
- 🧪 **測試驗證**：`python -m pytest test_api.py -v` 運行測試

### 🔄 系統維護
```bash
# 創建系統備份
python deploy.py backup

# 系統健康檢查
python deploy.py health

# 完全重置（謹慎使用）
docker-compose down -v
docker-compose up -d
```

### 📊 監控和日誌
```bash
# 實時查看日誌
docker-compose logs -f api

# 查看資源使用
docker stats

# 系統性能監控
curl http://localhost:5000/api/metrics
```

## 🚀 GitHub推送準備

### 📋 推送前檢查清單
- ✅ **代碼完整性**：所有核心檔案已包含
- ✅ **測試覆蓋**：單元測試通過
- ✅ **文檔完整**：README和使用說明完整
- ✅ **Docker配置**：容器化部署配置完成
- ✅ **環境變量**：敏感信息已移除
- ✅ **.gitignore**：忽略規則已配置

### 🔧 推送命令
```bash
# 初始化Git倉庫
git init
git add .
git commit -m "feat: 磁區規劃管理系統 v2.0 - 完整重構版本"

# 添加遠程倉庫
git remote add origin <your-repository-url>
git branch -M main
git push -u origin main
```

### 📦 發布版本
```bash
# 創建版本標籤
git tag -a v2.0 -m "磁區規劃管理系統 v2.0 正式發布"
git push origin v2.0
```

---

## 📈 版本資訊

**當前版本：** v2.0  
**發布日期：** 2025年1月  
**主要更新：**
- 🎨 Vue.js 3現代化前端重構
- 🐳 Docker容器化部署支援
- 🧪 完整測試套件和CI/CD準備
- 📊 增強的DataEase BI整合
- 🔧 系統監控和自動備份功能
- 📚 完整的文檔和部署指南

**下次更新：** 預計2025年Q2 - 微服務架構和Kubernetes支援

---

## 🤝 貢獻指南

### 🔧 開發環境設置
1. Fork本項目到您的GitHub帳戶
2. 克隆您的Fork：`git clone <your-fork-url>`
3. 安裝開發依賴：`npm install` 和 `pip install -r requirements.txt`
4. 運行測試：`python -m pytest test_api.py -v`
5. 啟動開發環境：`docker-compose up -d`

### 📝 提交規範
- `feat:` 新功能
- `fix:` 錯誤修復
- `docs:` 文檔更新
- `test:` 測試相關
- `refactor:` 代碼重構
- `chore:` 構建過程或輔助工具的變動

### 🎯 開發路線圖
- [ ] 微服務架構重構
- [ ] Kubernetes部署支援
- [ ] 多租戶支援
- [ ] 高級分析和機器學習整合
- [ ] 移動端應用開發

---

*💡 提示：本項目已準備好推送到GitHub，包含完整的Docker化部署、測試套件和文檔。建議先在本地測試所有功能後再推送。*