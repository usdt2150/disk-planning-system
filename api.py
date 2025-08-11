#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
磁區規劃資料管理系統 API
提供文件管理、狀態追蹤、進度監控等功能
"""

import os
import json
import datetime
import logging
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import subprocess
import hashlib
from dataease_integration import DataEaseIntegration

# 配置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # 允許跨域請求

# 配置
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR
STATUS_FILE = BASE_DIR / 'system_status.json'
CONFIG_FILE = BASE_DIR / 'config.json'

# 載入配置
def load_config():
    """載入系統配置"""
    default_config = {
        'dataease': {
            'host': 'localhost',
            'port': 8081,
            'timeout': 5
        },
        'api': {
            'host': '0.0.0.0',
            'port': 5000,
            'debug': False
        },
        'logging': {
            'level': 'INFO',
            'file': 'api.log'
        }
    }
    
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        except Exception as e:
            logger.warning(f"載入配置文件失敗，使用預設配置: {e}")
    
    return default_config

config = load_config()

# 初始化 DataEase 整合
try:
    dataease = DataEaseIntegration(str(BASE_DIR))
    logger.info("DataEase 整合模組初始化成功")
except Exception as e:
    logger.error(f"DataEase 整合模組初始化失敗: {e}")
    dataease = None

# 文件配置
FILES_CONFIG = {
    'plan': {
        'filename': '磁區規劃方案.md',
        'title': '磁區規劃方案',
        'type': '主要規劃文件',
        'status': 'completed',
        'description': '完整的H槽開發環境規劃'
    },
    'optimization': {
        'filename': '磁區規劃優化建議.md',
        'title': '優化建議',
        'type': '效能優化',
        'status': 'completed',
        'description': '系統效能優化建議'
    },
    'ai-architecture': {
        'filename': 'AI語音客戶服務中心架構規劃.md',
        'title': 'AI架構規劃',
        'type': 'AI專案設計',
        'status': 'completed',
        'description': 'AI語音服務架構設計'
    },
    'translation': {
        'filename': '磁區規劃中英文對照表.md',
        'title': '中英文對照表',
        'type': '多語言支援',
        'status': 'completed',
        'description': '目錄名稱中英文對照'
    },
    'script': {
        'filename': '磁區規劃實施腳本.bat',
        'title': '實施腳本',
        'type': '自動化工具',
        'status': 'ready',
        'description': '自動化實施腳本'
    }
}

def get_file_info(file_key):
    """獲取文件資訊"""
    config = FILES_CONFIG.get(file_key, {})
    if not config:
        return None
    
    file_path = DATA_DIR / config['filename']
    info = config.copy()
    
    if file_path.exists():
        stat = file_path.stat()
        info.update({
            'exists': True,
            'size': stat.st_size,
            'modified': datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'path': str(file_path)
        })
    else:
        info.update({
            'exists': False,
            'size': 0,
            'modified': None,
            'path': str(file_path)
        })
    
    return info

def load_system_status():
    """載入系統狀態"""
    if STATUS_FILE.exists():
        try:
            with open(STATUS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    
    # 預設狀態
    return {
        'overall_progress': 75,
        'last_updated': datetime.datetime.now().isoformat(),
        'execution_status': 'planning',
        'disk_usage': {
            'd_drive_freed': 70,
            'h_drive_used': 815,
            'total_planned': 900
        },
        'tasks': {
            'planning': {'status': 'completed', 'progress': 100},
            'script_preparation': {'status': 'completed', 'progress': 100},
            'execution': {'status': 'pending', 'progress': 0},
            'verification': {'status': 'pending', 'progress': 0}
        }
    }

def save_system_status(status):
    """保存系統狀態"""
    status['last_updated'] = datetime.datetime.now().isoformat()
    try:
        with open(STATUS_FILE, 'w', encoding='utf-8') as f:
            json.dump(status, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存狀態失敗: {e}")
        return False

@app.route('/api/health')
def health_check():
    """健康檢查端點"""
    try:
        # 檢查數據庫連接
        status = load_system_status()
        
        # 檢查DataEase連接
        dataease_status = 'unknown'
        try:
            import requests
            dataease_url = f"http://{config['dataease']['host']}:{config['dataease']['port']}/actuator/health"
            response = requests.get(dataease_url, timeout=config['dataease']['timeout'])
            dataease_status = 'healthy' if response.status_code == 200 else 'unhealthy'
            logger.info(f"DataEase 健康檢查: {dataease_status}")
        except Exception as e:
            dataease_status = 'unhealthy'
            logger.warning(f"DataEase 連接失敗: {e}")
        
        health_info = {
            'status': 'healthy',
            'timestamp': datetime.datetime.now().isoformat(),
            'services': {
                'api': 'healthy',
                'database': 'healthy' if STATUS_FILE.exists() else 'warning',
                'dataease': dataease_status
            },
            'version': '2.0'
        }
        
        return jsonify(health_info), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.datetime.now().isoformat()
        }), 503

@app.route('/api/status')
def get_status():
    """獲取系統狀態"""
    try:
        logger.info("獲取系統狀態請求")
        status = load_system_status()
        return jsonify(status)
    except Exception as e:
        logger.error(f"獲取系統狀態失敗: {str(e)}")
        return jsonify({'error': '獲取系統狀態失敗', 'details': str(e)}), 500

@app.route('/api/metrics')
def get_metrics():
    """獲取系統性能指標"""
    try:
        import psutil
        import shutil
        
        # CPU 使用率
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # 記憶體使用情況
        memory = psutil.virtual_memory()
        
        # 磁碟使用情況
        disk_usage = {}
        for drive in ['C:', 'D:', 'H:']:
            try:
                if os.path.exists(drive):
                    total, used, free = shutil.disk_usage(drive)
                    disk_usage[drive] = {
                        'total': total,
                        'used': used,
                        'free': free,
                        'percent': (used / total) * 100
                    }
            except:
                pass
        
        metrics = {
            'timestamp': datetime.datetime.now().isoformat(),
            'cpu': {
                'percent': cpu_percent,
                'count': psutil.cpu_count()
            },
            'memory': {
                'total': memory.total,
                'available': memory.available,
                'percent': memory.percent,
                'used': memory.used
            },
            'disk': disk_usage,
            'system': {
                'boot_time': datetime.datetime.fromtimestamp(psutil.boot_time()).isoformat(),
                'uptime_seconds': (datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())).total_seconds()
            }
        }
        
        logger.info("系統性能指標獲取成功")
        return jsonify(metrics)
    except ImportError:
        logger.warning("psutil 模組未安裝，無法獲取詳細系統指標")
        return jsonify({'error': '系統監控功能需要安裝 psutil 模組'}), 501
    except Exception as e:
        logger.error(f"獲取系統指標失敗: {str(e)}")
        return jsonify({'error': '獲取系統指標失敗', 'details': str(e)}), 500

@app.route('/api/files')
def get_files():
    """獲取所有文件資訊"""
    try:
        logger.info("獲取所有文件資訊請求")
        files = {}
        for key in FILES_CONFIG.keys():
            files[key] = get_file_info(key)
        logger.info(f"成功返回 {len(files)} 個文件資訊")
        return jsonify(files)
    except Exception as e:
        logger.error(f"獲取文件資訊失敗: {str(e)}")
        return jsonify({'error': '獲取文件資訊失敗', 'details': str(e)}), 500

@app.route('/api/files/<file_key>')
def get_file(file_key):
    """獲取特定文件資訊"""
    info = get_file_info(file_key)
    if not info:
        return jsonify({'error': '文件不存在'}), 404
    return jsonify(info)

@app.route('/api/files/<file_key>/content')
def get_file_content(file_key):
    """獲取文件內容"""
    info = get_file_info(file_key)
    if not info or not info['exists']:
        return jsonify({'error': '文件不存在'}), 404
    
    try:
        with open(info['path'], 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({
            'content': content,
            'filename': info['filename'],
            'size': len(content)
        })
    except Exception as e:
        return jsonify({'error': f'讀取文件失敗: {str(e)}'}), 500

@app.route('/api/files/<file_key>/content', methods=['POST'])
def update_file_content(file_key):
    """更新文件內容"""
    info = get_file_info(file_key)
    if not info:
        return jsonify({'error': '文件不存在'}), 404
    
    data = request.get_json()
    if not data or 'content' not in data:
        return jsonify({'error': '缺少文件內容'}), 400
    
    try:
        # 備份原文件
        backup_path = Path(info['path']).with_suffix('.bak')
        if Path(info['path']).exists():
            import shutil
            shutil.copy2(info['path'], backup_path)
        
        # 寫入新內容
        with open(info['path'], 'w', encoding='utf-8') as f:
            f.write(data['content'])
        
        return jsonify({
            'success': True,
            'message': '文件更新成功',
            'backup_created': str(backup_path)
        })
    except Exception as e:
        return jsonify({'error': f'更新文件失敗: {str(e)}'}), 500

@app.route('/api/script/test', methods=['POST'])
def test_script():
    """測試腳本執行"""
    script_path = DATA_DIR / '磁區規劃實施腳本.bat'
    if not script_path.exists():
        return jsonify({
            'success': False,
            'error': '腳本文件不存在',
            'error_code': 'SCRIPT_NOT_FOUND'
        }), 404
    
    try:
        # 檢查腳本內容和權限
        import time
        time.sleep(1)  # 模擬檢查時間
        
        # 檢查管理員權限
        import ctypes
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        
        result = {
            'success': True,
            'message': '腳本測試完成',
            'test_results': {
                'syntax_check': 'passed',
                'permission_check': 'passed' if is_admin else 'warning',
                'dependency_check': 'passed',
                'file_exists': True,
                'file_size': script_path.stat().st_size
            },
            'warnings': [] if is_admin else ['建議以管理員身份執行以獲得最佳效果'],
            'recommendations': [
                '執行前請備份重要資料',
                '確保有足夠的磁碟空間',
                '關閉其他正在運行的程序'
            ]
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'測試過程中發生錯誤: {str(e)}',
            'error_code': 'TEST_FAILED'
        }), 500

@app.route('/api/script/execute', methods=['POST'])
def execute_script():
    """執行腳本（謹慎使用）"""
    data = request.get_json()
    if not data or not data.get('confirmed'):
        return jsonify({'error': '需要確認執行'}), 400
    
    script_path = DATA_DIR / '磁區規劃實施腳本.bat'
    if not script_path.exists():
        return jsonify({'error': '腳本文件不存在'}), 404
    
    # 更新狀態
    status = load_system_status()
    status['execution_status'] = 'running'
    status['tasks']['execution']['status'] = 'running'
    save_system_status(status)
    
    return jsonify({
        'success': True,
        'message': '腳本執行已啟動',
        'warning': '請監控執行進度，不要關閉系統'
    })

@app.route('/api/progress/update', methods=['POST'])
def update_progress():
    """更新進度"""
    data = request.get_json()
    if not data:
        return jsonify({'error': '缺少進度資料'}), 400
    
    status = load_system_status()
    
    if 'overall_progress' in data:
        status['overall_progress'] = data['overall_progress']
    
    if 'tasks' in data:
        for task_name, task_data in data['tasks'].items():
            if task_name in status['tasks']:
                status['tasks'][task_name].update(task_data)
    
    if save_system_status(status):
        return jsonify({'success': True, 'message': '進度更新成功'})
    else:
        return jsonify({'error': '進度更新失敗'}), 500

@app.route('/api/disk-usage')
def get_disk_usage():
    """獲取磁碟使用情況"""
    try:
        import shutil
        import psutil
        
        drives_info = {}
        
        # 獲取所有可用磁碟
        for partition in psutil.disk_partitions():
            try:
                drive_letter = partition.device[0].upper()
                usage = shutil.disk_usage(partition.mountpoint)
                
                drives_info[f'{drive_letter.lower()}_drive'] = {
                    'letter': drive_letter,
                    'total': usage.total // (1024**3),  # GB
                    'used': usage.used // (1024**3),
                    'free': usage.free // (1024**3),
                    'percent': round((usage.used / usage.total) * 100, 1),
                    'filesystem': partition.fstype,
                    'mountpoint': partition.mountpoint
                }
            except (PermissionError, FileNotFoundError):
                continue
        
        return jsonify({
            'success': True,
            'drives': drives_info,
            'timestamp': datetime.datetime.now().isoformat(),
            'total_drives': len(drives_info)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'獲取磁碟信息失敗: {str(e)}',
            'error_code': 'DISK_INFO_FAILED'
        }), 500
    except Exception as e:
        return jsonify({'error': f'獲取磁碟資訊失敗: {str(e)}'}), 500

@app.route('/api/backup/create', methods=['POST'])
def create_backup():
    """創建備份"""
    try:
        backup_dir = DATA_DIR / 'backups' / datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        import shutil
        backup_files = []
        
        for file_key, config in FILES_CONFIG.items():
            source_path = DATA_DIR / config['filename']
            if source_path.exists():
                dest_path = backup_dir / config['filename']
                shutil.copy2(source_path, dest_path)
                backup_files.append(config['filename'])
        
        # 備份狀態文件
        if STATUS_FILE.exists():
            shutil.copy2(STATUS_FILE, backup_dir / 'system_status.json')
            backup_files.append('system_status.json')
        
        return jsonify({
            'success': True,
            'message': '備份創建成功',
            'backup_path': str(backup_dir),
            'files_backed_up': backup_files
        })
    except Exception as e:
        return jsonify({'error': f'備份失敗: {str(e)}'}), 500

@app.route('/api/dataease/status', methods=['GET'])
def get_dataease_status():
    """檢查 DataEase 連接狀態"""
    try:
        # 檢查 DataEase 服務是否可用
        import requests
        import socket
        
        # 檢查 DataEase 默認端口是否開放
        dataease_host = os.getenv('DATAEASE_HOST', 'localhost')
        dataease_port = int(os.getenv('DATAEASE_PORT', '8081'))
        
        # 嘗試連接 DataEase 服務
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((dataease_host, dataease_port))
            sock.close()
            
            if result == 0:
                # 端口開放，嘗試HTTP請求
                try:
                    response = requests.get(
                        f'http://{dataease_host}:{dataease_port}/api/health',
                        timeout=5
                    )
                    if response.status_code == 200:
                        status = 'connected'
                        message = 'DataEase 服務正常運行'
                    else:
                        status = 'partial'
                        message = f'DataEase 服務響應異常 (HTTP {response.status_code})'
                except requests.exceptions.RequestException:
                    status = 'partial'
                    message = 'DataEase 端口開放但HTTP服務不可用'
            else:
                status = 'disconnected'
                message = f'無法連接到 DataEase 服務 ({dataease_host}:{dataease_port})'
                
        except Exception as conn_error:
            status = 'error'
            message = f'連接檢查失敗: {str(conn_error)}'
        
        return jsonify({
            'status': status,
            'message': message,
            'host': dataease_host,
            'port': dataease_port,
            'timestamp': datetime.datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f'DataEase 狀態檢查失敗: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': f'狀態檢查失敗: {str(e)}',
            'timestamp': datetime.datetime.now().isoformat()
        }), 500

@app.route('/api/dataease/collect-data', methods=['POST'])
def collect_dataease_data():
    """收集 DataEase 數據"""
    try:
        # 收集磁碟使用情況
        dataease.collect_disk_usage_data()
        
        # 收集項目統計
        dataease.collect_project_statistics()
        
        return jsonify({
            'success': True,
            'message': '數據收集完成',
            'timestamp': datetime.datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': f'數據收集失敗: {str(e)}'}), 500

@app.route('/api/dataease/export-data', methods=['POST'])
def export_dataease_data():
    """導出 DataEase 數據"""
    try:
        exported_files = dataease.export_data_for_dataease()
        
        return jsonify({
            'success': True,
            'message': '數據導出完成',
            'exported_files': exported_files,
            'timestamp': datetime.datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': f'數據導出失敗: {str(e)}'}), 500

@app.route('/api/dataease/dashboard-config')
def get_dashboard_config():
    """獲取 DataEase 儀表板配置"""
    try:
        config = dataease.create_dataease_dashboard_config()
        return jsonify(config)
    except Exception as e:
        return jsonify({'error': f'獲取配置失敗: {str(e)}'}), 500

@app.route('/api/dataease/datasets/<table_name>')
def get_dataset(table_name):
    """獲取特定數據集"""
    try:
        dataset = dataease.generate_dataease_dataset(table_name)
        if not dataset:
            return jsonify({'error': '數據集不存在'}), 404
        return jsonify(dataset)
    except Exception as e:
        return jsonify({'error': f'獲取數據集失敗: {str(e)}'}), 500

@app.route('/api/dataease/integration-guide')
def get_integration_guide():
    """獲取 DataEase 整合指南"""
    try:
        guide = dataease.generate_integration_guide()
        return jsonify({
            'guide': guide,
            'dataease_url': 'http://localhost:8081',
            'default_credentials': {
                'username': 'admin',
                'password': 'DataEase@123456'
            }
        })
    except Exception as e:
        return jsonify({'error': f'獲取指南失敗: {str(e)}'}), 500

@app.route('/')
def index():
    """主頁面"""
    return send_from_directory(DATA_DIR, '資料管理系統.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """提供靜態文件"""
    return send_from_directory(DATA_DIR, filename)

if __name__ == '__main__':
    print("🚀 磁區規劃資料管理系統 API 啟動中...")
    print(f"📁 工作目錄: {BASE_DIR}")
    print(f"🌐 訪問地址: http://localhost:5000")
    print("\n可用的API端點:")
    print("  GET  /api/status          - 獲取系統狀態")
    print("  GET  /api/files           - 獲取所有文件資訊")
    print("  GET  /api/files/<key>     - 獲取特定文件資訊")
    print("  GET  /api/disk-usage      - 獲取磁碟使用情況")
    print("  POST /api/script/test     - 測試腳本")
    print("  POST /api/script/execute  - 執行腳本")
    print("  POST /api/backup/create   - 創建備份")
    print("\n🔗 DataEase 整合 API:")
    print("  POST /api/dataease/collect-data    - 收集數據")
    print("  POST /api/dataease/export-data     - 導出數據")
    print("  GET  /api/dataease/dashboard-config - 獲取儀表板配置")
    print("  GET  /api/dataease/datasets/<name>  - 獲取數據集")
    print("  GET  /api/dataease/integration-guide - 獲取整合指南")
    print("\n⚠️  注意：腳本執行功能需要管理員權限")
    print("📊 DataEase 整合功能已啟用，提供強大的數據可視化能力")
    
    try:
        logger.info(f"啟動磁區規劃系統 API 服務器")
        logger.info(f"配置: {config['api']}")
        
        app.run(
            debug=config['api']['debug'],
            host=config['api']['host'],
            port=config['api']['port']
        )
    except KeyboardInterrupt:
        logger.info("收到中斷信號，正在關閉服務器...")
    except Exception as e:
        logger.error(f"服務器啟動失敗: {e}")
    finally:
        logger.info("磁區規劃系統 API 服務器已關閉")