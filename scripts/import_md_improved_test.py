#!/usr/bin/env python3
import os
import requests
import hashlib

# 從環境變數讀取設定
API_URL = os.getenv("BOOKSTACK_API_URL", "https://mybookstack.zeabur.app/api")
TOKEN_ID = os.getenv("BOOKSTACK_TOKEN_ID", "fd4vO13WKGyHC1ydfEPCNMMjirpAkpjH")
TOKEN_SECRET = os.getenv("BOOKSTACK_TOKEN_SECRET", "I6ZxNWwYCBnRHr6QwRvhFEHanN59UT8s")
MD_DIR = os.getenv("BOOKSTACK_MD_DIR", "E:/Project/NOTE/bookstack/scripts/markdown")

# 測試用：只處理 AI 目錄
TEST_DIR = "AI"

session = requests.Session()
session.headers.update({
    "Authorization": f"Token {TOKEN_ID}:{TOKEN_SECRET}",
    "Content-Type": "application/json"
})


def get_content_hash(content):
    """計算內容的 MD5 雜湊值，用於比較是否有變更"""
    return hashlib.md5(content.encode('utf-8')).hexdigest()


def check_api_permissions():
    """檢查 API 權限"""
    try:
        r = session.get(f"{API_URL}/books")
        if r.status_code == 403:
            print("❌ API Token 權限不足，請檢查以下設定：")
            print("   1. 登入 BookStack 管理後台")
            print("   2. 前往 Settings > Users > [你的用戶]")
            print("   3. 確認具備 'Access system API' 權限")
            print("   4. 確認具備 'Create/Edit books/chapters/pages' 權限")
            return False
        elif r.status_code == 401:
            print("❌ API Token 無效，請重新生成")
            return False
        elif r.status_code != 200:
            print(f"❌ API 連線錯誤: {r.text}")
            return False
        return True
    except Exception as e:
        print(f"❌ 無法連線到 BookStack: {e}")
        return False




def create_or_update_book(name):
    """建立或更新書籍"""
    try:
        # 先檢查書籍是否存在
        books_response = session.get(f"{API_URL}/books")
        if books_response.status_code == 200:
            books = books_response.json().get("data", [])
            for book in books:
                if book["name"] == name:
                    print(f"📚 已存在書籍: {name}")
                    return book["id"]
        
        # 書籍不存在，建立新書籍
        r = session.post(f"{API_URL}/books", json={"name": name})
        if r.status_code == 200:
            print(f"📚 建立書籍: {name}")
            return r.json()["id"]
        else:
            print(f"❌ 建立書籍失敗 {name}: {r.text}")
            return None
    except Exception as e:
        print(f"❌ 處理書籍時發生錯誤: {e}")
        return None


def create_or_update_chapter(book_id, name):
    """建立或更新章節"""
    try:
        print(f"  📖 檢查章節: {name} (書籍ID: {book_id})")
        # 先檢查章節是否存在 - 使用正確的 API 端點 GET /api/books/{id}
        book_response = session.get(f"{API_URL}/books/{book_id}")
        if book_response.status_code == 200:
            book_data = book_response.json()
            # 檢查書籍內容中的章節
            contents = book_data.get("contents", [])
            for item in contents:
                if item.get("type") == "chapter" and item.get("name") == name:
                    print(f"  📖 已存在章節: {name} (ID: {item['id']})")
                    return item["id"]
        
        # 章節不存在，建立新章節
        r = session.post(f"{API_URL}/chapters", json={"book_id": book_id, "name": name})
        if r.status_code == 200:
            chapter_id = r.json()["id"]
            print(f"  📖 建立新章節: {name} (ID: {chapter_id})")
            return chapter_id
        else:
            print(f"❌ 建立章節失敗 {name}: {r.text}")
            return None
    except Exception as e:
        print(f"❌ 處理章節時發生錯誤: {e}")
        return None


