---
title: Jenkins自動化部署-與Gitea綁定，透過webhook觸發流程
updated: 2024-07-23 13:29:21Z
created: 2023-08-14 11:39:44Z
latitude: 24.8287095
longitude: 121.0169462
altitude: 0
tags:
  - Jenkins
  - Gitea
  - Webhook
---

# 1 Jenkins自動化佈署-與Gitea綁定，透過webhook觸發流程

還沒有安裝Jenkins? 請參照這篇[[Jenkins自動化部署-安裝教學]]

## 1.1 簡介
學習如何利用Jenkins綁定Gitea，透過webhook觸發流程

## 1.2 目錄

- [1 Jenkins自動化佈署-與Gitea綁定，透過webhook觸發流程](#1-jenkins自動化佈署-與gitea綁定透過webhook觸發流程)
  - [1.1 簡介](#11-簡介)
  - [1.2 目錄](#12-目錄)
  - [1.3 事前準備](#13-事前準備)
    - [1.3.1 請到gitea server建立 個新的倉庫](#131-請到gitea-server建立-個新的倉庫)
    - [1.3.2 點選設定→Webhook確認是否有和Jenkins綁定成功](#132-點選設定webhook確認是否有和jenkins綁定成功)
  - [1.4 設定教學](#14-設定教學)
    - [1.4.1 登入Jenkins，點選新增作業](#141-登入jenkins點選新增作業)
    - [1.4.2 在原始碼管理，點選Git，輸入URL並選取憑證](#142-在原始碼管理點選git輸入url並選取憑證)
    - [1.4.3 建置觸發程序，請將GitHub hook trigger for GITScm polling\&輪詢 SCM打勾，排程設定為每分鐘執行 次](#143-建置觸發程序請將github-hook-trigger-for-gitscm-polling輪詢-scm打勾排程設定為每分鐘執行-次)
    - [1.4.4 建置環境，勾選在「畫面輸出」中加入時間戳記，最後點選儲存即可](#144-建置環境勾選在畫面輸出中加入時間戳記最後點選儲存即可)
  - [1.5 實際測試(使用SourceTree)](#15-實際測試使用sourcetree)
    - [1.5.1 點選clone，請輸入URL，最後點選克隆](#151-點選clone請輸入url最後點選克隆)
    - [1.5.2 看到此畫面表示已成功同步](#152-看到此畫面表示已成功同步)
    - [1.5.3 準備檔案進行提交...](#153-準備檔案進行提交)
    - [1.5.4 將檔案加入stage](#154-將檔案加入stage)
    - [1.5.5 準備commit](#155-準備commit)
    - [1.5.6 準備push](#156-準備push)
    - [1.5.7 流程已佈署成功](#157-流程已佈署成功)
    - [1.5.8 檢查Gitea是否已顯示剛才推送上去的專案](#158-檢查gitea是否已顯示剛才推送上去的專案)
    - [1.5.9 參考連結](#159-參考連結)


## 1.3 事前準備

### 1.3.1 請到gitea server建立 個新的倉庫
![](https://markweb.idv.tw/uploads/upload_b31e77bdb2a2bfe541884812d00af1f7.png)

### 1.3.2 點選設定→Webhook確認是否有和Jenkins綁定成功
![](https://markweb.idv.tw/uploads/upload_5bb6653a5f7ef2dcb6f52aecdf5bbedd.png)

<!--more-->

## 1.4 設定教學

### 1.4.1 登入Jenkins，點選新增作業

![](https://markweb.idv.tw/uploads/upload_8ae9fb12cf730d58d6792b55cac5678a.png)

### 1.4.2 在原始碼管理，點選Git，輸入URL並選取憑證

![](https://markweb.idv.tw/uploads/upload_48674dafc93e503d4242912391f52a87.png)

### 1.4.3 建置觸發程序，請將GitHub hook trigger for GITScm polling&輪詢 SCM打勾，排程設定為每分鐘執行 次

```bash
*/1 * * * * 
```

![](https://markweb.idv.tw/uploads/upload_47502e5cdce66cf643599abd435d2bbd.png)


### 1.4.4 建置環境，勾選在「畫面輸出」中加入時間戳記，最後點選儲存即可
![](https://markweb.idv.tw/uploads/upload_1a2b12b5c513a18b3ad7b9c30d817bd8.png)


## 1.5 實際測試(使用SourceTree)

### 1.5.1 點選clone，請輸入URL，最後點選克隆
![](https://markweb.idv.tw/uploads/upload_495cf36ff949999bbb5de4a22c529ed1.png)


![](https://markweb.idv.tw/uploads/upload_0a11ab1ddd49c3bbfad12187ff63bd62.png)


### 1.5.2 看到此畫面表示已成功同步
![](https://markweb.idv.tw/uploads/upload_309dc359f930b437d29193068862dc3b.png)


### 1.5.3 準備檔案進行提交...

![](https://markweb.idv.tw/uploads/upload_55a2c99d89312c31b01540b9c6134a8c.png)


### 1.5.4 將檔案加入stage

![](https://markweb.idv.tw/uploads/upload_845816c1ffc2ae3899ba95afffbd8dc0.png)


### 1.5.5 準備commit

![](https://markweb.idv.tw/uploads/upload_917a8a939d137f47b3a61f5428264b3c.png)


### 1.5.6 準備push

![](https://markweb.idv.tw/uploads/upload_ecdf2f6e2c558b9c4987e7e8fa4d1397.png)


### 1.5.7 流程已佈署成功
![](https://markweb.idv.tw/uploads/upload_544368f63418c0aafde855c5559aeb43.png)


### 1.5.8 檢查Gitea是否已顯示剛才推送上去的專案

![](https://markweb.idv.tw/uploads/upload_855815601af0ac0645b4d889ec579601.png)

### 1.5.9 參考連結

https://www.cnblogs.com/Gitea/p/jenkins.html