#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
圖片遷移腳本 - 將外部圖床的圖片上傳到 BookStack 並更新連結
"""

import os
import re
import requests
import hashlib
from urllib.parse import urlparse, unquote
from pathlib import Path
import time
import json
from datetime import datetime
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class ImageMigrator:
    def __init__(self, markdown_dir, bookstack_url, bookstack_token, page_id=None):
        self.markdown_dir = Path(markdown_dir)
        self.bookstack_url = bookstack_url.rstrip('/')
        self.bookstack_token = bookstack_token
        self.page_id = page_id or 2  # 預設使用頁面 ID 2，匹配 curl 範例
        
        # 支援的圖片格式
        self.image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.bmp'}
        
        # 外部圖床 URL 模式
        self.external_patterns = [
            r'https://markweb\.idv\.tw/uploads/([^)]+)',
            r'https://raw\.githubusercontent\.com/([^)]+)'
        ]
        
        # 儲存已上傳的圖片映射 {原始URL: BookStack URL}
        self.uploaded_images = {}
        
        # 解析 Token (格式: TOKEN_ID:TOKEN_SECRET)
        if ':' in self.bookstack_token:
            # 使用正確的 Authorization 格式: "Token YOUR_ID:YOUR_SECRET"
            self.token_format = f'Token {self.bookstack_token}'
        else:
            # 如果用戶只提供了一部分，提示正確格式
            print("⚠️ 警告: Token 格式可能不正確")
            print("正確格式應為: TOKEN_ID:TOKEN_SECRET")
            self.token_format = f'Token {self.bookstack_token}'
            
        # BookStack API headers  
        self.headers = {
            'Authorization': self.token_format,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        # 當前月份用於路徑
        self.current_month = datetime.now().strftime('%Y-%m')
        
        # 創建 session 以保持連線
        self.session = requests.Session()
        
        # 設定重試策略
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # 為 session 設定 headers
        self.session.headers.update(self.headers)
        
    def test_api_connection(self):
        """測試 BookStack API 連線"""
        try:
            # 測試基本 API 訪問
            test_url = f"{self.bookstack_url}/api/docs"
            response = self.session.get(test_url, timeout=10)
            
            if response.status_code == 200:
                print("✓ BookStack API 連線成功")
                return True
            else:
                print(f"✗ BookStack API 連線失敗: {response.status_code}")
                if response.status_code == 403:
                    self.handle_permission_error(response)
                return False
        except Exception as e:
            print(f"✗ 無法連接到 BookStack API: {e}")
            return False
    
            
    def handle_permission_error(self, response):
        """處理權限錯誤並提供解決方案"""
        try:
            error_data = response.json()
            error_msg = error_data.get('error', {}).get('message', '未知錯誤')
            print(f"錯誤詳情: {error_msg}")
        except:
            print(f"錯誤詳情: HTTP {response.status_code}")
            
        print("\n解決方案:")
        print("1. 確認您已登入 BookStack 並具有管理員權限")
        print("2. 前往 BookStack -> 設定 -> API Tokens")
        print("3. 創建新的 API Token，確保:")
        print("   - Token 名稱: ImageMigrator")
        print("   - 過期時間: 設定為適當的時間")
        print("   - 權限: 確保包含 'Create/Update/Delete Images' 權限")
        print("4. 使用新創建的 Token 重新執行腳本")
        print("5. 如果問題持續，請檢查 BookStack 版本是否支援 Image Gallery API")
        
    def find_external_images(self):
        """掃描所有 markdown 文件，找出外部圖片連結"""
        external_images = set()
        
        for md_file in self.markdown_dir.rglob('*.md'):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 查找圖片連結 ![alt](url)
                image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
                matches = re.findall(image_pattern, content)
                
                for alt_text, url in matches:
                    # 檢查是否為外部圖片
                    for pattern in self.external_patterns:
                        if re.search(pattern, url):
                            external_images.add(url.strip())
                            print(f"發現外部圖片: {url}")
                            
            except Exception as e:
                print(f"讀取文件 {md_file} 時發生錯誤: {e}")
        
        return external_images
    
    def generate_local_filename(self, url):
        """為圖片生成本地檔名"""
        # 解析 URL
        parsed = urlparse(url)
        original_filename = os.path.basename(unquote(parsed.path))
        
        # 如果沒有副檔名，嘗試從 URL 推測
        if not any(original_filename.lower().endswith(ext) for ext in self.image_extensions):
            original_filename += '.png'  # 預設為 PNG
        
        # 使用 URL 的 hash 作為前綴，避免檔名衝突
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        
        # 保留原始檔名，但加上 hash 前綴
        name, ext = os.path.splitext(original_filename)
        local_filename = f"{url_hash}_{name}{ext}"
        
        return local_filename
    
    def download_and_upload_image(self, url):
        """下載圖片並上傳到 BookStack"""
        try:
            # 檢查是否已經上傳過
            if url in self.uploaded_images:
                return self.uploaded_images[url]
            
            print(f"正在處理: {url}")
            
            # 下載圖片
            download_headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Sec-Fetch-Dest': 'image',
                'Sec-Fetch-Mode': 'no-cors',
                'Sec-Fetch-Site': 'cross-site'
            }
            
            # 加入重試機制
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # 為下載請求創建獨立的 session
                    download_session = requests.Session()
                    download_session.headers.update(download_headers)
                    response = download_session.get(url, timeout=30)
                    response.raise_for_status()
                    break
                except requests.RequestException as e:
                    if attempt == max_retries - 1:
                        raise e
                    print(f"下載失敗，正在重試 ({attempt + 1}/{max_retries}): {e}")
                    time.sleep(2)  # 等待 2 秒後重試
            
            # 生成檔名
            original_filename = self.generate_local_filename(url)
            
            # 上傳到 BookStack
            bookstack_url = self.upload_to_bookstack(response.content, original_filename)
            
            if bookstack_url:
                print(f"已上傳: {original_filename} -> {bookstack_url}")
                self.uploaded_images[url] = bookstack_url
                
                # 避免過於頻繁的請求
                time.sleep(1)
                
                return bookstack_url
            else:
                print(f"上傳失敗: {url}")
                return None
                
        except Exception as e:
            print(f"處理圖片失敗 {url}: {e}")
            return None
    
    def upload_to_bookstack(self, image_data, filename):
        """上傳圖片到 BookStack 圖片庫"""
        try:
            # BookStack 圖片上傳 API 端點
            upload_url = f"{self.bookstack_url}/api/image-gallery"
            
            print(f"DEBUG: 上傳到 {upload_url}")
            print(f"DEBUG: Authorization: {self.token_format}")
            print(f"DEBUG: 參數 - type=gallery, uploaded_to={self.page_id}")
            print(f"DEBUG: 檔案名稱: {filename}")
            
            # 準備檔案上傳 - 完全匹配 curl 命令格式
            files = {
                'image': (filename, image_data, self.get_content_type(filename))
            }
            
            # 完全匹配 curl 的 -F 參數
            data = {
                'type': 'gallery',
                'uploaded_to': str(self.page_id)
            }
            
            # 直接使用 requests.post，不使用 session
            response = requests.post(
                upload_url,
                headers={
                    'Authorization': self.token_format,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                },
                files=files,
                data=data,
                timeout=30
            )
            
            print(f"HTTP 狀態碼: {response.status_code}")
            
            if response.status_code in [200, 201]:
                try:
                    result = response.json()
                    print(f"成功! API 回應: {result}")
                    
                    # 從回應中取得圖片 URL
                    if 'url' in result:
                        return result['url']
                    elif 'path' in result:
                        return f"{self.bookstack_url}{result['path']}"
                    else:
                        # 如果沒有明確的 URL，嘗試構建一個
                        return f"{self.bookstack_url}/uploads/images/gallery/{filename}"
                        
                except ValueError:
                    print("回應不是有效的 JSON")
                    return f"{self.bookstack_url}/uploads/images/gallery/{filename}"
            else:
                print(f"上傳失敗! HTTP {response.status_code}")
                print(f"回應內容: {response.text}")
                return None
                
        except Exception as e:
            print(f"上傳異常: {e}")
            return None
    
    def get_content_type(self, filename):
        """根據檔案副檔名獲取 MIME 類型"""
        ext = os.path.splitext(filename)[1].lower()
        content_types = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.webp': 'image/webp',
            '.svg': 'image/svg+xml',
            '.bmp': 'image/bmp'
        }
        return content_types.get(ext, 'image/png')
    
    def update_markdown_files(self):
        """更新所有 markdown 文件中的圖片連結"""
        updated_files = 0
        total_replacements = 0
        
        for md_file in self.markdown_dir.rglob('*.md'):
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                file_replacements = 0
                
                # 替換圖片連結
                for original_url, bookstack_url in self.uploaded_images.items():
                    old_pattern = f"]({original_url})"
                    new_pattern = f"]({bookstack_url})"
                    
                    if old_pattern in content:
                        count_before = content.count(old_pattern)
                        content = content.replace(old_pattern, new_pattern)
                        count_after = content.count(old_pattern)
                        replacements = count_before - count_after
                        file_replacements += replacements
                
                # 如果有變更，寫回文件
                if content != original_content:
                    with open(md_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"已更新: {md_file} ({file_replacements} 個連結)")
                    updated_files += 1
                    total_replacements += file_replacements
                    
            except Exception as e:
                print(f"更新文件 {md_file} 時發生錯誤: {e}")
        
        return updated_files, total_replacements
    
    def migrate(self):
        """執行完整的圖片遷移流程"""
        print("測試 BookStack API 連線...")
        if not self.test_api_connection():
            print("錯誤：無法連接到 BookStack API，請檢查 URL 和 Token")
            return 0, 0, 0
            
        print("開始掃描外部圖片...")
        external_images = self.find_external_images()
        
        if not external_images:
            print("沒有找到外部圖片連結")
            return
        
        print(f"找到 {len(external_images)} 個外部圖片")
        print()
        
        print("開始下載並上傳圖片到 BookStack...")
        success_count = 0
        for url in external_images:
            if self.download_and_upload_image(url):
                success_count += 1
        
        print(f"成功下載 {success_count}/{len(external_images)} 個圖片")
        print()
        
        if success_count > 0:
            print("開始更新 markdown 文件...")
            updated_files, total_replacements = self.update_markdown_files()
            print(f"已更新 {updated_files} 個文件，總共替換 {total_replacements} 個連結")
        else:
            updated_files, total_replacements = 0, 0
        
        print("圖片遷移完成！")
        return success_count, updated_files, total_replacements

def main():
    # 設定參數
    markdown_dir = "E:/Project/NOTE/bookstack/scripts/markdown"
    bookstack_url = "https://mybookstack.zeabur.app"
    
    print("🔧 BookStack 圖片遷移工具")
    print("=" * 50)
    
    # BookStack API Token (需要從 BookStack 設定中獲取)
    print("\n📋 請提供以下資訊:")
    print("1. BookStack API Token (格式: TOKEN_ID:TOKEN_SECRET)")
    print("2. 頁面 ID (圖片將上傳到此頁面，預設為 2)")
    print("\n📝 此腳本等同於執行以下 curl 命令:")
    print('curl -X POST "https://mybookstack.zeabur.app/api/image-gallery" \\')
    print('  -H "Authorization: Token YOUR_ID:YOUR_SECRET" \\')
    print('  -F "type=gallery" \\')
    print('  -F "uploaded_to=2" \\')
    print('  -F "image=@/path/to/your/image.png"')
    print()
    
    bookstack_token = input("請輸入 BookStack API Token: ").strip()
    
    if not bookstack_token:
        print("❌ 錯誤：需要提供 BookStack API Token")
        print("\n📝 如何獲取 Token:")
        print("1. 登入 BookStack -> 個人設定 -> API Tokens")
        print("2. 創建新 Token，格式會是: ttk_xxxxxx:yyyyyyy")
        print("3. 確保帳號有圖片管理權限")
        return
    
    # 獲取頁面 ID
    page_id_input = input("請輸入頁面 ID (預設為 2): ").strip()
    try:
        page_id = int(page_id_input) if page_id_input else 2
        print(f"✅ 將使用頁面 ID: {page_id}")
    except ValueError:
        print("⚠️ 頁面 ID 格式錯誤，使用預設值 2")
        page_id = 2
    
    # 檢查路徑是否存在
    if not os.path.exists(markdown_dir):
        print(f"Markdown 目錄不存在: {markdown_dir}")
        return
    
    # 執行遷移
    print(f"\n🚀 開始執行遷移...")
    print(f"📁 Markdown 目錄: {markdown_dir}")
    print(f"🌐 BookStack URL: {bookstack_url}")
    print(f"📄 目標頁面 ID: {page_id}")
    print()
    
    migrator = ImageMigrator(markdown_dir, bookstack_url, bookstack_token, page_id)
    success_count, updated_files, total_replacements = migrator.migrate()
    
    print(f"\n=== 遷移結果 ===")
    print(f"上傳圖片: {success_count}")
    print(f"更新文件: {updated_files}")
    print(f"替換連結: {total_replacements}")

if __name__ == "__main__":
    main()