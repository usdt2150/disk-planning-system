#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
磁區規劃系統部署和維護腳本
"""

import os
import sys
import json
import shutil
import subprocess
import datetime
import argparse
from pathlib import Path

class DiskPlanningDeployer:
    """磁區規劃系統部署器"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.backup_dir = self.base_dir / 'backups'
        self.logs_dir = self.base_dir / 'logs'
        
        # 確保目錄存在
        self.backup_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
    
    def log(self, message, level='INFO'):
        """記錄日誌"""
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] [{level}] {message}"
        print(log_message)
        
        # 寫入日誌文件
        log_file = self.logs_dir / 'deploy.log'
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_message + '\n')
    
    def run_command(self, command, cwd=None):
        """執行命令"""
        try:
            self.log(f"執行命令: {command}")
            result = subprocess.run(
                command, 
                shell=True, 
                cwd=cwd or self.base_dir,
                capture_output=True, 
                text=True,
                encoding='utf-8'
            )
            
            if result.returncode == 0:
                self.log(f"命令執行成功: {result.stdout.strip()}")
                return True, result.stdout
            else:
                self.log(f"命令執行失敗: {result.stderr.strip()}", 'ERROR')
                return False, result.stderr
        except Exception as e:
            self.log(f"命令執行異常: {str(e)}", 'ERROR')
            return False, str(e)
    
    def check_dependencies(self):
        """檢查依賴項"""
        self.log("檢查系統依賴項...")
        
        dependencies = {
            'python': 'python --version',
            'docker': 'docker --version',
            'docker-compose': 'docker-compose --version',
            'node': 'node --version',
            'npm': 'npm --version'
        }
        
        missing = []
        for name, command in dependencies.items():
            success, output = self.run_command(command)
            if success:
                self.log(f"✓ {name}: {output.strip()}")
            else:
                self.log(f"✗ {name}: 未安裝或不可用", 'WARNING')
                missing.append(name)
        
        if missing:
            self.log(f"缺少依賴項: {', '.join(missing)}", 'WARNING')
            return False
        
        return True
    
    def backup_data(self):
        """備份數據"""
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"backup_{timestamp}"
        backup_path = self.backup_dir / backup_name
        
        self.log(f"開始備份數據到: {backup_path}")
        
        try:
            backup_path.mkdir(exist_ok=True)
            
            # 備份配置文件
            config_files = ['config.json', 'system_status.json', '.env']
            for config_file in config_files:
                src = self.base_dir / config_file
                if src.exists():
                    shutil.copy2(src, backup_path)
                    self.log(f"已備份: {config_file}")
            
            # 備份數據庫
            db_file = self.base_dir / 'disk_planning_data.db'
            if db_file.exists():
                shutil.copy2(db_file, backup_path)
                self.log("已備份: 數據庫文件")
            
            # 備份日誌
            if self.logs_dir.exists():
                shutil.copytree(self.logs_dir, backup_path / 'logs', dirs_exist_ok=True)
                self.log("已備份: 日誌文件")
            
            self.log(f"備份完成: {backup_path}")
            return True, backup_path
            
        except Exception as e:
            self.log(f"備份失敗: {str(e)}", 'ERROR')
            return False, None
    
    def install_dependencies(self):
        """安裝Python依賴項"""
        self.log("安裝Python依賴項...")
        
        success, output = self.run_command('pip install -r requirements.txt')
        if success:
            self.log("Python依賴項安裝成功")
            return True
        else:
            self.log("Python依賴項安裝失敗", 'ERROR')
            return False
    
    def build_frontend(self):
        """構建前端"""
        frontend_dir = self.base_dir / 'frontend'
        if not frontend_dir.exists():
            self.log("前端目錄不存在，跳過前端構建")
            return True
        
        self.log("構建前端應用...")
        
        # 安裝前端依賴
        success, output = self.run_command('npm install', cwd=frontend_dir)
        if not success:
            self.log("前端依賴安裝失敗", 'ERROR')
            return False
        
        # 構建前端
        success, output = self.run_command('npm run build', cwd=frontend_dir)
        if success:
            self.log("前端構建成功")
            return True
        else:
            self.log("前端構建失敗", 'ERROR')
            return False
    
    def deploy_docker(self):
        """Docker部署"""
        self.log("開始Docker部署...")
        
        # 停止現有容器
        self.run_command('docker-compose down')
        
        # 構建並啟動容器
        success, output = self.run_command('docker-compose up -d --build')
        if success:
            self.log("Docker部署成功")
            return True
        else:
            self.log("Docker部署失敗", 'ERROR')
            return False
    
    def health_check(self):
        """健康檢查"""
        self.log("執行健康檢查...")
        
        import time
        import requests
        
        # 等待服務啟動
        time.sleep(30)
        
        endpoints = {
            'API': 'http://localhost:5000/api/health',
            'Frontend': 'http://localhost:3002',
            'DataEase': 'http://localhost:8081/actuator/health'
        }
        
        all_healthy = True
        for name, url in endpoints.items():
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    self.log(f"✓ {name}: 健康")
                else:
                    self.log(f"✗ {name}: 不健康 (狀態碼: {response.status_code})", 'WARNING')
                    all_healthy = False
            except Exception as e:
                self.log(f"✗ {name}: 連接失敗 ({str(e)})", 'WARNING')
                all_healthy = False
        
        return all_healthy
    
    def deploy(self, mode='development'):
        """完整部署流程"""
        self.log(f"開始部署磁區規劃系統 (模式: {mode})")
        
        # 1. 檢查依賴項
        if not self.check_dependencies():
            self.log("依賴項檢查失敗，部署中止", 'ERROR')
            return False
        
        # 2. 備份數據
        backup_success, backup_path = self.backup_data()
        if not backup_success:
            self.log("數據備份失敗，部署中止", 'ERROR')
            return False
        
        # 3. 安裝依賴項
        if not self.install_dependencies():
            self.log("依賴項安裝失敗，部署中止", 'ERROR')
            return False
        
        # 4. 構建前端
        if not self.build_frontend():
            self.log("前端構建失敗，部署中止", 'ERROR')
            return False
        
        # 5. Docker部署
        if mode == 'docker':
            if not self.deploy_docker():
                self.log("Docker部署失敗", 'ERROR')
                return False
        
        # 6. 健康檢查
        if not self.health_check():
            self.log("健康檢查失敗，請檢查服務狀態", 'WARNING')
        
        self.log("部署完成！")
        return True

def main():
    parser = argparse.ArgumentParser(description='磁區規劃系統部署工具')
    parser.add_argument('action', choices=['deploy', 'backup', 'health'], 
                       help='執行的操作')
    parser.add_argument('--mode', choices=['development', 'docker'], 
                       default='development', help='部署模式')
    
    args = parser.parse_args()
    
    deployer = DiskPlanningDeployer()
    
    if args.action == 'deploy':
        success = deployer.deploy(args.mode)
        sys.exit(0 if success else 1)
    elif args.action == 'backup':
        success, _ = deployer.backup_data()
        sys.exit(0 if success else 1)
    elif args.action == 'health':
        success = deployer.health_check()
        sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()