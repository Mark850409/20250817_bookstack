# BookStack 圖片遷移腳本使用說明

## 功能說明

此腳本可以：
1. 掃描所有 markdown 文件，找出外部圖片連結
2. 下載外部圖片並上傳到 BookStack 圖片庫
3. 將 markdown 文件中的圖片連結替換為 BookStack 格式

## 使用前準備

### 1. 獲取 BookStack API Token

1. 登入您的 BookStack： `https://mybookstack.zeabur.app`
2. 進入 **設定** → **API Tokens**
3. 點擊 **建立新的 Token**
4. 輸入 Token 名稱（例如：Image Migration）
5. 設定適當的權限（至少需要圖片上傳權限）
6. 複製生成的 Token（只會顯示一次）

### 2. 安裝必要套件

```bash
pip install requests pathlib
```

## 使用方法

### 執行腳本

```bash
cd E:\Project\NOTE\bookstack\scripts
python migrate_images.py
```

### 輸入 API Token

當腳本提示時，輸入您從 BookStack 獲取的 API Token：

```
請輸入 BookStack API Token: [貼上您的 Token]
```

## 腳本執行流程

1. **掃描階段**：掃描所有 markdown 文件，找出外部圖片
   - 支援的來源：`markweb.idv.tw` 和 `raw.githubusercontent.com`

2. **上傳階段**：逐個下載並上傳圖片到 BookStack
   - 圖片會上傳到 BookStack 圖片庫
   - 自動生成 `https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/檔名` 格式的 URL

3. **替換階段**：更新所有 markdown 文件中的圖片連結
   - 將外部連結替換為 BookStack 連結
   - 統計替換的連結數量

## 輸出格式

腳本會生成如下格式的 URL：
```
https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/檔名.png
```

其中：
- `2025-08` 是當前年月
- 檔名會包含原始檔名和 hash 前綴以避免重複

## 執行結果

腳本完成後會顯示：
- **上傳圖片**：成功上傳的圖片數量
- **更新文件**：修改的 markdown 文件數量  
- **替換連結**：總共替換的圖片連結數量

## 注意事項

⚠️ **重要提醒**：
- 執行前建議先備份 markdown 文件
- 確保網路連線穩定
- API Token 請妥善保管，不要分享給他人
- 如果上傳失敗，腳本會顯示錯誤訊息

## 疑難排解

### 常見錯誤

1. **API Token 無效**
   - 檢查 Token 是否正確
   - 確認 Token 權限設定

2. **網路連線問題**
   - 檢查網路連線
   - 確認 BookStack 服務器可訪問

3. **圖片下載失敗**
   - 部分外部圖片可能已失效
   - 檢查原始圖片是否還存在

### 手動檢查

執行完成後，您可以：
1. 檢查 BookStack 圖片庫是否有新上傳的圖片
2. 隨機檢查幾個 markdown 文件的圖片連結是否正確替換
3. 確認圖片在 BookStack 中能正常顯示

## 技術細節

- **支援格式**：PNG, JPG, JPEG, GIF, WebP, SVG, BMP
- **檔名處理**：使用 MD5 hash 前綴避免檔名衝突
- **速度控制**：每次上傳間隔 1 秒，避免伺服器壓力
- **錯誤處理**：完整的異常處理和錯誤回報