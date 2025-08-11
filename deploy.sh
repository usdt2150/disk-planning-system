#!/bin/bash

# 磁區規劃系統一鍵部署腳本

echo "=== 磁區規劃系統部署開始 ==="

# 檢查 Docker 和 Docker Compose
if ! command -v docker &> /dev/null; then
    echo "錯誤: Docker 未安裝"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "錯誤: Docker Compose 未安裝"
    exit 1
fi

# 創建必要的目錄
mkdir -p nginx/ssl
mkdir -p data/mysql
mkdir -p data/dataease

# 複製環境變量文件
if [ ! -f .env ]; then
    cp .env.example .env
    echo "請編輯 .env 文件配置您的環境變量"
fi

# 構建和啟動服務
echo "構建 Docker 鏡像..."
docker-compose -f docker-compose.prod.yml build

echo "啟動服務..."
docker-compose -f docker-compose.prod.yml up -d

# 等待服務啟動
echo "等待服務啟動..."
sleep 30

# 檢查服務狀態
echo "檢查服務狀態..."
docker-compose -f docker-compose.prod.yml ps

echo "=== 部署完成 ==="
echo "前端訪問地址: http://localhost"
echo "API 訪問地址: http://localhost/api"
echo "DataEase 訪問地址: http://localhost/dataease"
echo ""
echo "使用以下命令查看日誌:"
echo "docker-compose -f docker-compose.prod.yml logs -f"