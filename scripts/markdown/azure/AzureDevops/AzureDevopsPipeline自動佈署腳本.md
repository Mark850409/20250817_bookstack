---
title: AzureDevopsPipeline自動佈署腳本
updated: 2024-07-24 08:09:53Z
created: 2024-07-13 15:34:54Z
latitude: 25.0329694
longitude: 121.5654177
altitude: 0
tags:
  - Azure
  - Devops
  - Pipeline
---

# 1. AzureDevopsPipeline自動佈署腳本

## 1.1. 簡介

`自動化雲端佈署`python，免去`人工建置`的困擾

## 1.2. 專案結構
```
MyPython
├─ azure-pipelines.yml
├─ python
│  ├─ .env
│  ├─ docker-compose.yml
│  ├─ mypython
│  │  ├─ apache
│  │  │  ├─ 000-default.conf
│  │  │  ├─ apache2.conf
│  │  │  ├─ conf-available
│  │  │  │  ├─ charset.conf
│  │  │  │  ├─ javascript-common.conf
│  │  │  │  ├─ localized-error-pages.conf
│  │  │  │  ├─ other-vhosts-access-log.conf
│  │  │  │  ├─ security.conf
│  │  │  │  └─ serve-cgi-bin.conf
│  │  │  ├─ conf-enabled
│  │  │  │  ├─ charset.conf
│  │  │  │  ├─ javascript-common.conf
│  │  │  │  ├─ localized-error-pages.conf
│  │  │  │  ├─ other-vhosts-access-log.conf
│  │  │  │  ├─ security.conf
│  │  │  │  └─ serve-cgi-bin.conf
│  │  │  ├─ envvars
│  │  │  ├─ letsencrypt
│  │  │  │  └─ live
│  │  │  │     └─ markweb.idv.tw
│  │  │  │        ├─ cert.pem
│  │  │  │        ├─ chain.pem
│  │  │  │        ├─ fullchain.pem
│  │  │  │        ├─ privkey.pem
│  │  │  │        └─ README
│  │  │  ├─ magic
│  │  │  ├─ mods-available
│  │  │  ├─ mods-enabled
│  │  │  ├─ ports.conf
│  │  │  ├─ sites-available
│  │  │  │  ├─ 000-default.conf
│  │  │  │  └─ default-ssl.conf
│  │  │  └─ sites-enabled
│  │  │     └─ 000-default.conf
│  │  ├─ DigiCertGlobalRootCA.crt.pem
│  │  ├─ Dockerfile
│  │  ├─ letsencrypt
│  │  │  └─ live
│  │  │     └─ markweb.idv.tw
│  │  │        ├─ cert.pem
│  │  │        ├─ chain.pem
│  │  │        ├─ fullchain.pem
│  │  │        ├─ privkey.pem
│  │  │        └─ README
│  │  ├─ main.py
│  │  ├─ requirements.txt
│  │  └─ serve-cgi-bin.conf
│  └─ phpmyadmin
│     ├─ Dockerfile
│     └─ php.ini
└─ README.md
```

## 1.3. 目錄

