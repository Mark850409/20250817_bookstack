---
title: sonar-scanner環境建置
updated: 2024-07-23 13:32:27Z
created: 2023-08-04 08:26:30Z
tags:
  - SonarQube
---

# 1. sonar-scanner環境建置

## 1.1. 簡介
學習如何透過sonar-scanner進行原始碼弱點掃描

## 1.2. 目錄

- [1. sonar-scanner環境建置](#1-sonar-scanner環境建置)
  - [1.1. 簡介](#11-簡介)
  - [1.2. 目錄](#12-目錄)
  - [1.3. 操作步驟](#13-操作步驟)
    - [1.3.1. C:\\Users\\MarkHSU\\Desktop\\sonar-scanner-4.6.2.2472-windows\\conf\\sonar-scanner.properties](#131-cusersmarkhsudesktopsonar-scanner-4622472-windowsconfsonar-scannerproperties)
    - [1.3.2. 建置sonar-project.properties，並複製到要掃描的專案下](#132-建置sonar-projectproperties並複製到要掃描的專案下)
    - [1.3.3. 打開命令提示字元，輸入以下指令](#133-打開命令提示字元輸入以下指令)
    - [1.3.4. 打開http://localhost:9000](#134-打開httplocalhost9000)


```mysql
CREATE DATABASE sonar CHARACTER SET utf8 COLLATE utf8_general_ci; 
CREATE USER 'sonar' IDENTIFIED BY 'sonar'; 
GRANT ALL ON sonar.* TO 'sonar'@'%' IDENTIFIED BY 'password';
FLUSH PRIVILEGES;
```

```powershell
C:\Users\MarkHSU\Desktop\sonarqube\sonar-scanner-4.6.2.2472-windows\bin
```

## 1.3. 操作步驟
### 1.3.1. C:\Users\MarkHSU\Desktop\sonar-scanner-4.6.2.2472-windows\conf\sonar-scanner.properties

```java
#Configure here general information about the environment, such as SonarQube server connection details for example
#No information about specific project should appear here

#----- Default SonarQube server
sonar.host.url=http://localhost:9000

#----- Default source code encoding
sonar.sourceEncoding=UTF-8

sonar.jdbc.username=sonar
sonar.jdbc.password=sonar
sonar.jdbc.url=jdbc:mysql://localhost:3307/sonar?useUnicode=true&characterEncoding=utf8&rewriteBatchedStatements=true&useConfigs=maxPerformance&useSSL=false
```

<!--more-->

### 1.3.2. 建置sonar-project.properties，並複製到要掃描的專案下

sonar.projectName:專案名稱

sonar.sources:專案路徑

```java
# must be unique in a given SonarQube instance
sonar.projectKey=my:project

# --- optional properties ---

# defaults to project key
sonar.projectName=20211218-MarkWebTest
# defaults to 'not provided'
sonar.projectVersion=1.0
 
# Path is relative to the sonar-project.properties file. Defaults to .
sonar.sources=E:/Developer/PHP_WS/20211218-MarkWebTest
 
# Encoding of the source code. Default is default system encoding
sonar.sourceEncoding=UTF-8
```

### 1.3.3. 打開命令提示字元，輸入以下指令

```powershell
cd /d E:\Developer\PHP_WS\20211218-MarkWebTest

sonar-scanner
```

![](https://markweb.idv.tw/uploads/upload_7b2f480a86a8906fc9deb800bfd76d00.png)

![](https://markweb.idv.tw/uploads/upload_63ab189efc2402572827fa8f5927dec4.png)


### 1.3.4. 打開[http://localhost:9000](http://localhost:9000/projects)

看到此畫面代表成功

![](https://markweb.idv.tw/uploads/upload_14b9059bb985972541955d27d39a0054.png)

