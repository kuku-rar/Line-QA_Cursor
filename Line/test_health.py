#!/usr/bin/env python3
"""
簡單的健康檢查測試腳本
用於驗證部署後的服務狀態
"""

import requests
import sys

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

def test_api_endpoints(base_url):
    """測試 API 端點是否可用"""
    endpoints = [
        "/api/user/sync",
        "/api/survey/submit"
    ]
    
    print("🔍 測試 API 端點...")
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            # API 端點可能回傳 405 (Method Not Allowed) 因為需要 POST
            if response.status_code in [405, 400]:
                print(f"✅ API 端點可用: {endpoint}")
            else:
                print(f"⚠️ API 端點狀態異常: {endpoint} - HTTP {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ API 端點無法存取: {endpoint} - {e}")

def main():
    if len(sys.argv) != 2:
        print("用法: python test_health.py <base_url>")
        print("範例: python test_health.py https://your-project.zeabur.app")
        print("本地測試: python test_health.py http://localhost:8080")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    
    print("🚀 開始測試 LINE 健康問卷系統")
    print(f"📍 目標網址: {base_url}")
    print(f"⏰ 測試時間: {datetime.now()}")
    print("-" * 50)
    
    tests_passed = 0
    total_tests = 3
    
    # 測試健康檢查端點
    if test_health_endpoint(base_url):
        tests_passed += 1
    print()
    
    # 測試問卷頁面
    if test_survey_page(base_url):
        tests_passed += 1
    print()
    
    # 測試 API 端點
    try:
        test_api_endpoints(base_url)
        tests_passed += 1
        print("✅ API 端點測試完成")
    except Exception as e:
        print(f"❌ API 端點測試失敗: {e}")
    print()
    
    # 總結
    print("-" * 50)
    print(f"📊 測試結果: {tests_passed}/{total_tests} 通過")
    
    if tests_passed == total_tests:
        print("🎉 所有測試通過！系統運行正常")
        print("📝 下一步：")
        print("   1. 在 Zeabur 專案中設定環境變數")
        print("   2. 確認 MySQL 服務正常運行")
        print("   3. 設定 LINE LIFF 的 Endpoint URL")
        sys.exit(0)
    else:
        print("⚠️ 部分測試失敗，請檢查系統狀態")
        print("🔍 建議檢查項目：")
        print("   - Zeabur 服務是否正常啟動")
        print("   - 環境變數是否正確設定")
        print("   - MySQL 資料庫是否可連線")
        sys.exit(1)

if __name__ == "__main__":
    main()