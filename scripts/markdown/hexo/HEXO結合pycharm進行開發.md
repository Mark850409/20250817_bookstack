---
title: HEXO結合pycharm進行開發
updated: 2024-07-23 13:29:09Z
created: 2023-08-04 08:26:29Z
tags:
  - hexo
---

# 1 HEXO結合pycharm進行開發

## 1.1 簡介
學習如何用pycharm開發HEXO

## 1.2 目錄

- [1 HEXO結合pycharm進行開發](#1-hexo結合pycharm進行開發)
  - [1.1 簡介](#11-簡介)
  - [1.2 目錄](#12-目錄)
  - [1.3 步驟開始](#13-步驟開始)
    - [1.3.1 建立 個空的新專案，並設定SFTP同步](#131-建立-個空的新專案並設定sftp同步)
    - [1.3.2 根據以下圖片內容進行設定](#132-根據以下圖片內容進行設定)
    - [1.3.3 點選Mappings頁籤進行以下設定](#133-點選mappings頁籤進行以下設定)
    - [1.3.4 點選tools→Deployment→Options](#134-點選toolsdeploymentoptions)
    - [1.3.5 Upload changed files auto...這邊選擇Always即可](#135-upload-changed-files-auto這邊選擇always即可)


## 1.3 步驟開始

### 1.3.1 建立 個空的新專案，並設定SFTP同步

![](https://markweb.idv.tw/uploads/upload_28c774de95e05d69b17aeebd005350eb.png)

* * *
<!--more-->

### 1.3.2 根據以下圖片內容進行設定

- Type：選擇SFTP
- Root path：設定網站根目錄路徑
- Web server URL：輸入https://markweb.idv.tw:23443

 連線前請先點選tset connection進行測試



![](https://markweb.idv.tw/uploads/upload_96626bb5ad5c46e2da1fcd1ef5056fc6.png)

* * *

### 1.3.3 點選Mappings頁籤進行以下設定


記得要將Deployment path：設定為＂/＂


![](https://markweb.idv.tw/uploads/upload_3a98b65c9bd0ffd0349188d47e23a775.png)

* * *

### 1.3.4 點選tools→Deployment→Options

![](https://markweb.idv.tw/uploads/upload_2a14592ef92fc55948400c65ccfcd2d0.png)

* * *

### 1.3.5 Upload changed files auto...這邊選擇Always即可

![](https://markweb.idv.tw/uploads/upload_e5cbd837efc3a14ef8faf927d13b1724.png)