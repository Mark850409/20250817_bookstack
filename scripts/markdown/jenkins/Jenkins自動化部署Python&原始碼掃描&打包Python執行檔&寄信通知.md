---
title: Jenkins自動化部署Python&原始碼掃描&打包Python執行檔&寄信通知
updated: 2024-07-23 13:29:25Z
created: 2023-08-28 07:48:21Z
latitude: 25.0329694
longitude: 121.5654177
altitude: 0
tags:
  - Jenkins
  - python
  - email
---

# 1. 1 Jenkins自動化佈署Python&原始碼掃描&打包Python執行檔&寄信通知

還沒有安裝Jenkins? 請參照這篇[[Jenkins自動化部署-安裝教學]]

## 1.1. 簡介
學習如何利用Jenkins在本地部署python並寄信

## 1.2. 目錄

- [1. 1 Jenkins自動化佈署Python\&原始碼掃描\&打包Python執行檔\&寄信通知](#1-1-jenkins自動化佈署python原始碼掃描打包python執行檔寄信通知)
  - [1.1. 簡介](#11-簡介)
  - [1.2. 目錄](#12-目錄)
  - [1.3. 事前準備](#13-事前準備)
    - [1.3.1. 請先安裝以下套件](#131-請先安裝以下套件)
  - [1.4. 建立git倉庫](#14-建立git倉庫)
  - [1.5.  建立Jenkins作業流程](#15--建立jenkins作業流程)
    - [1.5.1. 設定git倉庫網址\&登入金鑰](#151-設定git倉庫網址登入金鑰)
    - [1.5.2. 建置觸發程序，設定為每分鐘](#152-建置觸發程序設定為每分鐘)
    - [1.5.3. 選擇SonarqubeScanner，並設定以下參數在properties](#153-選擇sonarqubescanner並設定以下參數在properties)
    - [1.5.4. 撰寫腳本並給予權限執行腳本](#154-撰寫腳本並給予權限執行腳本)
    - [1.5.5. 建置後動作選擇Allure Report，產生測試報告](#155-建置後動作選擇allure-report產生測試報告)
    - [1.5.6. 建置後動作選擇寄信，附件和建置紀錄可加可不加](#156-建置後動作選擇寄信附件和建置紀錄可加可不加)
    - [1.5.7. 執行結果如附圖](#157-執行結果如附圖)


## 1.3. 事前準備

### 1.3.1. 請先安裝以下套件


沒安裝以下套件會報錯，請先安裝

1. 安裝node.js
apt-get install -y nodejs

2. 安裝npm
apt-get install npm

3. 安裝pyinstaller
pip3 install pyinstaller

4. 安裝zip
 apt-get install zip 


<!--more-->
 
## 1.4. 建立git倉庫

![](https://markweb.idv.tw/uploads/upload_546404075566efa17aa2bfaedcc490ab.png)



## 1.5.  建立Jenkins作業流程

### 1.5.1. 設定git倉庫網址&登入金鑰

![](https://markweb.idv.tw/uploads/upload_3f7c0577bdaf9aa4c1996827bbe08dc1.png)

### 1.5.2. 建置觸發程序，設定為每分鐘
![](https://markweb.idv.tw/uploads/upload_971f10629d8d32a64ba72e672721024a.png)

### 1.5.3. 選擇SonarqubeScanner，並設定以下參數在properties

自行設名稱
* sonar.projectKey = python.Web
自行設名稱，此專案名稱會出現在server上
* sonar.projectName = python.Web
* sonar.projectVersion=1.1
注意下面是你要掃描的目錄
* sonar.sources=/var/jenkins_home/workspace/自動化佈署+原始碼版控+原始碼弱掃+單元測試+產出測試報告+寄送email
* sonar.sourceEncoding=UTF-8

![](https://markweb.idv.tw/uploads/upload_77c33e4d1c00743ca3998088b94f67c6.png)

### 1.5.4. 撰寫腳本並給予權限執行腳本

![](https://markweb.idv.tw/uploads/upload_21bf0be7b1c0ef6523cd5ce58d128cc0.png)

```bash

#!/bin/bash
#+-------------------------------------腳本說明--------------------------------------------+
# 自動化佈署+原始碼版控+原始碼弱掃+單元測試+產出測試報告+寄送email腳本
#
# (C) 2023 - markhsu - licensed under markweb License v1.
# 
#+----------------------------------------------------------------------------------------+
date=$(date +%Y-%m-%d)
echo "+----------------------------------------------------------------------------------------+"
echo "                                    開始打包python                                         "
echo "+----------------------------------------------------------------------------------------+"
pyinstaller -F main.py
echo "+----------------------------------------------------------------------------------------+"
echo "                                    開始進行單元測試並產生測試報告                            "
echo "+----------------------------------------------------------------------------------------+"
python3 -m pytest -s -q ${WORKSPACE}/test_calculator.py --alluredir=${WORKSPACE}/allure-results --clean-alluredir
echo "+----------------------------------------------------------------------------------------+"
echo "                                    開始打包測試報告                                      "
echo "+----------------------------------------------------------------------------------------+"
zip -r ${WORKSPACE}/${date}_allure-results.bak ${WORKSPACE}/allure-results/*

```

### 1.5.5. 建置後動作選擇Allure Report，產生測試報告

![](https://markweb.idv.tw/uploads/upload_af16fcc85f1d8cb824fd56e8d494a6e3.png)

### 1.5.6. 建置後動作選擇寄信，附件和建置紀錄可加可不加
![](https://markweb.idv.tw/uploads/upload_ec12afdf09415a9ff418239884159930.png)

### 1.5.7. 執行結果如附圖

![](https://markweb.idv.tw/uploads/upload_99295c82b9c293ccba11b8d32d597287.png)