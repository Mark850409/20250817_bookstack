---
title: 建立python環境在docker上
updated: 2024-07-21 05:26:03Z
created: 2023-08-04 08:26:29Z
tags:
  - python
  - Docker
---

# 1. 建立python環境在docker上

## 1.1. 簡介
學習如何使用docker建立pythonc環境

## 1.2. 目錄

- [1. 建立python環境在docker上](#1-建立python環境在docker上)
  - [1.1. 簡介](#11-簡介)
  - [1.2. 目錄](#12-目錄)
  - [1.3. 操作步驟](#13-操作步驟)
    - [1.3.1.  事前準備](#131--事前準備)
    - [1.3.2. 撰寫DockerFile](#132-撰寫dockerfile)
    - [1.3.3. 執行部署指令](#133-執行部署指令)
      - [1.3.3.1. 請先切換到根目錄下](#1331-請先切換到根目錄下)
      - [1.3.3.2. 開始部屬，執行以下命令](#1332-開始部屬執行以下命令)
      - [1.3.3.3. 參考此文章，如何推送至docker registry hub](#1333-參考此文章如何推送至docker-registry-hub)
      - [1.3.3.4. 撰寫docker-compose.yml](#1334-撰寫docker-composeyml)
      - [1.3.3.5. 部屬成功!!!](#1335-部屬成功)
      - [1.3.3.6. 切換至apache目錄，打開設定檔](#1336-切換至apache目錄打開設定檔)
      - [1.3.3.7. 加入此行，設定python網站預設執行根目錄](#1337-加入此行設定python網站預設執行根目錄)
      - [1.3.3.8. 加入此行，設定python網站預設執行根目錄](#1338-加入此行設定python網站預設執行根目錄)
      - [1.3.3.9. 輸入網址，即可看到Helloworld的畫面](#1339-輸入網址即可看到helloworld的畫面)
    - [1.3.4. 同場佳映](#134-同場佳映)


## 1.3. 操作步驟

### 1.3.1.  事前準備
* .py 首頁範本檔
* requirements.txt python套件版本設定檔
* 網站設定檔與金鑰檔
* DockerFile 定要和所有檔案放同 層目錄

![](https://markweb.idv.tw/uploads/upload_aeb0b3420000db4352661d63186d81cf.png)

<!--more-->

### 1.3.2. 撰寫DockerFile

```docker
FROM php:7.4-apache
WORKDIR /var/www/html
ADD . /var/www/html
RUN apt-get -y update && apt-get install -y python3 python3-pip && apt install vim -y && a2enmod rewrite && a2enmod ssl && a2enmod socache_shmcb && a2enmod headers
RUN pip3 install --upgrade pip
WORKDIR /media/markhsu/Data3/DockerImage/apache/letsencrypt/live/markweb.idv.tw
COPY . /etc/apache2/letsencrypt/
WORKDIR /media/markhsu/Data3/DockerImage/apache
COPY apache2/apache2.conf /etc/apache2/
COPY apache2/sites-available/000-default.conf /etc/apache2/sites-available/
COPY apache2/ports.conf /etc/apache2/
RUN apt-get update && apt-get upgrade -y && apt install vim -y 
COPY requirements.txt ./
RUN pip3 install art 
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py /var/www/html
ENV LANG C.UTF-8
```


> [!note] 小提示
> 1. From 拉取官方映像檔
> 2. WORKDIR 設定工作目錄
> 3. RUN 執行CMD
> 4. COPY 指定目錄文件複製
> 5. ENV 設定環境變數

### 1.3.3. 執行部署指令

#### 1.3.3.1. 請先切換到根目錄下
```bash
cd /media/markhsu/Data3/DockerImage/python/
```
![](https://markweb.idv.tw/uploads/upload_a1aba57dff025a8e540a2f90e83402c4.png)

#### 1.3.3.2. 開始部屬，執行以下命令
```docker
docker build -t mypython:1.0 -f Dockerfile_NEW .
```
![](https://markweb.idv.tw/uploads/upload_e491c422a55511b1ab27cefab96b3b64.png)


> [!note] 小提示
> 1. -t image name
> 2. -f 指定要使用的Dockerfile路径


#### 1.3.3.3. 參考此文章，如何推送至docker registry hub
[docker registry hub](https://markweb.idv.tw/9CtToMRcTHuv3C3FgBdu6A?both)

#### 1.3.3.4. 撰寫docker-compose.yml

```yaml
version: '3'

services:
  # Database
  db:
    image: mysql:8.0.32
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: python
      MYSQL_USER: mark
      MYSQL_PASSWORD: mark850409
    ports:
      - '9005:3306'
    volumes:
      - /media/markhsu/Data3/DockerProtainer/python/db_data:/var/lib/mysql
    restart: always
    networks:
      - python
  # phpmyadmin
  phpmyadmin:
    depends_on:
      - db
    image: phpmyadmin/phpmyadmin
    restart: always
    ports:
      - '9003:80'
    environment:
      PMA_HOST: db
      PMA_ABSOLUTE_URI: https://markweb.idv.tw:28443
      MYSQL_ROOT_PASSWORD: root
      MYSQL_USER: mark
      MYSQL_PASSWORD: mark850409
    networks:
      - python
  python:
    image: mypythonweb5:latest #請在這邊放至自己部屬好的image
    restart: always
    ports:
      - '9004:80' #設定pyhton預設執行的port
      - '27443:27443'
      - '28443:28443'
    volumes:
      - /media/markhsu/Data3/DockerProtainer/python/etc/apache2:/etc/apache2
      - /media/markhsu/Data3/DockerProtainer/python/var/www/html:/var/www/html
      - /media/markhsu/Data3/DockerProtainer/python/etc/letsencrypt/live/markweb.idv.tw:/etc/letsencrypt/live/markweb.idv.tw
networks:
  python:
```

#### 1.3.3.5. 部屬成功!!!
![](https://markweb.idv.tw/uploads/upload_b97f6f0e586573331468fa259ff63703.png)

#### 1.3.3.6. 切換至apache目錄，打開設定檔
```bash
 cd /media/markhsu/Data3/DockerProtainer/python/etc/apache2
 vim apache2.conf
```
![](https://markweb.idv.tw/uploads/upload_d39a5bf7d783a2448c6ad48e8874d943.png)

#### 1.3.3.7. 加入此行，設定python網站預設執行根目錄
```bash
ScriptAlias /cgi-bin/ /var/www/html/
```
![](https://markweb.idv.tw/uploads/upload_d678909a15d50b4f74f67cc04b4f034d.png)

#### 1.3.3.8. 加入此行，設定python網站預設執行根目錄

```bash
vim /etc/apache2/conf-enabled/serve-cgi-bin.conf
```

![](https://markweb.idv.tw/uploads/upload_d40ad34cc9068c3c4e23068a736852e4.png)


#### 1.3.3.9. 輸入網址，即可看到Helloworld的畫面

![](https://markweb.idv.tw/uploads/upload_a25fe363d1e2734d7d25e83ccf426b54.png)

### 1.3.4. 同場佳映


> [!note] 小提示
> 如果發現有找不到python首頁的狀況...
> 請參考步驟8的圖片有說明...


![](https://markweb.idv.tw/uploads/upload_f05fadf2513f553adbff653bc28976f1.png)
