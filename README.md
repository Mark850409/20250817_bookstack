# BookStack 知識庫管理系統

## 📖 專案簡介

本專案基於 BookStack 建置的知識庫管理系統，整合了 Markdown 自動導入功能。BookStack 是一個開源的自託管知識管理平台，支援書籍、章節、頁面的層級結構管理，並提供豐富的編輯功能和權限管理。

## ✨ 主要功能

- 📚 支援書籍、章節、頁面的層級結構管理
- 📝 整合 Markdown 編輯器與所見即所得編輯器
- 🔄 自動化 Markdown 檔案匯入功能
- 🗃️ 完整的權限管理系統
- 🔍 全文搜尋功能
- 📱 響應式設計，支援行動裝置
- 🐳 Docker 容器化部署

## 🛠️ 技術架構

- **應用程式**: BookStack (基於 PHP Laravel 框架)
- **資料庫**: MariaDB 10.6
- **容器化**: Docker & Docker Compose
- **反向代理**: Nginx
- **自動化工具**: Python 3 匯入腳本

## 📋 安裝需求

### 系統需求
- Docker >= 20.x
- Docker Compose >= 3.7
- 至少 2GB 可用記憶體
- 至少 5GB 可用磁碟空間

### 連接埠需求
- **6875**: BookStack Web 介面
- **3306**: MariaDB 資料庫（內部使用）

## 🚀 快速開始

### 1. 克隆專案
```bash
git clone <repository-url>
cd bookstack
```

### 2. 環境配置

檢查 `docker-compose.yml` 中的環境變數設定：

```yaml
# BookStack 設定
APP_URL: http://localhost:6875
DB_HOST: bookstack_db
DB_USER: bookstack
DB_PASS: bookstack123
DB_DATABASE: bookstackapp

# MariaDB 設定  
MYSQL_ROOT_PASSWORD: rootpass
MYSQL_USER: bookstack
MYSQL_PASSWORD: bookstack123
```

### 3. 啟動服務
```bash
# 建置並啟動容器
docker-compose up -d

# 查看容器狀態
docker-compose ps

# 查看日誌
docker-compose logs -f
```

### 4. 初始設定

1. 開啟瀏覽器，前往 `http://localhost:6875`
2. 使用預設管理員帳號登入：
   - **Email**: `admin@admin.com`
   - **密碼**: `password`
3. 首次登入後請立即更改管理員密碼

## 📁 目錄結構

```
bookstack/
├── Dockerfile              # BookStack 容器定義
├── docker-compose.yml      # Docker Compose 配置
├── bookstack_data/         # BookStack 應用程式資料
├── bookstack_db/           # MariaDB 資料庫檔案
├── uploads/                # 上傳檔案儲存目錄
├── scripts/                # 自動化腳本
│   ├── import_md_all.py    # Markdown 匯入腳本
│   └── markdown/           # 待匯入的 Markdown 檔案
└── README.md              # 本文件
```

## 🔄 Markdown 自動匯入功能

### 使用方式

1. **準備 Markdown 檔案**
   - 將 Markdown 檔案放置於 `scripts/markdown/` 目錄下
   - 支援層級結構：資料夾 → 書籍，子資料夾 → 章節，檔案 → 頁面

2. **設定環境變數**
```bash
export BOOKSTACK_API_URL="http://localhost:6875/api"
export BOOKSTACK_TOKEN_ID="your_token_id"
export BOOKSTACK_TOKEN_SECRET="your_token_secret"
export BOOKSTACK_MD_DIR="./scripts/markdown"
```

3. **執行匯入**
```bash
# 進入容器執行
docker-compose exec bookstack python3 /scripts/import_md_all.py

# 或在本機執行（需安裝 Python 3 和 requests）
python3 scripts/import_md_all.py
```

### 匯入規則

- 每個**頂層資料夾**對應一本**書籍**
- 資料夾內的**子目錄**對應**章節**
- `.md` 檔案對應**頁面**
- 如果資料夾直接包含 `.md` 檔案（無子目錄），則直接建立為書籍下的頁面

### 範例結構
```
scripts/markdown/
├── AI/                     → 書籍: AI
│   ├── LangChain/         → 章節: LangChain
│   │   └── tutorial.md    → 頁面: tutorial
│   └── RAG/               → 章節: RAG
│       └── implementation.md → 頁面: implementation
└── Docker/                 → 書籍: Docker
    └── guide.md           → 頁面: guide（直接在書籍下）
```

## 🔧 常用操作

### 容器管理
```bash
# 停止服務
docker-compose down

# 重新啟動
docker-compose restart

# 重新建置
docker-compose up -d --build

# 查看容器狀態
docker-compose ps

# 進入 BookStack 容器
docker-compose exec bookstack bash
```

### 資料備份
```bash
# 備份資料庫
docker-compose exec bookstack_db mysqldump -u bookstack -pbookstack123 bookstackapp > backup.sql

# 備份上傳檔案
tar -czf uploads_backup.tar.gz uploads/

# 備份應用程式資料
tar -czf bookstack_data_backup.tar.gz bookstack_data/
```

### 資料還原
```bash
# 還原資料庫
docker-compose exec -T bookstack_db mysql -u bookstack -pbookstack123 bookstackapp < backup.sql

# 還原檔案（停止容器後操作）
tar -xzf uploads_backup.tar.gz
tar -xzf bookstack_data_backup.tar.gz
```

## ⚠️ 注意事項

### 安全性設定

1. **變更預設密碼**
   - 首次登入後立即更改 `admin@admin.com` 的密碼
   - 定期更新密碼並使用強密碼

2. **環境變數保護**
   - 生產環境請變更 `docker-compose.yml` 中的資料庫密碼
   - 建議使用 `.env` 檔案管理敏感資訊

3. **API Token 管理**
   - 在 BookStack 管理介面中產生專用的 API Token
   - 避免在腳本中硬編碼 Token 資訊

### 效能最佳化

1. **資源配置**
   - 生產環境建議至少分配 4GB 記憶體
   - 定期清理不必要的檔案上傳

2. **資料庫維護**
   - 定期執行資料庫最佳化
   - 設定自動備份機制

### 故障排除

1. **容器無法啟動**
   ```bash
   # 檢查連接埠是否被占用
   netstat -tlnp | grep :6875
   
   # 查看詳細錯誤日誌
   docker-compose logs bookstack
   ```

2. **資料庫連線問題**
   ```bash
   # 檢查資料庫狀態
   docker-compose exec bookstack_db mysql -u bookstack -pbookstack123 -e "SELECT 1"
   ```

3. **匯入腳本問題**
   - 確認 API URL 和 Token 設定正確
   - 檢查 Markdown 檔案編碼為 UTF-8
   - 驗證檔案路徑權限設定

## 🔗 相關連結

- [BookStack 官方文件](https://www.bookstackapp.com/docs/)
- [BookStack GitHub](https://github.com/BookStackApp/BookStack)
- [Docker Hub - BookStack](https://hub.docker.com/r/linuxserver/bookstack)

## 🤝 貢獻指南

1. Fork 本專案
2. 建立功能分支 (`git checkout -b feature/new-feature`)
3. 提交變更 (`git commit -am 'Add some feature'`)
4. 推送到分支 (`git push origin feature/new-feature`)
5. 建立 Pull Request

## 📄 授權條款

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案

---

如有任何問題或建議，請建立 Issue 或聯繫專案維護者。