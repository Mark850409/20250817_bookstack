---
title: Jenkins自動上傳備份檔到AzureBlob
updated: 2024-07-23 13:29:56Z
created: 2024-03-10 06:49:33Z
latitude: 25.0329694
longitude: 121.5654177
altitude: 0
tags:
  - Jenkins
  - Azure
  - Blob
  - Backup
---

# 1. Jenkins自動上傳備份檔到AzureBlob

還沒有安裝Jenkins? 請參照這篇[[Jenkins自動化部署-安裝教學]]
## 1.1. 簡介

自動上傳備份檔到AzureBlob

## 1.2. 專案架構

```
AzureBlobUploadWithJenkins
├─ Jenkinsfile
├─ README.md
└─ test.txt

```

## 1.3. 目錄

- [1. Jenkins自動上傳備份檔到AzureBlob](#1-jenkins自動上傳備份檔到azureblob)
  - [1.1. 簡介](#11-簡介)
  - [1.2. 專案架構](#12-專案架構)
  - [1.3. 目錄](#13-目錄)
  - [1.4. 操作步驟](#14-操作步驟)
    - [1.4.1. AZURE 操作步驟](#141-azure-操作步驟)
    - [1.4.2. 撰寫腳本前置步驟(先在本地測試)](#142-撰寫腳本前置步驟先在本地測試)


## 1.4. 操作步驟

### 1.4.1. AZURE 操作步驟

進入AZURE > 建立儲存體帳戶 > 基本 > 選擇訂用帳戶和資源群組

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/c562d1f4-upload-43ac0618df1c79b5c174ed7a5132cef7.png)

輸入儲存體帳戶名稱

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/6feb2499-upload-060c7dde3177fea9839a855fb3fd56a4.png)

切換到網路 > 選擇公開存取

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/kjM6faf60c0-upload-f055f6e0b5421a80700e2600f59e750d.png)

切換到檢閱 > 選擇建立

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/Fpy08c9a881-upload-62a2506375d540a5f2ec45761d793bfb.png)

<!--more-->
### 1.4.2. 撰寫腳本前置步驟(先在本地測試)

輸入az login > 按照以下說明將網址貼到瀏覽器 > 並貼上驗證碼

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/LT89054c91a-upload-cfd3abc26ee1a3eb01bd370f85293260.png)

輸入驗證碼 > 點選下 步

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/d2S441cc04e-upload-3e6aa873dd8283361547b30acd55014f.png)

選擇自己的微軟帳戶

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/47o28f38c21-upload-1adfaca400c30ba9fe204d6c934c7dfd.png)

點選繼續

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/9Ph20041a23-upload-79e42d6bdff27074d9a44fb104b73363.png)

輸入以下指令，登入azure帳戶，並請記住紅框標示處，等等會使用到

```bash
az login
```

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/d8bb0996-upload-77a38d6645f3697499465c2dca545711.png)

輸入以下指令，進行應用程式註冊，並請記住紅框標示處，等等會使用到

```bash
az ad sp create-for-rbac --name <service-principal-name> --role Owner --scopes /subscriptions/<subscription-id>
```


> [!note] 小提示 
> 1.使用UI建立的方式也可以，但因為在撰寫Jenkins Pipeline會遇到權限問題，導致登入失敗，建議使用指令建立
>2.這邊的關鍵是...要將角色設定為擁有者，並指定到訂閱帳戶下

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/fb1ce43b-upload-158cb8b60e5f2412b8e226260cb1b385.png)