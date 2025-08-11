#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DataEase 整合模組
將 DataEase 開源 BI 工具整合到磁區規劃資料管理系統中
提供強大的數據可視化和分析功能
"""

import os
import json
import requests
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import sqlite3
import logging

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataEaseIntegration:
    """
    DataEase 整合類
    負責與 DataEase 系統的數據交互和可視化功能
    """
    
    def __init__(self, base_dir: str = None):
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent
        self.db_path = self.base_dir / 'disk_planning_data.db'
        self.dataease_config = {
            'host': 'localhost',
            'port': 8081,  # DataEase 默認端口
            'username': 'admin',
            'password': 'DataEase@123456',
            'api_base': 'http://localhost:8081/api'
        }
        self.init_database()
    
    def init_database(self):
        """初始化本地數據庫"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 創建磁碟使用情況表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS disk_usage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    drive_letter TEXT NOT NULL,
                    total_space BIGINT,
                    used_space BIGINT,
                    free_space BIGINT,
                    usage_percentage REAL
                )
            ''')
            
            # 創建文件操作記錄表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS file_operations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    operation_type TEXT NOT NULL,
                    file_path TEXT,
                    file_size BIGINT,
                    status TEXT,
                    details TEXT
                )
            ''')
            
            # 創建系統性能表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_performance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    cpu_usage REAL,
                    memory_usage REAL,
                    disk_io_read BIGINT,
                    disk_io_write BIGINT,
                    network_io BIGINT
                )
            ''')
            
            # 創建項目統計表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS project_statistics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    project_name TEXT NOT NULL,
                    project_type TEXT,
                    file_count INTEGER,
                    total_size BIGINT,
                    last_modified DATETIME,
                    status TEXT
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("數據庫初始化完成")
            
        except Exception as e:
            logger.error(f"數據庫初始化失敗: {e}")
    
    def collect_disk_usage_data(self):
        """收集磁碟使用情況數據"""
        try:
            import shutil
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 檢查常見磁碟
            drives = ['C:', 'D:', 'E:', 'F:', 'G:', 'H:']
            
            for drive in drives:
                drive_path = f"{drive}\\"
                if os.path.exists(drive_path):
                    try:
                        total, used, free = shutil.disk_usage(drive_path)
                        usage_percentage = (used / total) * 100 if total > 0 else 0
                        
                        cursor.execute('''
                            INSERT INTO disk_usage 
                            (drive_letter, total_space, used_space, free_space, usage_percentage)
                            VALUES (?, ?, ?, ?, ?)
                        ''', (drive[0], total, used, free, usage_percentage))
                        
                    except Exception as e:
                        logger.warning(f"無法獲取 {drive} 磁碟資訊: {e}")
            
            conn.commit()
            conn.close()
            logger.info("磁碟使用情況數據收集完成")
            
        except Exception as e:
            logger.error(f"收集磁碟數據失敗: {e}")
    
    def collect_project_statistics(self):
        """收集項目統計數據"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # 定義要統計的項目目錄
            project_dirs = {
                'CloudPDF': 'd:/CloudPDF',
                'Web Speech API': 'd:/Web Speech API',
                'AI Tools': 'd:/02_Assets/AI_Tools',
                'Personal Projects': 'd:/01_Projects',
                'Obsidian System': 'd:/Obsidian檔案管理系統'
            }
            
            for project_name, project_path in project_dirs.items():
                if os.path.exists(project_path):
                    try:
                        # 統計文件數量和總大小
                        file_count = 0
                        total_size = 0
                        last_modified = None
                        
                        for root, dirs, files in os.walk(project_path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                try:
                                    stat = os.stat(file_path)
                                    file_count += 1
                                    total_size += stat.st_size
                                    
                                    file_modified = datetime.fromtimestamp(stat.st_mtime)
                                    if last_modified is None or file_modified > last_modified:
                                        last_modified = file_modified
                                        
                                except (OSError, IOError):
                                    continue
                        
                        # 判斷項目類型
                        project_type = self._determine_project_type(project_path)
                        
                        # 判斷項目狀態
                        status = self._determine_project_status(last_modified)
                        
                        cursor.execute('''
                            INSERT INTO project_statistics 
                            (project_name, project_type, file_count, total_size, last_modified, status)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (project_name, project_type, file_count, total_size, last_modified, status))
                        
                    except Exception as e:
                        logger.warning(f"統計項目 {project_name} 失敗: {e}")
            
            conn.commit()
            conn.close()
            logger.info("項目統計數據收集完成")
            
        except Exception as e:
            logger.error(f"收集項目統計失敗: {e}")
    
    def _determine_project_type(self, project_path: str) -> str:
        """根據項目路徑和內容判斷項目類型"""
        path_lower = project_path.lower()
        
        if 'ai' in path_lower or 'ml' in path_lower:
            return 'AI/ML'
        elif 'web' in path_lower or 'api' in path_lower:
            return 'Web Development'
        elif 'pdf' in path_lower:
            return 'Document Processing'
        elif 'obsidian' in path_lower:
            return 'Knowledge Management'
        elif 'tool' in path_lower:
            return 'Development Tools'
        else:
            return 'General'
    
    def _determine_project_status(self, last_modified: datetime) -> str:
        """根據最後修改時間判斷項目狀態"""
        if last_modified is None:
            return 'Unknown'
        
        now = datetime.now()
        days_since_modified = (now - last_modified).days
        
        if days_since_modified <= 7:
            return 'Active'
        elif days_since_modified <= 30:
            return 'Recent'
        elif days_since_modified <= 90:
            return 'Inactive'
        else:
            return 'Archived'
    
    def generate_dataease_dataset(self, table_name: str) -> Dict[str, Any]:
        """為 DataEase 生成數據集"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            # 根據表名生成不同的數據集
            if table_name == 'disk_usage':
                df = pd.read_sql_query('''
                    SELECT 
                        drive_letter as "磁碟",
                        ROUND(total_space / 1024.0 / 1024.0 / 1024.0, 2) as "總容量(GB)",
                        ROUND(used_space / 1024.0 / 1024.0 / 1024.0, 2) as "已使用(GB)",
                        ROUND(free_space / 1024.0 / 1024.0 / 1024.0, 2) as "可用空間(GB)",
                        ROUND(usage_percentage, 2) as "使用率(%)",
                        DATE(timestamp) as "日期"
                    FROM disk_usage 
                    ORDER BY timestamp DESC
                ''', conn)
                
            elif table_name == 'project_statistics':
                df = pd.read_sql_query('''
                    SELECT 
                        project_name as "項目名稱",
                        project_type as "項目類型",
                        file_count as "文件數量",
                        ROUND(total_size / 1024.0 / 1024.0, 2) as "總大小(MB)",
                        status as "狀態",
                        DATE(last_modified) as "最後修改",
                        DATE(timestamp) as "統計日期"
                    FROM project_statistics 
                    ORDER BY timestamp DESC
                ''', conn)
                
            else:
                raise ValueError(f"不支持的表名: {table_name}")
            
            conn.close()
            
            # 轉換為 DataEase 可用的格式
            dataset = {
                'name': f'磁區規劃_{table_name}',
                'description': f'磁區規劃系統 - {table_name} 數據',
                'data': df.to_dict('records'),
                'columns': [
                    {
                        'name': col,
                        'type': self._get_column_type(df[col]),
                        'description': col
                    } for col in df.columns
                ],
                'row_count': len(df)
            }
            
            return dataset
            
        except Exception as e:
            logger.error(f"生成數據集失敗: {e}")
            return {}
    
    def _get_column_type(self, series: pd.Series) -> str:
        """判斷列的數據類型"""
        if pd.api.types.is_numeric_dtype(series):
            return 'NUMBER'
        elif pd.api.types.is_datetime64_any_dtype(series):
            return 'DATE'
        else:
            return 'TEXT'
    
    def create_dataease_dashboard_config(self) -> Dict[str, Any]:
        """創建 DataEase 儀表板配置"""
        dashboard_config = {
            'name': '磁區規劃管理儀表板',
            'description': '磁區規劃系統的綜合數據分析儀表板',
            'panels': [
                {
                    'id': 'disk_usage_pie',
                    'title': '磁碟使用情況分布',
                    'type': 'pie',
                    'dataset': '磁區規劃_disk_usage',
                    'config': {
                        'dimension': '磁碟',
                        'measure': '已使用(GB)',
                        'colors': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
                    },
                    'position': {'x': 0, 'y': 0, 'w': 6, 'h': 4}
                },
                {
                    'id': 'disk_usage_bar',
                    'title': '各磁碟使用率對比',
                    'type': 'bar',
                    'dataset': '磁區規劃_disk_usage',
                    'config': {
                        'dimension': '磁碟',
                        'measure': '使用率(%)',
                        'colors': ['#FF6B6B']
                    },
                    'position': {'x': 6, 'y': 0, 'w': 6, 'h': 4}
                },
                {
                    'id': 'project_type_distribution',
                    'title': '項目類型分布',
                    'type': 'doughnut',
                    'dataset': '磁區規劃_project_statistics',
                    'config': {
                        'dimension': '項目類型',
                        'measure': '文件數量',
                        'colors': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
                    },
                    'position': {'x': 0, 'y': 4, 'w': 4, 'h': 4}
                },
                {
                    'id': 'project_size_comparison',
                    'title': '項目大小對比',
                    'type': 'horizontal_bar',
                    'dataset': '磁區規劃_project_statistics',
                    'config': {
                        'dimension': '項目名稱',
                        'measure': '總大小(MB)',
                        'colors': ['#45B7D1']
                    },
                    'position': {'x': 4, 'y': 4, 'w': 8, 'h': 4}
                },
                {
                    'id': 'project_status_summary',
                    'title': '項目狀態統計',
                    'type': 'table',
                    'dataset': '磁區規劃_project_statistics',
                    'config': {
                        'columns': ['項目名稱', '項目類型', '狀態', '文件數量', '總大小(MB)', '最後修改'],
                        'sort_by': '總大小(MB)',
                        'sort_order': 'desc'
                    },
                    'position': {'x': 0, 'y': 8, 'w': 12, 'h': 6}
                }
            ],
            'filters': [
                {
                    'field': '日期',
                    'type': 'date_range',
                    'default': 'last_30_days'
                },
                {
                    'field': '項目類型',
                    'type': 'multi_select',
                    'options': ['AI/ML', 'Web Development', 'Document Processing', 'Knowledge Management', 'Development Tools', 'General']
                }
            ]
        }
        
        return dashboard_config
    
    def export_data_for_dataease(self, output_dir: str = None) -> Dict[str, str]:
        """導出數據供 DataEase 使用"""
        if output_dir is None:
            output_dir = self.base_dir / 'dataease_export'
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        exported_files = {}
        
        try:
            # 導出磁碟使用情況數據
            disk_dataset = self.generate_dataease_dataset('disk_usage')
            if disk_dataset:
                disk_file = output_path / 'disk_usage.json'
                with open(disk_file, 'w', encoding='utf-8') as f:
                    json.dump(disk_dataset, f, ensure_ascii=False, indent=2)
                exported_files['disk_usage'] = str(disk_file)
            
            # 導出項目統計數據
            project_dataset = self.generate_dataease_dataset('project_statistics')
            if project_dataset:
                project_file = output_path / 'project_statistics.json'
                with open(project_file, 'w', encoding='utf-8') as f:
                    json.dump(project_dataset, f, ensure_ascii=False, indent=2)
                exported_files['project_statistics'] = str(project_file)
            
            # 導出儀表板配置
            dashboard_config = self.create_dataease_dashboard_config()
            dashboard_file = output_path / 'dashboard_config.json'
            with open(dashboard_file, 'w', encoding='utf-8') as f:
                json.dump(dashboard_config, f, ensure_ascii=False, indent=2)
            exported_files['dashboard_config'] = str(dashboard_file)
            
            # 創建 CSV 格式的數據文件（DataEase 也支持 CSV）
            conn = sqlite3.connect(self.db_path)
            
            # 磁碟使用情況 CSV
            disk_df = pd.read_sql_query('SELECT * FROM disk_usage', conn)
            disk_csv = output_path / 'disk_usage.csv'
            disk_df.to_csv(disk_csv, index=False, encoding='utf-8-sig')
            exported_files['disk_usage_csv'] = str(disk_csv)
            
            # 項目統計 CSV
            project_df = pd.read_sql_query('SELECT * FROM project_statistics', conn)
            project_csv = output_path / 'project_statistics.csv'
            project_df.to_csv(project_csv, index=False, encoding='utf-8-sig')
            exported_files['project_statistics_csv'] = str(project_csv)
            
            conn.close()
            
            logger.info(f"數據導出完成，文件保存在: {output_path}")
            return exported_files
            
        except Exception as e:
            logger.error(f"數據導出失敗: {e}")
            return {}
    
    def generate_integration_guide(self) -> str:
        """生成 DataEase 整合指南"""
        guide = """