- [1. AzureDevopsPipeline自動佈署腳本](#1-azuredevopspipeline自動佈署腳本)
  - [1.1. 簡介](#11-簡介)
  - [1.2. 專案結構](#12-專案結構)
  - [1.3. 目錄](#13-目錄)
    - [1.3.1. 使用方式](#131-使用方式)
      - [1.3.1.1. 設置git環境並產生金鑰](#1311-設置git環境並產生金鑰)
    - [1.3.2. 拉取git存放庫目錄到本地](#132-拉取git存放庫目錄到本地)
  - [1.4. 執行步驟](#14-執行步驟)
    - [1.4.1. 建立AZURE DEVOPS專案](#141-建立azure-devops專案)
    - [1.4.2. 建立Pipelinnes](#142-建立pipelinnes)
    - [1.4.3. 建立APP SERVICE](#143-建立app-service)
    - [1.4.4. 建立AZURE Container Registry 存放庫](#144-建立azure-container-registry-存放庫)
    - [1.4.5. 建立MYSQL資料庫](#145-建立mysql資料庫)
    - [1.4.6. 建立Pipelines環境變數](#146-建立pipelines環境變數)
    - [1.4.7. 開始撰寫腳本](#147-開始撰寫腳本)
      - [1.4.7.1. 建立`azure-pipelines.yml`，輸入以下指令](#1471-建立azure-pipelinesyml輸入以下指令)
      - [1.4.7.2. 建立Python `DockerFile`，並輸入以下指令](#1472-建立python-dockerfile並輸入以下指令)
      - [1.4.7.3. 建立`main.py`，並輸入以下指令](#1473-建立mainpy並輸入以下指令)
      - [1.4.7.4. 建立`requirements.txt`，輸入以下指令](#1474-建立requirementstxt輸入以下指令)
      - [1.4.7.5. 建立`docker-compose.yml`，並輸入以下指令](#1475-建立docker-composeyml並輸入以下指令)
      - [1.4.7.6. 建立`.env`，並輸入以下指令](#1476-建立env並輸入以下指令)
      - [1.4.7.7. 新增Shell Script `AutoSPImport.sh` 並輸入以下指令](#1477-新增shell-script-autospimportsh-並輸入以下指令)
      - [1.4.7.8. 新增一隻SP `procCreateTableSchema.sql`](#1478-新增一隻sp-proccreatetableschemasql)
  - [1.5. 執行結果](#15-執行結果)
    - [1.5.1. 查看執行結果](#151-查看執行結果)
  - [1.6. 問題排除](#16-問題排除)



### 1.3.1. 使用方式

#### 1.3.1.1. 設置git環境並產生金鑰
1. 安裝好`git`環境
2. 開啟`cmd`,輸入以下指令
```shell
ssh keygan -b 4096 -c ['你的email']
```
3. 將產生的`金鑰`放在以下路徑 
```batch
C：\users\['你的使用者名稱']\.ssh
```
![image-20231018202934452](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/image-20231018202934452.png)


4. 進入`AZURE DEVOPS` 的`使用者設定`，把剛剛產生的`public key 複製`到上面

![image-20231018203040256](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/gCde526cb00-image-20231018203040256.png)

<!--more-->

### 1.3.2. 拉取git存放庫目錄到本地

1. 在windows`建立 個新目錄`，開啟`cmd`，輸入以下指令，成功畫面如下圖

```shell
git clone ['你的倉庫URL位址']
```
2. `倉庫的URL`可以在這邊找到

![image-20231019094128649](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/5b9eca4b-image-20231019094128649.png)

![image-20231018203309314](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/b3b79905-image-20231018203309314.png)

<!--more-->

## 1.4. 執行步驟

### 1.4.1. 建立AZURE DEVOPS專案

輸入專案名稱、選擇私有專案，點選create

![image-20231018203636277](https://markweb.idv.tw/uploads/image-20231018203636277.png)

### 1.4.2. 建立Pipelinnes

點選`AZURE存放庫`

![image-20231018203929816](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/V6k87c25d83-image-20231018203929816.png)

選擇`mypython`
![image-20231018203959065](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/5abb4c53-image-20231018203959065.png)

建立 個`新的pipelines`
![image-20231018204044225](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/4293054c-image-20231018204044225.png)

開始撰寫`pipelines`
![image-20231018204347774](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/g2i4dfdaf79-image-20231018204347774.png)

### 1.4.3. 建立APP SERVICE

點選建立`Web應用程式`
![image-20231018204551684](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/fgk4d1b208d-image-20231018204551684.png)

填寫`紅框處`相關資訊
![image-20231018204743294](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/dd9d4e9d-image-20231018204743294.png)

選擇`定價方案`
![image-20231018204808282](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/5BM03279ce6-image-20231018204808282.png)

選擇`單 容器→快速入門`
![image-20231018205007447](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/2ff5eaf0-image-20231018205007447.png)

點選`啟用公開存取`
![image-20231018205037346](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/da6d816c-image-20231018205037346.png)

點選`Application Insights`
![image-20231018205054750](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/WXX83746ebb-image-20231018205054750.png)

看個人情況決定是否`建立標籤`
![image-20231018205126436](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/05c4ec3b-image-20231018205126436.png)

點選建立`Web應用程式`
![image-20231018205157355](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/4fc0588a-image-20231018205157355.png)



### 1.4.4. 建立AZURE Container Registry 存放庫

點選`Container Registry`
![image-20231018205242702](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/360204f7-image-20231018205242702.png)

輸入`紅框處`相關內容
![image-20231018205413828](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/4Bv200c1e50-image-20231018205413828.png)

點選`下 步`
![image-20231018205435882](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/9de950ec-image-20231018205435882.png)

點選`下 步`
![image-20231018205448309](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/tVz1a44c73a-image-20231018205448309.png)

看個人情況決定是否`建立標籤`
![image-20231018205516050](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/e1a02b21-image-20231018205516050.png)





AZURE Container Registry 存放庫設定

存放庫建立完成後，請先進入`設定`頁面，將`管理員權限`開啟
![image-20231018205728327](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/e2e1d3c3-image-20231018205728327.png)


存放庫可查看推送上去的`映象檔`
![image-20231018205921457](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/Nv1d3b09b24-image-20231018205921457.png)

### 1.4.5. 建立MYSQL資料庫

點選`建立`
![image-20231018210311672](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/73e2830d-image-20231018210311672.png)

選擇`彈性伺服器`
![image-20231018210339090](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/MfU75d45ad3-image-20231018210339090.png)

輸入`紅框處`相關資訊
![image-20231018210626261](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/8Bvc5c4f055-image-20231018210626261.png)

點選只有`mysql驗證`，並輸入下方相關資訊
![image-20231018210736879](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/8ab91026-image-20231018210736879.png)

這邊`公用存取`選項 定要勾
![image-20231018210826611](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/ChTecbe9a84-image-20231018210826611.png)

`防火牆規則`建立(可全開也可不全開)
![image-20231018210921019](https://markweb.idv.tw/uploads/image-20231018210921019.png)

點選`下 步`
![image-20231018211001017](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/lXg372c6856-image-20231018211001017.png)

看個人情況決定是否`建立標籤`
![image-20231018211031391](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/kFS30eebc42-image-20231018211031391.png)

點選建立
![image-20231018211140671](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/bEW841a3bc7-image-20231018211140671.png)

資料庫容器建置完成後，請`新增` 個`資料庫`
![image-20231018211304595](https://markweb.idv.tw/uploads/image-20231018211304595.png)

這邊可以查看`連線相關帳密`
![image-20231018211738319](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/3MGc0562744-image-20231018211738319.png)

### 1.4.6. 建立Pipelines環境變數

![image-20231018212513993](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/a78a4e9f-image-20231018212513993.png)

### 1.4.7. 開始撰寫腳本

#### 1.4.7.1. 建立`azure-pipelines.yml`，輸入以下指令

```yaml
# git pipelines觸發
trigger:
- 'none'

# 定義變數群組
variables:
  - group: Azure Registry Login

# 腳本執行進入點
stages:
- stage: AzureWebAppServiceBuild
  displayName: "AzureWebAppServiceBuild"
  jobs:
  - job: PythonImageBuild
    displayName: "PythonImageBuild"
    steps:   
    #DockerCompose
    - task: DockerCompose@0
      inputs:
        containerregistrytype: 'Azure Container Registry'
        azureSubscription: 'Azure for Students(1)(eb76b2aa-fd5d-4aed-a836-a830c995d714)'
        azureContainerRegistry: '{"loginServer":"godprojectregistry.azurecr.io", "id" : "/subscriptions/eb76b2aa-fd5d-4aed-a836-a830c995d714/resourceGroups/myPythonServer/providers/Microsoft.ContainerRegistry/registries/GodProjectRegistry"}'
        dockerComposeFile: 'python/docker-compose.yml'
        action: 'Run a Docker Compose command'
        dockerComposeCommand: '--env-file python/.env up -d --build'
    #DockerImages
    - script: |
             docker images
      displayName: 'AZURE DOCKER IMAGE LIST'
    #DockerBuildAndPush
    - script: |
             docker login $(REGISTRY_HOST) -u $(REGISTRY_USER) -p $(REGISTRY_PASSWORD)
             docker tag mypythonweb:1.0 $(REGISTRY_IMAGE)
             docker push $(REGISTRY_IMAGE)
      displayName: 'AZURE DOCKER REGISTRY LOGIN AND PUSH IMAGE'
    #AzureWebAppContainer
    - task: AzureWebAppContainer@1
      displayName: 'AZURE WEB APP SERVICE BUILD'
      inputs:
        azureSubscription: 'Azure for Students(eb76b2aa-fd5d-4aed-a836-a830c995d714)'
        appName: 'myPythonServer'
        containers: '$(REGISTRY_IMAGE)'
    #CALL STORE PROCEDURE TO CREATE DB AND INSERT DATA
    - task: ShellScript@2
      displayName: 'CALL SP TO CREATE DB AND INSERT DATA'
      inputs:
        scriptPath: 'AutoSPImport.sh'
```
#### 1.4.7.2. 建立Python `DockerFile`，並輸入以下指令

```Dockerfile
FROM php:7.4-apache
COPY requirements.txt ./
RUN apt-get -y update \
&& apt-get install -y python3 python3-pip \
&& apt install vim -y \
&& a2enmod rewrite \
&& a2enmod ssl \
&& a2enmod headers \
&& a2enmod proxy \
&& a2enmod proxy_http \
&& a2enmod proxy_balancer \
&& a2enmod cgi \
&& apt-get install -y --no-install-recommends \
&& python3 -m pip install --upgrade pip \ 
&& pip install --no-cache-dir -r requirements.txt
COPY letsencrypt /etc/letsencrypt/
COPY apache/apache2.conf /etc/apache2/
COPY apache/000-default.conf /etc/apache2/sites-available/
COPY apache/ports.conf /etc/apache2/
COPY main.py /var/www/html
COPY DigiCertGlobalRootCA.crt.pem /var/www/html
WORKDIR /var/www/html
RUN chmod +X main.py && chmod 755 main.py 
EXPOSE 8000
```   

#### 1.4.7.3. 建立`main.py`，並輸入以下指令

```python
# !/usr/bin/python3
from wsgiref.handlers import CGIHandler
from flask import Flask
import pymysql
import os
app = Flask(__name__)

# 這邊建立MYSQL連線資訊

@app.route("/")   
def index():
    # 建立資料庫連接
    db = pymysql.connect(
      host='[請在mysql server上查看]',
      user='[請在mysql server上查看]',
      password='[請在mysql server上查看]',
      database='[請在mysql server上查看]',
      ssl_disabled='True')
    
    cursor = db.cursor()

    # 讀取資料
    cursor.execute("SELECT * FROM student;")
    rows = cursor.fetchall()
    print("Read",cursor.rowcount,"row(s) of data.")

    # 印出資料
    for row in rows:
      print(row)

    # 釋放連線
    db.commit()
    cursor.close()
    db.close()

    return "Done"
# 啟動CGI SERVER
if __name__ == "__main__":
  CGIHandler().run(app)
```
#### 1.4.7.4. 建立`requirements.txt`，輸入以下指令
```
markdown==3.1.1
mysql-connector-python==8.0.17
protobuf==3.6.1
markupsafe==2.1.1
Jinja2==3.1.2
Flask == 2.0.1
Werkzeug==2.2.2
pymysql==1.1.0
```
#### 1.4.7.5. 建立`docker-compose.yml`，並輸入以下指令
```yaml
version: '3.3'
services:
  python:
    build: ./mypython
    container_name: mypythonweb
    image: mypythonweb:${BUILD_NUMBER}
    restart: always
    ports:
      - "${PYTHON_PORTS}:80"
    volumes:
      - $SourcesDirectory/etc/apache2:/etc/apache2/
      - $SourcesDirectory/etc/letsencrypt/live/markweb.idv.tw:/etc/letsencrypt/live/markweb.idv.tw
      - $SourcesDirectory/var/www/html:/var/www/html
```
#### 1.4.7.6. 建立`.env`，並輸入以下指令
```title:".env"
# MARIADB參數設定
MARIADB_ROOT_PASSWORD=[自行定義]
MARIADB_DATABASE=[自行定義]
MARIADB_USER=[自行定義]
MARIADB_PASSWORD=[自行定義]
MARIADB_PORTS=8088

# python參數設定
PYTHON_PORTS=80

# PHPMYADMIN參數設定
PHPMYADMIN_PORTS=8080
MYSQL_ROOT_PASSWORD=[自行定義]
BUILD_NUMBER=1.0
```
#### 1.4.7.7. 新增Shell Script `AutoSPImport.sh` 並輸入以下指令
```bash
#!/bin/bash
# ====================================================================
# bash script Name     : procCreateTableSchema
# Function    : CreateStockTable
# Author      : Mark
# Create Date : 2023-10-26
# Parameter   : 
# Modify His  : 
# ===================================================================
#參數定義
USER=[可以在AZURE MYSQL上查看]
PASSWORD=[可以在AZURE MYSQL上查看]
HOST=[可以在AZURE MYSQL上查看]
DB=stock
SQL_NAME=procCreateTableSchema.sql
#如果資料庫不存在就建立一個新的
mysql -h $HOST -u $USER -p$PASSWORD -e "source $SQL_NAME;" -e "use $DB;"  && \
mysql -h $HOST -u $USER -p$PASSWORD -e "use $DB;" -e 'call procExportTableSchemaAndInsertTable("$DB");' 
```
#### 1.4.7.8. 新增一隻SP `procCreateTableSchema.sql`
```sql 
-- ====================================================================
-- SP Name     : procExportTableSchemaAndInsertTable
-- Function    : 批次將各資料表匯出table schema，並複製 份到總表進行管理
-- Author      : Mark
-- Create Date : 2023-10-26
-- Parameter   : DBName
-- Modify His  : 
-- (1) 2023-10-26 : Mark    : CREATE 
-- ===================================================================

-- 如果stock資料庫不存在就建立 個新的
CREATE DATABASE IF NOT EXISTS stock DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
-- 使用stock資料庫
USE stock;
DELIMITER $$
-- 如果PROCEDURE存在就先移除                                                                                                                                                                   
DROP PROCEDURE IF EXISTS procExportTableSchemaAndInsertTable $$       
-- 建立PROCEDURE(傳入資料庫名稱參數)                                                                                                                           
CREATE PROCEDURE procExportTableSchemaAndInsertTable(DBName varchar(255))    
BEGIN   
		        -- 變數宣告
			-- 1. 資料表集合名稱
			-- 2. 取得最後 張資料表
			-- 3. 時間戳記
        DECLARE table_name VARCHAR(255);                                                                                                                                        
        DECLARE end_of_tables INT DEFAULT 0;
        DECLARE mylocaltimestamp DATETIME;
		
        -- 利用SQL取出指定資料庫裡面所有資料表的list，直到最後 張資料表為止
        DECLARE cur CURSOR FOR                                                                                                                                                  
            SELECT t.table_name                                                                                                                                                 
            FROM information_schema.tables t                                                                                                                                    
            WHERE t.table_schema = DBName AND t.table_type='BASE TABLE' AND t.table_name <> 'stock_all_data';                                                                                                 
        DECLARE CONTINUE HANDLER FOR NOT FOUND SET end_of_tables = 1;   
        
		-- 開始建立6張資料表
		DROP TABLE IF EXISTS stock_daily;
		CREATE TABLE IF NOT EXISTS stock_daily
		(
			sdate varchar(10),
			id varchar(10),
			sname varchar(255),
			trs_qty decimal(18, 0),
			trs_count decimal(18, 0),
			trs_amt decimal(18, 0),
			open_price decimal(18, 2),
			h_price decimal(18, 2),
			l_price decimal(18, 2),
			close_price decimal(18, 2),
			s_status varchar(255),
			dec_price decimal(18, 2),
			lb_price decimal(18, 2),
			lb_amt decimal(18, 2),
			ls_price decimal(18, 2),
			ls_amt decimal(18, 2),
			PE decimal(18, 2)
		);
        
		DROP TABLE IF EXISTS stock_list;
		CREATE TABLE IF NOT EXISTS stock_list
		(
			id varchar(10),
			sname varchar(255),
			stock_attr varchar(255),
			industry varchar(255),
			CONSTRAINT PK_stock_list
				PRIMARY KEY (id)
		);

		DROP TABLE IF EXISTS stock_monthly_revenue;
		CREATE TABLE IF NOT EXISTS stock_monthly_revenue
		(
			yyyymm varchar(6),
			id varchar(10),
			sname varchar(255),
			month_amt decimal(18, 0),
			pre_m_amt decimal(18, 0),
			pre_y_amt decimal(18, 0),
			pre_m_percent decimal(18, 2),
			pre_y_percent decimal(18, 2),
			sum_amt decimal(18, 0),
			per_sum_amt decimal(18, 0),
			sum_percent decimal(18, 2),
			memo_str varchar(255),
			CONSTRAINT PK_stock_monthly_revenue
				PRIMARY KEY
				(
					id,
					yyyymm
				)
		);

		DROP TABLE IF EXISTS stock_daily_3;
		CREATE TABLE IF NOT EXISTS stock_daily_3
		(
			sdate varchar(10),
			id varchar(10),
			f_qty decimal(18, 0),
			i_qty decimal(18, 0),
			s_qty decimal(18, 0),
			t_qty decimal(18, 0),
			est_f_qty decimal(18, 0),
			est_i_qty decimal(18, 0),
			est_s_qty decimal(18, 0),
			est_t_qty decimal(18, 0),
			trs_f_percent decimal(18, 2),
			trs_3_percent decimal(18, 2),
			CONSTRAINT PK_stock_daily_3
				PRIMARY KEY
				(
					id,
					sdate
				)
		);

		DROP TABLE IF EXISTS stock_daily_MT;
		CREATE TABLE IF NOT EXISTS stock_daily_MT
		(
			sdate varchar(10),
			id varchar(10),
			mt_b_qty decimal(18, 0),
			mt_s_qty decimal(18, 0),
			mt_r_qty decimal(18, 0),
			mt_qty decimal(18, 0),
			mt_dec_qty decimal(18, 0),
			mt_limit_qty decimal(18, 0),
			mt_use_percent decimal(18, 2),
			ss_b_qty decimal(18, 0),
			ss_s_qt decimal(18, 0),
			ss_r_qty decimal(18, 0),
			ss_qty decimal(18, 0),
			ss_dec_qty decimal(18, 0),
			ms_percent decimal(18, 2),
			ms_dec_qty decimal(18, 0),
			CONSTRAINT PK_stock_daily_MT
				PRIMARY KEY
				(
					id,
					sdate
				)
		);

		DROP TABLE IF EXISTS stock_daily_MR;
		CREATE TABLE IF NOT EXISTS stock_daily_MR
		(
			sdate varchar(10),
			id varchar(50),
			id_sub varchar(50),
			id_mr varchar(50),
			mrname varchar(255),
			b_qty decimal(18, 0),
			s_qty decimal(18, 0),
			dec_qty decimal(18, 0),
			dstatus int,
			trs_percent decimal(18, 2),
			CONSTRAINT PK_stock_daily_MR
				PRIMARY KEY
				(
					id,
					sdate
				)
		);
		
	   -- 如果總表存在先行移除，避免資料重複
	   SET @drop_table=CONCAT("DROP TABLE IF EXISTS stock_all_data");
       PREPARE stmt2 FROM @drop_table;                                                                                                                                               
	   EXECUTE stmt2; 
        
        OPEN cur;                                                                                                                                                               
		
        -- 迴圈開始
        tables_loop: LOOP                   
            	
	    -- 將資料集透過迴圈取出，最後 張表時強制離開迴圈
            FETCH cur INTO table_name;             			
            IF end_of_tables = 1 THEN                                                                                                                                           
                LEAVE tables_loop;                                                                                                                                              
            END IF;                                                                                                                                                             
			
            -- 使用CONCAT串接SQL語法(這 段是查看SQL結果，可以拿掉不執行)
            -- SET @show_schema = CONCAT("desc"," ",DBName,".",table_name);
            -- 建立PREPARE STATEMENT，並執行
            --  PREPARE stmt FROM @show_schema;                                                                                                                                               
            -- EXECUTE stmt;     
     
            -- 判斷不同的資料表，給予不同的中文欄位名稱
			CASE table_name
			WHEN 'stock_list' THEN
			   SET @table_type='證券清冊';
			   SET @caseSQL = CONCAT("(
						CASE 
							WHEN COLUMN_NAME='id' THEN '證券代號'
                            WHEN COLUMN_NAME='sname' THEN '證券名稱' 
                            WHEN COLUMN_NAME='stock_attr' THEN '上市上櫃類別'
                            WHEN COLUMN_NAME='industry' THEN '產業分類'
						ELSE 'null'
						END)  as descs"
						);
                        
			WHEN  'stock_daily' THEN
			   SET @table_type='每日收盤資訊';
			   SET @caseSQL=CONCAT("(
						CASE 
							WHEN COLUMN_NAME='sdate' THEN '交易日期' 
							WHEN COLUMN_NAME='id' THEN '證券代號'
                            WHEN COLUMN_NAME='sname' THEN '證券名稱'
                            WHEN COLUMN_NAME='trs_qty' THEN '成交股數'
                            WHEN COLUMN_NAME='trs_count' THEN '成交筆數'
                            WHEN COLUMN_NAME='trs_amt' THEN '成交金額'
                            WHEN COLUMN_NAME='open_price' THEN '開盤價'
                            WHEN COLUMN_NAME='h_price' THEN '最高價'
                            WHEN COLUMN_NAME='l_price' THEN '最低價'
                            WHEN COLUMN_NAME='close_price' THEN '收盤價'
                            WHEN COLUMN_NAME='s_status' THEN '漲跌(+/-)'
                            WHEN COLUMN_NAME='dec_price' THEN '漲跌價差'
                            WHEN COLUMN_NAME='lb_price' THEN '最後揭示買價'
                            WHEN COLUMN_NAME='lb_amt' THEN '最後揭示買量'
                            WHEN COLUMN_NAME='ls_price' THEN '最後揭示賣價'
                            WHEN COLUMN_NAME='ls_amt' THEN '最後揭示賣量'
                            WHEN COLUMN_NAME='PE' THEN '本益比'
						ELSE 'null'
						END)  as descs"
						);
                        
			   WHEN 'stock_monthly_revenue' THEN
			    SET @table_type='每月營收';
			   SET @caseSQL = CONCAT("(
						CASE 
							WHEN COLUMN_NAME='yyyymm' THEN '營收年月' 
							WHEN COLUMN_NAME='id' THEN '證券代號'
                            WHEN COLUMN_NAME='sname' THEN '證券名稱'
                            WHEN COLUMN_NAME='month_amt' THEN '當月營收'
                            WHEN COLUMN_NAME='pre_m_amt' THEN '上月營收'
                            WHEN COLUMN_NAME='pre_y_amt' THEN '去年當月營收'
                            WHEN COLUMN_NAME='pre_m_percent' THEN '上月比較增減(%)'
                            WHEN COLUMN_NAME='pre_y_percent' THEN '去年同月增減(%)'
                            WHEN COLUMN_NAME='sum_amt' THEN '當月累計營收'
                            WHEN COLUMN_NAME='per_sum_amt' THEN '去年累計營收'
                            WHEN COLUMN_NAME='sum_percent' THEN '前期比較增減(%)'
                            WHEN COLUMN_NAME='memo_str' THEN '備註'
						ELSE 'null'
						END)  as descs"
						);
                        
			WHEN 'stock_daily_3' THEN
               SET @table_type=' 大法人進出';
			   SET @caseSQL = CONCAT("(
						CASE 
							WHEN COLUMN_NAME='sdate' THEN '交易日期' 
							WHEN COLUMN_NAME='id' THEN '證券代號'
                            WHEN COLUMN_NAME='f_qty' THEN '外資'
                            WHEN COLUMN_NAME='i_qty' THEN '投信'
                            WHEN COLUMN_NAME='s_qty' THEN '自營商'
                            WHEN COLUMN_NAME='t_qty' THEN '單日合計'
                            WHEN COLUMN_NAME='est_f_qty' THEN '估計外資持股'
                            WHEN COLUMN_NAME='est_i_qty' THEN '估計投信持股'
                            WHEN COLUMN_NAME='est_s_qty' THEN '估計自營商持股'
                            WHEN COLUMN_NAME='est_t_qty' THEN '合計'
                            WHEN COLUMN_NAME='trs_f_percent' THEN '外資比例'
                            WHEN COLUMN_NAME='trs_3_percent' THEN ' 大法人比例'
						ELSE 'null'
						END) as descs"
						);
			WHEN 'stock_daily_mr' THEN
               SET @table_type='主力進出';
			   SET @caseSQL = CONCAT("(
						CASE 
							WHEN COLUMN_NAME='sdate' THEN '日期' 
							WHEN COLUMN_NAME='id' THEN '股票代號'
                            WHEN COLUMN_NAME='id_sub' THEN '券商代號'
                            WHEN COLUMN_NAME='id_mr' THEN '券商主代號'
                            WHEN COLUMN_NAME='mrname' THEN '券商名稱'
                            WHEN COLUMN_NAME='b_qty' THEN '買進'
                            WHEN COLUMN_NAME='s_qty' THEN '賣出'
                            WHEN COLUMN_NAME='dec_qty' THEN '買超'
                            WHEN COLUMN_NAME='dstatus' THEN '買or賣'
                            WHEN COLUMN_NAME='trs_percent' THEN '佔成交比重'
						ELSE 'null'
						END)  as descs"
						);
			WHEN 'stock_daily_mt' THEN
               SET @table_type='融資融券';
			   SET @caseSQL = CONCAT("(
						CASE 
							WHEN COLUMN_NAME='sdate' THEN '交易日期' 
							WHEN COLUMN_NAME='id' THEN '證券代號'
                            WHEN COLUMN_NAME='mt_b_qty' THEN '融資買進'
                            WHEN COLUMN_NAME='mt_s_qty' THEN '融資賣出'
                            WHEN COLUMN_NAME='mt_r_qty' THEN '融資現償'
                            WHEN COLUMN_NAME='mt_qty' THEN '融資餘額'
                            WHEN COLUMN_NAME='mt_dec_qty' THEN '融資增減'
                            WHEN COLUMN_NAME='mt_limit_qty' THEN '融資限額'
                            WHEN COLUMN_NAME='mt_use_percent' THEN '融資使用率'
                            WHEN COLUMN_NAME='ss_b_qty' THEN '融券賣出'
                            WHEN COLUMN_NAME='ss_s_qt' THEN '融券買進'
                            WHEN COLUMN_NAME='ss_r_qty' THEN '融券券償'
                            WHEN COLUMN_NAME='ss_qty' THEN '融券餘額'
                            WHEN COLUMN_NAME='ss_dec_qty' THEN '融券增減'
                            WHEN COLUMN_NAME='ms_percent' THEN '券資比'
                            WHEN COLUMN_NAME='ms_dec_qty' THEN '資券相抵'
						ELSE 'null'
						END)  as descs"
						);	

				ELSE BEGIN END;  
			END CASE;
            
				-- 建立總表資料表
				SET @create_table = CONCAT("CREATE TABLE IF NOT EXISTS stock_all_data(COLUMN_NAMES varchar(255),DATA_TYPE varchar(255),IS_NULLABLE varchar(255),COLUMN_KEY varchar(255),DESCS varchar(255),TABLE_TYPE varchar(255))");
                PREPARE stmt3 FROM @create_table;                                                                                                                                               
   			    EXECUTE stmt3; 
                
                -- 總表的資料來源是透過原先串好並取得的資料複製 份到stock_all_data
                SET @Insert_table = CONCAT("INSERT INTO stock_all_data (COLUMN_NAMES,DATA_TYPE,IS_NULLABLE,COLUMN_KEY,DESCS,TABLE_TYPE)");
				SET @join_table = CONCAT(@Insert_table,"select COLUMN_NAME,DATA_TYPE,IS_NULLABLE,COLUMN_KEY,",@caseSQL,",","'",@table_type,"'",' as TABLE_TYPE'" FROM information_schema.columns 
				where table_schema = '",DBName,"' AND table_name='",table_name,"'",";");  
                PREPARE stmt4 FROM @join_table;                                                                                                                                               
   			    EXECUTE stmt4; 
            
            -- 這 段供測試用
	    -- SELECT @join_table;
         
         -- 迴圈結束
        END LOOP;                                                                                                                                                               
        CLOSE cur;                                                                                                                                                              
    END $$                                                                                                                                                                      
DELIMITER ;

```


## 1.5. 執行結果

### 1.5.1. 查看執行結果

![image-20231018212224544](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/e666348c-image-20231018212224544.png)

![image-20231018212300671](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/4jq38a3c464-image-20231018212300671.png)

![image-20231018212335104](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/39d5353d-image-20231018212335104.png)

## 1.6. 問題排除

1. 請到APP SERVICE的組態設定，檢查紅框處設定是否正確
![image-20231019094703760](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/kEH4f69b9c0-image-20231019094703760.png)
2. 部署中心的設定可以檢查這個APP SERVICE目前和誰綁定，由此圖可以得知目前和DEVOPS做綁定
![image-20231019095015816](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/c9j90d219b6-image-20231019095015816.png)

3. 部署中心的紀錄可以查看APP SERVICE的是否啟動，也可點選重新整理或是下載來查看紀錄
![image-20231019095240503](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/md6f63109d5-image-20231019095240503.png)



