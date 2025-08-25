---
title: Jenkins自動化部署-自動建置並部署docker到遠端主機
updated: 2024-07-23 13:29:36Z
created: 2023-08-28 03:12:03Z
latitude: 25.0329694
longitude: 121.5654177
altitude: 0
tags:
  - Jenkins
  - Docker
  - remote
---

# 1 Jenkins自動化佈署-自動建置並佈署docker到遠端主機

還沒有安裝Jenkins? 請參照這篇[[Jenkins自動化部署-安裝教學]]

## 1.1 簡介
學習如何利用Jenkins遠端部署docker

## 1.2 目錄

- [1 Jenkins自動化佈署-自動建置並佈署docker到遠端主機](#1-jenkins自動化佈署-自動建置並佈署docker到遠端主機)
  - [1.1 簡介](#11-簡介)
  - [1.2 目錄](#12-目錄)
  - [1.3 建立git專案](#13-建立git專案)
  - [1.4 建立Jenkins作業流程](#14-建立jenkins作業流程)
    - [1.4.1 建立git倉庫後，將ssh的URL貼到Repository URL上面，並選擇 開始建立好的金鑰](#141-建立git倉庫後將ssh的url貼到repository-url上面並選擇-開始建立好的金鑰)
    - [1.4.2 設定專案觸發＆排程](#142-設定專案觸發排程)
    - [1.4.3 將腳本複製到遠端主機上面](#143-將腳本複製到遠端主機上面)
    - [1.4.4 建置後動作選擇寄信，附檔和建置紀錄可加可不加，最後按下儲存即可](#144-建置後動作選擇寄信附檔和建置紀錄可加可不加最後按下儲存即可)
    - [1.4.5 執行結果如附圖參考](#145-執行結果如附圖參考)


## 1.3 建立git專案

![](https://markweb.idv.tw/uploads/upload_1a7315a2034d8ba74541f8e211948c10.png)

<!--more-->

## 1.4 建立Jenkins作業流程

### 1.4.1 建立git倉庫後，將ssh的URL貼到Repository URL上面，並選擇 開始建立好的金鑰
![](https://markweb.idv.tw/uploads/upload_69cb821d2c22d51f7926d4ab486e1bba.png)

### 1.4.2 設定專案觸發＆排程
![](https://markweb.idv.tw/uploads/upload_3089f9291c84b8d01a86c60997f2ddf5.png)

### 1.4.3 將腳本複製到遠端主機上面
![](https://markweb.idv.tw/uploads/upload_85d9b03537f252f1c7bacd38e2e3a012.png)

### 1.4.4 建置後動作選擇寄信，附檔和建置紀錄可加可不加，最後按下儲存即可
![](https://markweb.idv.tw/uploads/upload_12f845f082263ed9b443786869523137.png)

### 1.4.5 執行結果如附圖參考
![](https://markweb.idv.tw/uploads/upload_bf004b4709cba6198f087312bc863261.png)