# DataEase 整合指南

## 1. 安裝 DataEase

### 方法一：Docker 快速安裝
```bash
# 拉取並運行 DataEase
docker run -d \
  --name dataease \
  -p 8081:8081 \
  -v /opt/dataease/data:/opt/dataease/data \
  dataease/dataease:latest
```

### 方法二：一鍵安裝腳本
```bash
curl -sSL https://dataease.oss-cn-hangzhou.aliyuncs.com/quick_start_v2.sh | bash
```

## 2. 配置數據源

1. 訪問 DataEase：http://localhost:8081
2. 使用默認帳號登入：
   - 用戶名：admin
   - 密碼：DataEase@123456

3. 添加數據源：
   - 類型：SQLite 或 CSV 文件
   - 路徑：使用導出的數據文件

## 3. 創建數據集

1. 在 DataEase 中創建新數據集
2. 選擇已配置的數據源
3. 導入以下表：
   - disk_usage（磁碟使用情況）
   - project_statistics（項目統計）

## 4. 創建儀表板

使用提供的 dashboard_config.json 配置文件，或手動創建以下圖表：

### 磁碟使用情況分析
- 餅圖：各磁碟使用空間分布
- 柱狀圖：磁碟使用率對比
- 折線圖：磁碟使用趨勢

### 項目統計分析
- 環形圖：項目類型分布
- 橫向柱狀圖：項目大小對比
- 表格：項目詳細信息

