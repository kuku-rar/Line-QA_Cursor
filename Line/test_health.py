#!/usr/bin/env python3
"""
簡單的健康檢查測試腳本
用於驗證部署後的服務狀態
"""

import requests
import sys
import json
from datetime import datetime

def test_health_endpoint(base_url):
    """測試健康檢查端點"""
    try:
        print(f"🔍 測試健康檢查端點: {base_url}/health")
        response = requests.get(f"{base_url}/health", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 健康檢查通過")
            print(f"   狀態: {data.get('status')}")
            print(f"   時間戳: {data.get('timestamp')}")
            return True
        else:
            print(f"❌ 健康檢查失敗 - HTTP {response.status_code}")
            print(f"   回應: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 連線失敗: {e}")
        return False

def test_survey_page(base_url):
    """測試問卷頁面是否可存取"""
    try:
        print(f"🔍 測試問卷頁面: {base_url}/survey")
        response = requests.get(f"{base_url}/survey", timeout=10)
        
        if response.status_code == 200:
            print("✅ 問卷頁面可正常存取")
            return True
        else:
            print(f"❌ 問卷頁面無法存取 - HTTP {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 連線失敗: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("用法: python test_health.py <base_url>")
        print("範例: python test_health.py https://your-project.zeabur.app")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    
    print(f"🚀 開始測試 LINE 健康問卷系統")
    print(f"📍 目標網址: {base_url}")
    print(f"⏰ 測試時間: {datetime.now()}")
    print("-" * 50)
    
    tests_passed = 0
    total_tests = 2
    
    # 測試健康檢查端點
    if test_health_endpoint(base_url):
        tests_passed += 1
    print()
    
    # 測試問卷頁面
    if test_survey_page(base_url):
        tests_passed += 1
    print()
    
    # 總結
    print("-" * 50)
    print(f"📊 測試結果: {tests_passed}/{total_tests} 通過")
    
    if tests_passed == total_tests:
        print("🎉 所有測試通過！系統運行正常")
        sys.exit(0)
    else:
        print("⚠️ 部分測試失敗，請檢查系統狀態")
        sys.exit(1)

if __name__ == "__main__":
    main()