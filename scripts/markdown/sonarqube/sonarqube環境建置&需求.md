---
title: sonarqube環境建置&需求
updated: 2024-07-23 13:32:24Z
created: 2023-08-04 08:26:30Z
tags:
  - SonarQube
---

<div class="note info">
       <p>java jdk=11，mysql≥5.6≤8.0</p>
 </div>


# 1. sonarqube環境建置&需求

## 1.1. 簡介
學習如何建置sonarqube環境

## 1.2. 目錄

- [1. sonarqube環境建置\&需求](#1-sonarqube環境建置需求)
  - [1.1. 簡介](#11-簡介)
  - [1.2. 目錄](#12-目錄)
  - [1.3. 操作步驟](#13-操作步驟)
    - [1.3.1. 至官網下載sonarqube7.7版本，並解壓](#131-至官網下載sonarqube77版本並解壓)
    - [1.3.2. 編輯sonarqube7.7/conf/sonar.properties，建置以下 行，存檔](#132-編輯sonarqube77confsonarproperties建置以下-行存檔)
    - [1.3.3. 到sonarqube-7.7\\extensions\\jdbc-driver\\oracle放入JDBC DRIVER](#133-到sonarqube-77extensionsjdbc-driveroracle放入jdbc-driver)
    - [1.3.4. 到sonarqube-7.7\\bin\\windows-x86-64找到StartSonar.bat，並點兩下執行](#134-到sonarqube-77binwindows-x86-64找到startsonarbat並點兩下執行)
    - [1.3.5. 如遇無法啟動可至sonarqube-7.7\\logs\\web.log查看](#135-如遇無法啟動可至sonarqube-77logsweblog查看)


## 1.3. 操作步驟
### 1.3.1. 至官網下載sonarqube7.7版本，並解壓

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/Qzpc86c20d7-upload-4bfc143561fc0993f4cf31316f742dcd.png)

<!--more-->

### 1.3.2. 編輯sonarqube7.7/conf/sonar.properties，建置以下 行，存檔


![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/fOK9af05b98-upload-518c2e750d86585fff5200df31974fb7.png)

```java
sonar.jdbc.username=sonar
sonar.jdbc.password=sonar
sonar.jdbc.url=jdbc:mysql://localhost:3307/sonar?useUnicode=true&characterEncoding=utf8&rewriteBatchedStatements=true&useConfigs=maxPerformance&useSSL=false
```

### 1.3.3. 到sonarqube-7.7\extensions\jdbc-driver\oracle放入JDBC DRIVER

![](https://markweb.idv.tw/uploads/upload_d2d586c5f05d540f8284d3c1d68e830f.png)


### 1.3.4. 到sonarqube-7.7\bin\windows-x86-64找到StartSonar.bat，並點兩下執行


![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/lYMb08fd74b-upload-d86bab4446900fa13a3db33a45cc3e2f.png)

### 1.3.5. 如遇無法啟動可至sonarqube-7.7\logs\web.log查看


![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/KY59db281f6-upload-8261624ff0e2d9ccd1aa4be8908bf119.png)