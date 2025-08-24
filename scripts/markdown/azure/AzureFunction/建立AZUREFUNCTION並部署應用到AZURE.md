---
title: 建立AZURE FUNCTION並部署應用到AZURE
created: 2023-12-17 13:10:29Z
updated: 2024-10-24 13:10:29Z
tags:
  - Azure
  - AzureFunction
---
# 1. 20231217_AzureFunctionHomeWork

## 1.1. 簡介

建立AZURE FUNCTION並部署應用到AZURE

## 1.2. 目錄

- [1. 20231217\_AzureFunctionHomeWork](#1-20231217_azurefunctionhomework)
  - [1.1. 簡介](#11-簡介)
  - [1.2. 目錄](#12-目錄)
    - [1.2.1. 事前準備](#121-事前準備)
    - [1.2.2. 使用教學](#122-使用教學)
      - [1.2.2.1. 建立AZURE FUNCTION](#1221-建立azure-function)
      - [1.2.2.2. 程式碼撰寫](#1222-程式碼撰寫)
      - [1.2.2.3. 本地測試方式](#1223-本地測試方式)
        - [1.2.2.3.1. 方法一：Postman](#12231-方法一postman)
        - [1.2.2.3.2. 方法二：browser](#12232-方法二browser)
      - [1.2.2.4. 建立部署專案](#1224-建立部署專案)
      - [1.2.2.5. 程式碼改寫](#1225-程式碼改寫)
      - [1.2.2.6. 部署前的本地測試](#1226-部署前的本地測試)
      - [1.2.2.7. 部署後的線上測試](#1227-部署後的線上測試)


### 1.2.1. 事前準備

開啟VSCODE，安裝AZURE TOOLS
![image-20231217105800222](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/dDR6113e429-image-20231217105800222.png)



![image-20231217105834715](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/a8fdbc8f-image-20231217105834715.png)


以系統管理員身分執行PowerShell，並輸入以下指令
```powershell
set-excutionpolicy remotesigned
```
![image-20231217105954406](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/90c44481-image-20231217105954406.png)



![image-20231217110204339](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/51K103f78a4-image-20231217110204339.png)


如果要部屬到AZURE FUNCTION進行本機測試，請事先安裝azure function tools
https://github.com/Azure/azure-functions-core-tools?tab=readme-ov-file#installing


<!--more-->

### 1.2.2. 使用教學

#### 1.2.2.1. 建立AZURE FUNCTION
STEP 1：點選functions→Create Function App in Azure
![image-20231217105157765](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/Odr8b3ec0bf-image-20231217105157765.png)

STEP 2：輸入function名稱
![image-20231217105256231](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/4900b4d6-image-20231217105256231.png)


STEP 3：選擇python3.11版本，請注意要和本地虛擬環境版本一致
![image-20231217105403290](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/NRYcf9cd5b7-image-20231217105403290.png)

STEP 4：選擇East US
![image-20231217105527832](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/954823a4-image-20231217105527832.png)

STEP 5：等待建立完成
![image-20231217105601422](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/11a98607-image-20231217105601422.png)


STEP 6：建立成功
![image-20231217105657675](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/c22b3ed3-image-20231217105657675.png)



#### 1.2.2.2. 程式碼撰寫
STEP 1：將key&location進行替換，params也要修改成對應值
![image-20231217115352866](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/400b0ade-image-20231217115352866.png)

STEP 2：將body的text也進行替換
![image-20231217120311009](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/cee74a89-image-20231217120311009.png)

STEP 3：點選F5進行測試，發現錯誤，因為沒有安裝flask套件，請在虛擬環境安裝flask
![image-20231217110538776](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/PqW135f5a64-image-20231217110538776.png)

STEP 4：安裝後可正常執行畫面
![image-20231217122125572](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/image-20231217122125572.png)

#### 1.2.2.3. 本地測試方式
##### 1.2.2.3.1. 方法一：Postman
STEP 1：使用postman進行API測試，帶入相對應的參數值，點選send，如下圖
![image-20231217122417083](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/7d5f1c5e-image-20231217122417083.png)
##### 1.2.2.3.2. 方法二：browser
STEP 1：使用browser進行API測試，帶入相對應的參數值並按下Enter，如下圖
![image-20231217122534787](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/46822cec-image-20231217122534787.png)



#### 1.2.2.4. 建立部署專案
STEP 1：點選Create New Project
![image-20231217122836915](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/3fe98b6f-image-20231217122836915.png)
STEP 2：選擇本地專案
![image-20231217122901647](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/2362e13b-image-20231217122901647.png)
STEP 3：選擇Python
![image-20231217122923365](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/xlW454b554c-image-20231217122923365.png)
STEP 4：選擇Model V1
![image-20231217122948478](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/F200a02c392-image-20231217122948478.png)
STEP 5：選擇HTTP trigger
![image-20231217123010947](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/e7f81666-image-20231217123010947.png)
STEP 6：輸入名稱
![image-20231217123046767](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/QyEcab710d9-image-20231217123046767.png)
STEP 7：選擇Anonymous
![image-20231217123114042](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/a41e3ac9-image-20231217123114042.png)

#### 1.2.2.5. 程式碼改寫

STEP 1：開啟__init__.py，除了retun code，其他全部移除
![image-20231217123401931](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/Koq0ccce954-image-20231217123401931.png)

STEP 2：請更改接收參數的方式以及回傳方式
![image-20231217124942611](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/81dec7fb-image-20231217124942611.png)

#### 1.2.2.6. 部署前的本地測試

STEP 1：點選F5，使用提示的測試網址進行API測試
![image-20231217125140732](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/9cc9213f-image-20231217125140732.png)

STEP 2：未輸入任何參數的測試
![image-20231217125222875](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/3b032dbb-image-20231217125222875.png)

STEP 3：已輸入正確參數的測試
![image-20231217125308278](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/8ycba83cb45-image-20231217125308278.png)

#### 1.2.2.7. 部署後的線上測試
STEP 1：點選Deploy to Function App
![image-20231217125348224](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/18e1176b-image-20231217125348224.png)

STEP 2：出現對話框，點選Deploy
![image-20231217125414064](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/GHpee95dc6c-image-20231217125414064.png)
STEP 3：出現此訊息表示部署成功
![image-20231217125535920](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/7ZK1ecfaa05-image-20231217125535920.png)
STEP 4：到Azure Portol進入剛剛建立好的function，複製API網址
![image-20231217125624557](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/7k621305b04-image-20231217125624557.png)
STEP 5：未輸入任何參數的測試
![image-20231217125708168](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/ghv0e03b544-image-20231217125708168.png)
STEP 6：已輸入正確參數的測試
![image-20231217125735038](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/image-20231217125735038.png)
