#!/usr/bin/env python3
import os
import requests

# 從環境變數讀取設定
API_URL = os.getenv("BOOKSTACK_API_URL", "http://bookstack:80/api")
TOKEN_ID = os.getenv("BOOKSTACK_TOKEN_ID", "")
TOKEN_SECRET = os.getenv("BOOKSTACK_TOKEN_SECRET", "")
MD_DIR = os.getenv("BOOKSTACK_MD_DIR", "/scripts/markdown")  # 放置 markdown 的根目錄

session = requests.Session()
session.headers.update({
    "Authorization": f"Token {TOKEN_ID}:{TOKEN_SECRET}",
    "Content-Type": "application/json"
})


def create_book(name):
    """建立書籍 (Book)"""
    r = session.post(f"{API_URL}/books", json={"name": name})
    if r.status_code == 200:
        print(f"📚 建立書籍: {name}")
        return r.json()["id"]
    else:
        # 已存在 → 找出 ID
        books = session.get(f"{API_URL}/books").json().get("data", [])
        for b in books:
            if b["name"] == name:
                print(f"📚 已存在書籍: {name}")
                return b["id"]
    return None


def create_chapter(book_id, name):
    """建立章節 (Chapter)"""
    r = session.post(f"{API_URL}/chapters", json={"book_id": book_id, "name": name})
    if r.status_code == 200:
        print(f"  📖 建立章節: {name}")
        return r.json()["id"]
    else:
        # 已存在 → 找出 ID
        chapters = session.get(f"{API_URL}/books/{book_id}/content").json().get("data", [])
        for c in chapters:
            if c["type"] == "chapter" and c["name"] == name:
                print(f"  📖 已存在章節: {name}")
                return c["id"]
    return None


def create_page(book_id, chapter_id, name, markdown):
    """建立頁面 (Page)"""
    payload = {
        "book_id": book_id,
        "name": name,
        "markdown": markdown
    }
    if chapter_id:
        payload["chapter_id"] = chapter_id

    r = session.post(f"{API_URL}/pages", json=payload)
    if r.status_code == 200:
        print(f"    📝 建立頁面: {name}")
    else:
        print(f"    ❌ 建立頁面失敗 {name}: {r.text}")


def import_markdown():
    """
    主要流程：
    - 每個最上層資料夾 = 一本書
    - 如果資料夾底下有子目錄 → 子目錄 = 章節，檔案 = 頁面
    - 如果資料夾底下直接是 markdown → 每個檔案直接變成「書籍下的頁面」
    """
    for book_name in os.listdir(MD_DIR):
        book_path = os.path.join(MD_DIR, book_name)
        if not os.path.isdir(book_path):
            continue

        # 每個資料夾 = 一本書
        book_id = create_book(book_name)

        has_subdir = any(os.path.isdir(os.path.join(book_path, e)) for e in os.listdir(book_path))

        for entry in os.listdir(book_path):
            entry_path = os.path.join(book_path, entry)

            # 子目錄 → 章節
            if os.path.isdir(entry_path):
                chapter_id = create_chapter(book_id, entry)

                for fname in os.listdir(entry_path):
                    if fname.endswith(".md"):
                        with open(os.path.join(entry_path, fname), "r", encoding="utf-8") as f:
                            content = f.read()
                        page_name = fname[:-3]
                        create_page(book_id, chapter_id, page_name, content)

            # 直接是 markdown
            elif entry.endswith(".md"):
                with open(entry_path, "r", encoding="utf-8") as f:
                    content = f.read()

                page_name = entry[:-3]
                # 🚫 如果該書有子目錄，代表要用章節 → 此時這個檔案放「書籍根目錄」
                # ✅ 如果沒有子目錄，直接放在書籍底下（chapter_id=None）
                create_page(book_id, None if not has_subdir else None, page_name, content)


if __name__ == "__main__":
    import_markdown()