def create_or_update_page(book_id, chapter_id, name, markdown):
    """建立或更新頁面"""
    try:
        print(f"    📝 檢查頁面: {name} (章節ID: {chapter_id}, 書籍ID: {book_id})")
        # 先檢查頁面是否存在 - 使用正確的 API 端點 GET /api/books/{id}
        book_response = session.get(f"{API_URL}/books/{book_id}")
        existing_page_id = None
        
        if book_response.status_code == 200:
            book_data = book_response.json()
            contents = book_data.get("contents", [])
            
            # 遞歸搜尋頁面（包含章節內的頁面）
            def find_page_in_contents(contents_list):
                for item in contents_list:
                    if item.get("type") == "page" and item.get("name") == name:
                        # 如果有指定章節，檢查頁面是否在該章節內
                        if chapter_id:
                            if item.get("chapter_id") == chapter_id:
                                return item["id"]
                        else:
                            # 沒有指定章節，檢查是否在書籍根目錄
                            if not item.get("chapter_id"):
                                return item["id"]
                    elif item.get("type") == "chapter" and chapter_id and item.get("id") == chapter_id:
                        # 搜尋章節內的頁面
                        chapter_pages = item.get("pages", [])
                        for page in chapter_pages:
                            if page.get("name") == name:
                                return page["id"]
                return None
            
            existing_page_id = find_page_in_contents(contents)
        
        # 如果頁面存在，檢查是否需要更新
        if existing_page_id:
            page_detail_response = session.get(f"{API_URL}/pages/{existing_page_id}")
            if page_detail_response.status_code == 200:
                existing_content = page_detail_response.json().get("markdown", "")
                current_hash = get_content_hash(markdown)
                existing_hash = get_content_hash(existing_content)
                
                if current_hash != existing_hash:
                    # 內容有變更，執行更新
                    update_payload = {"name": name, "markdown": markdown}
                    if chapter_id:
                        update_payload["chapter_id"] = chapter_id
                    
                    update_response = session.put(f"{API_URL}/pages/{existing_page_id}", json=update_payload)
                    if update_response.status_code == 200:
                        print(f"    📝 更新頁面: {name} (ID: {existing_page_id})")
                    else:
                        print(f"    ❌ 更新頁面失敗 {name}: {update_response.text}")
                else:
                    print(f"    📝 頁面無變更: {name} (ID: {existing_page_id})")
            else:
                print(f"    ❌ 無法取得頁面詳細內容: {name}")
        else:
            # 頁面不存在，建立新頁面
            payload = {
                "book_id": book_id,
                "name": name,
                "markdown": markdown
            }
            if chapter_id:
                payload["chapter_id"] = chapter_id

            r = session.post(f"{API_URL}/pages", json=payload)
            if r.status_code == 200:
                page_id = r.json()["id"]
                print(f"    📝 建立新頁面: {name} (ID: {page_id})")
            else:
                print(f"    ❌ 建立頁面失敗 {name}: {r.text}")
                
    except Exception as e:
        print(f"❌ 處理頁面時發生錯誤: {e}")


def import_test_directory():
    """測試導入指定目錄"""
    print(f"🚀 開始測試導入 {TEST_DIR} 目錄...")
    
    # 檢查 API 權限
    print("🔐 檢查 API 權限...")
    if not check_api_permissions():
        print("❌ API 權限檢查失敗，請先解決權限問題")
        return
    
    test_path = os.path.join(MD_DIR, TEST_DIR)
    if not os.path.exists(test_path):
        print(f"❌ 測試目錄不存在: {test_path}")
        return

    # 處理測試目錄 - 每個資料夾 = 一本書
    book_id = create_or_update_book(TEST_DIR)
    if not book_id:
        return

    has_subdir = any(os.path.isdir(os.path.join(test_path, entry)) 
                     for entry in os.listdir(test_path))

    for entry in os.listdir(test_path):
        entry_path = os.path.join(test_path, entry)

        # 子目錄 → 章節
        if os.path.isdir(entry_path):
            chapter_id = create_or_update_chapter(book_id, entry)
            if not chapter_id:
                continue

            for fname in os.listdir(entry_path):
                if fname.endswith(".md"):
                    try:
                        with open(os.path.join(entry_path, fname), "r", encoding="utf-8") as f:
                            content = f.read()
                        page_name = fname[:-3]
                        create_or_update_page(book_id, chapter_id, page_name, content)
                    except Exception as e:
                        print(f"    ❌ 讀取檔案錯誤 {fname}: {e}")

        # 直接是 markdown
        elif entry.endswith(".md"):
            try:
                with open(entry_path, "r", encoding="utf-8") as f:
                    content = f.read()

                page_name = entry[:-3]
                # 如果該書有子目錄，代表要用章節 → 此時這個檔案放「書籍根目錄」
                # 如果沒有子目錄，直接放在書籍底下（chapter_id=None）
                create_or_update_page(book_id, None if not has_subdir else None, page_name, content)
            except Exception as e:
                print(f"    ❌ 讀取檔案錯誤 {entry}: {e}")
    
    print(f"✅ {TEST_DIR} 目錄處理完成！")


if __name__ == "__main__":
    import_test_directory()