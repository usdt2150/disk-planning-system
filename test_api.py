#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
磁區規劃系統 API 單元測試
"""

import unittest
import json
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# 設置測試環境
os.environ['TESTING'] = 'True'

from api import app, load_system_status, save_system_status, get_file_info

class TestDiskPlanningAPI(unittest.TestCase):
    """磁區規劃系統 API 測試類"""
    
    def setUp(self):
        """測試前設置"""
        self.app = app.test_client()
        self.app.testing = True
        
        # 創建臨時測試目錄
        self.test_dir = tempfile.mkdtemp()
        self.test_status_file = Path(self.test_dir) / 'test_status.json'
    
    def tearDown(self):
        """測試後清理"""
        import shutil
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_health_endpoint(self):
        """測試健康檢查端點"""
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertIn('timestamp', data)
        self.assertIn('services', data)
        self.assertIn('api', data['services'])
        self.assertIn('database', data['services'])
        self.assertIn('dataease', data['services'])
    
    def test_status_endpoint(self):
        """測試狀態端點"""
        response = self.app.get('/api/status')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('overall_progress', data)
        self.assertIn('execution_status', data)
        self.assertIn('disk_usage', data)
    
    def test_files_endpoint(self):
        """測試文件列表端點"""
        response = self.app.get('/api/files')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
    
    def test_metrics_endpoint(self):
        """測試系統指標端點"""
        response = self.app.get('/api/metrics')
        # 可能返回200或501（如果psutil未安裝）
        self.assertIn(response.status_code, [200, 501])
        
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertIn('timestamp', data)
            self.assertIn('cpu', data)
            self.assertIn('memory', data)
    
    def test_system_status_functions(self):
        """測試系統狀態相關函數"""
        # 測試預設狀態
        status = load_system_status()
        self.assertIsInstance(status, dict)
        self.assertIn('overall_progress', status)
        
        # 測試保存狀態
        test_status = {'test': 'value', 'overall_progress': 50}
        with patch('api.STATUS_FILE', self.test_status_file):
            save_system_status(test_status)
            loaded_status = load_system_status()
            self.assertEqual(loaded_status['test'], 'value')
    
    @patch('requests.get')
    def test_dataease_health_check(self, mock_get):
        """測試 DataEase 健康檢查"""
        # 模擬成功響應
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        response = self.app.get('/api/health')
        data = json.loads(response.data)
        
        # 檢查是否調用了 DataEase 健康檢查
        mock_get.assert_called()
    
    def test_error_handling(self):
        """測試錯誤處理"""
        # 測試不存在的端點
        response = self.app.get('/api/nonexistent')
        self.assertEqual(response.status_code, 404)
        
        # 測試不存在的文件
        response = self.app.get('/api/files/nonexistent_file')
        self.assertEqual(response.status_code, 404)  # 應該返回404錯誤

class TestUtilityFunctions(unittest.TestCase):
    """工具函數測試類"""
    
    def test_get_file_info(self):
        """測試文件信息獲取函數"""
        # 測試存在的配置項
        info = get_file_info('readme')
        if info is not None:
            self.assertIsInstance(info, dict)
            self.assertIn('exists', info)
            self.assertIn('path', info)
        
        # 測試不存在的配置項
        info = get_file_info('nonexistent')
        self.assertIsNone(info)

if __name__ == '__main__':
    # 運行測試
    unittest.main(verbosity=2)