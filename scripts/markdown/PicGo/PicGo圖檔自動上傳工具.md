---
title: PicGo圖檔自動上傳工具
updated: 2024-07-25 02:31:00Z
created: 2024-04-07 12:29:03Z
latitude: 25.0329694
longitude: 121.5654177
altitude: 0
tags:
  - PicGO
  - upload
---

# 1. PicGo圖檔自動上傳工具

## 1.1. 簡介

`自動化`上傳圖檔


## 1.2. 目錄

- [1. PicGo圖檔自動上傳工具](#1-picgo圖檔自動上傳工具)
  - [1.1. 簡介](#11-簡介)
  - [1.2. 目錄](#12-目錄)
    - [1.2.1. 使用方式](#121-使用方式)
    - [1.2.2. 參考連結](#122-參考連結)


### 1.2.1. 使用方式

https://github.com/Molunerfinn/picgo/releases

<!--more-->

請撰寫`sftpUploader.json`

```json
{
  "ubuntu2304": {
    "url": "https://markweb.idv.tw",
    "path": "/uploads/{fullName}",
    "uploadPath": "/media/markhsu/Data/DockerProtainer/hackmd/uploads/{fullName}",
    "host": "markweb.idv.tw",
    "username": "root",
    "password": "mark850409"
  }
}
```

進入插件設定 > 安裝sftp-uploader
![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/MJBc951085f-202404071957931.png)

設定以下必填項目
![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/9FYba25a538-202404071958911.png)


> [!note] 小提示
>這裡的網站標是要和設定檔的標題一致，否則會發生錯誤!!!


配置該json文件
![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/7IQ4468ea9d-202404071958898.png)



> [!note] 小提示
>1. uploadPath是上傳路徑
>2. path這個是針對網址的路徑


### 1.2.2. 參考連結

1. 寫 Markdown 的好夥伴！PicGo 支援快速上傳圖片到預設圖床，並且返回 Markdown 圖片超連結

https://medium.com/pm%E7%9A%84%E7%94%9F%E7%94%A2%E5%8A%9B%E5%B7%A5%E5%85%B7%E7%AE%B1/%E5%AF%AB-markdown-%E7%9A%84%E5%A5%BD%E5%A4%A5%E4%BC%B4-picgo-%E6%94%AF%E6%8F%B4%E5%BF%AB%E9%80%9F%E4%B8%8A%E5%82%B3%E5%9C%96%E7%89%87%E5%88%B0%E9%A0%90%E8%A8%AD%E5%9C%96%E5%BA%8A-%E4%B8%A6%E4%B8%94%E8%BF%94%E5%9B%9E-markdown-%E5%9C%96%E7%89%87%E6%A0%BC%E5%BC%8F-7b83ad56ddb7