## 5. 設置自動更新

在磁區規劃系統中定期運行數據收集：
```python
# 在 API 中添加定時任務
from dataease_integration import DataEaseIntegration

integration = DataEaseIntegration()
integration.collect_disk_usage_data()
integration.collect_project_statistics()
integration.export_data_for_dataease()
```

## 6. 高級功能

### 實時數據更新
- 配置 DataEase 定時刷新數據源
- 設置警報規則（磁碟使用率過高等）

### 數據鑽取
- 設置圖表間的聯動關係
- 配置詳細數據查看功能

### 權限管理
- 為不同用戶設置不同的查看權限
- 配置數據行級權限
"""
        return guide


def main():
    """主函數 - 演示 DataEase 整合功能"""
    print("🚀 DataEase 整合模組啟動")
    
    # 初始化整合模組
    integration = DataEaseIntegration()
    
    # 收集數據
    print("📊 收集磁碟使用情況數據...")
    integration.collect_disk_usage_data()
    
    print("📈 收集項目統計數據...")
    integration.collect_project_statistics()
    
    # 導出數據
    print("📤 導出數據供 DataEase 使用...")
    exported_files = integration.export_data_for_dataease()
    
    if exported_files:
        print("✅ 數據導出成功！")
        for data_type, file_path in exported_files.items():
            print(f"  - {data_type}: {file_path}")
    
    # 生成整合指南
    guide = integration.generate_integration_guide()
    guide_file = integration.base_dir / 'DataEase整合指南.md'
    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print(f"📖 整合指南已生成: {guide_file}")
    print("\n🎯 下一步：")
    print("1. 安裝 DataEase（參考整合指南）")
    print("2. 配置數據源")
    print("3. 創建儀表板")
    print("4. 享受強大的數據可視化功能！")


if __name__ == '__main__':
    main()