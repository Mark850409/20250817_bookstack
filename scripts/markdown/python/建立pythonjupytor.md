---
title: 建立pythonjupytor
updated: 2024-07-21 05:25:51Z
created: 2023-08-04 08:26:29Z
tags:
  - python
  - jupytor
---

# 1. 建立pythonjupytor

## 1.1. 簡介
學習如何使用pythonjupytor

## 1.2. 目錄

- [1. 建立pythonjupytor](#1-建立pythonjupytor)
  - [1.1. 簡介](#11-簡介)
  - [1.2. 目錄](#12-目錄)
  - [1.3.  操作步驟](#13--操作步驟)
    - [1.3.1. 事前準備](#131-事前準備)
    - [1.3.2. 撰寫DockerFile](#132-撰寫dockerfile)
    - [1.3.3. 執行部屬指令](#133-執行部屬指令)
      - [1.3.3.1. 請先切換到根目錄下](#1331-請先切換到根目錄下)
      - [1.3.3.2. 開始部屬，執行以下命令](#1332-開始部屬執行以下命令)
      - [1.3.3.3. 參考此文章，如何推送至docker registry hub](#1333-參考此文章如何推送至docker-registry-hub)
      - [1.3.3.4. 撰寫docker-compose.yml](#1334-撰寫docker-composeyml)
      - [1.3.3.5. 部屬成功!!!](#1335-部屬成功)
      - [1.3.3.6. 查看是否能進入主畫面!!!](#1336-查看是否能進入主畫面)


## 1.3.  操作步驟

### 1.3.1. 事前準備
* 撰寫 個python專案檔
* 金鑰目錄
* jupyter_notebook_config.py jupyter設定檔
* DockerFile 定要和所有檔案放同 層目錄

![](https://markweb.idv.tw/uploads/upload_f8b2cfaac0558649e274ba20b7ad2ce3.png)

<!--more-->

### 1.3.2. 撰寫DockerFile

```Dockerfile
FROM brokyz/notebook_hub
RUN apt-get -y update && apt install vim -y && apt-get dist-upgrade -y && apt-get install mariadb-server-10.6 -y && apt install net-tools -y && apt-get install python3-dev libmysqlclient-dev -y && pip3 install Flask-Waitress && pip3 install ipython-sql && pip install mysql-connector-python-rf && pip install mysqlclient
COPY jupyter_notebook_config.py /root/.jupyter/
COPY 20230613_jupyter /root/notebook
COPY letsencrypt /etc
```

### 1.3.3. 執行部屬指令

#### 1.3.3.1. 請先切換到根目錄下

![](https://markweb.idv.tw/uploads/upload_26fc2b893baef68e38d2270e79dc6abe.png)

#### 1.3.3.2. 開始部屬，執行以下命令
```docker
docker build --network=host -t myjupyter:1.0 .
```

#### 1.3.3.3. 參考此文章，如何推送至docker registry hub
![](https://markweb.idv.tw/uploads/upload_4a8ffb7156ea2ce9b725d33ea7bc2a93.png)


#### 1.3.3.4. 撰寫docker-compose.yml
```yaml
version: "3"
services:
  datascience-notebook:
      image: markweb.idv.tw:29443/mydockerrepo/myjupyter
      environment:
        PASSWORD: mark850409
      volumes: #將設定檔與主機位置做綁定
      - type: bind
        source: /media/markhsu/Data3/DockerProtainer/jupyter/config/jupyter_notebook_config.py
        target: /root/.jupyter/jupyter_notebook_config.py
        read_only: true
      - /media/markhsu/Data3/DockerProtainer/jupyter/workspace:/root/notebook
      - /media/markhsu/Data3/DockerProtainer/jupyter/etc/letsencrypt/live/markweb.idv.tw:/etc/letsencrypt/live/markweb.idv.tw
      ports:
        - 8888:8888 #更改外部進入的埠號，若無必要也可以都設為 8888
        - 8889:5000 #python flask server使用
      container_name: datascience-notebook-container 
  apache:
    image: php:7.4-apache
    restart: always
    ports:
      - '30443:30443' #可使用反向代理導向至8889服務
    volumes:
      - /media/markhsu/Data3/DockerProtainer/jupyter/etc/apache2:/etc/apache2
      - /media/markhsu/Data3/DockerProtainer/jupyter/etc/letsencrypt/live/markweb.idv.tw:/etc/letsencrypt/live/markweb.idv.tw 
volumes:
    data: #確保你下次重新開容器時，原先編輯的資料還會被保留下來
```

#### 1.3.3.5. 部屬成功!!!
![](https://markweb.idv.tw/uploads/upload_5a972a26e9c9187707105d892a7cd236.png)


#### 1.3.3.6. 查看是否能進入主畫面!!!
![](https://markweb.idv.tw/uploads/upload_ed49ecda269e3fba3fd38feb30d4a9b3.png)
