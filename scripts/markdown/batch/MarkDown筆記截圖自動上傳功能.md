---
title: MarkDown筆記截圖自動上傳功能
updated: 2024-07-23 13:27:48Z
created: 2023-09-06 13:32:07Z
latitude: 24.83872260
longitude: 121.01772460
altitude: 0.0000
---

# 1 MarkDown筆記截圖自動上傳功能

## 1.1 簡介
`自動化上傳筆記到`hexo，免去`人工建置`的困擾

## 1.2 目錄

- [1 MarkDown筆記截圖自動上傳功能](#1-markdown筆記截圖自動上傳功能)
  - [1.1 簡介](#11-簡介)
  - [1.2 目錄](#12-目錄)
  - [1.3 事前準備](#13-事前準備)
    - [1.3.1 請先在Joplin進行以下設定](#131-請先在joplin進行以下設定)
  - [1.4 開始準備撰寫腳本](#14-開始準備撰寫腳本)
  - [1.5 在Typora進行以下設定](#15-在typora進行以下設定)
  - [1.6 最後完成畫面](#16-最後完成畫面)


## 1.3 事前準備

### 1.3.1 請先在Joplin進行以下設定

![image-20230906213746159](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/IKo3d24bb8b-image-20230906213746159.png)

<!--more-->

## 1.4 開始準備撰寫腳本

```bash title:"AutoUpload.bat"
chcp 65001
REM 抓出系統時間
for /f "tokens=1-6 delims=-" %%a in ('PowerShell -Command "& {Get-Date -format "yyyy-MM-dd-HH-mm-ss"}"') do (
    SET year=%%a
    SET month=%%b
    SET day=%%c
)
REM 將本地目錄複製到專案目錄下存放
xcopy /S /Q /Y /F "C:\Users\MarkHSU\AppData\Roaming\Typora\typora-user-images\%~nx1" "E:\Project\jenkins\UploadMarkdownImage"
cd /d "E:\Project\jenkins\UploadMarkdownImage"
REM 開始上傳git
git init
git add --all
git commit -m "%year%-%month%-%day%_筆記圖檔倉庫"
git remote add origin https://markweb.idv.tw:8443/markhsu/JoplinImageUpload.git
git push -u origin master
REM 重點為以下這兩行
echo Upload Success:
echo https://markweb.idv.tw/uploads/%~nx1
```

![image-20230906214031341](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/Zxj6ecdfed5-image-20230906214031341.png)

## 1.5 在Typora進行以下設定

- 選擇上傳圖片
- 套用規則打勾
- 使用相對路徑打勾
- 插入圖片轉義URL打勾
- 圖片上傳命令使用自定義腳本

![image-20230906214414536](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/Ir9bbabea5c-image-20230906214414536.png)

## 1.6 最後完成畫面
![image-20230906214601539](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/K08888b8629-image-20230906214601539.png)