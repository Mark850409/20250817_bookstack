---
title: 安裝Docker
updated: 2024-07-23 13:28:36Z
created: 2023-08-04 08:26:29Z
tags:
  - Docker
---

# 1 Docker環境建置

## 1.1 簡介
學習如何建立Docker環境

## 1.2 目錄

- [1 Docker環境建置](#1-docker環境建置)
  - [1.1 簡介](#11-簡介)
  - [1.2 目錄](#12-目錄)
  - [1.3 、安裝Docker](#13-安裝docker)
  - [1.4 、安裝DockerCompose](#14-安裝dockercompose)
  - [1.5 、常用指令](#15-常用指令)
    - [1.5.1 docker run](#151-docker-run)
    - [1.5.2 docker logs](#152-docker-logs)
    - [1.5.3 docker volume ls](#153-docker-volume-ls)
    - [1.5.4 docker network ls](#154-docker-network-ls)
    - [1.5.5 docker inspect](#155-docker-inspect)
    - [1.5.6 docker ps -a](#156-docker-ps--a)
    - [1.5.7 docker search](#157-docker-search)
  - [1.6 、建立Dockerfile(用來產生image)](#16-建立dockerfile用來產生image)
  - [1.7 、複製檔案到docker容器](#17-複製檔案到docker容器)
  - [1.8 、執行dockerfile產生image](#18-執行dockerfile產生image)
  - [1.9 、執行docker](#19-執行docker)
  - [1.10 、docker-compose.yaml範例](#110-docker-composeyaml範例)



## 1.3 、安裝Docker

1.  更新apt安裝包以及apt所需的相關套件

```bash
sudo apt-get update

sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

2.  加入docker的官方GPG Key:

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

3.  設定repository:

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

4.  安裝Docker Engine

```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

5.  確認是否安裝成功

```bash
sudo docker run hello-world
```

* * *
<!--more-->

## 1.4 、安裝DockerCompose

```bash
sudo apt-get update
sudo apt-get install docker-compose-plugin
docker compose version
```

* * *

## 1.5 、常用指令

### 1.5.1 docker run

- -d 就是指在背景運行啦，如果沒有下的這個指令的話就會直接印出所有目前所啟動 container 在 Console 會輸出的訊息
- -v 就是設定 volume
- -e 就是設定 些環境變數的值
- –net 指定要將 container 掛在哪 個自定義的網路底下，這個以後會再細談
- -i 在這裡沒有，但指的是 interactive，代表你可以直接跟像是**bash**或是**sh**等的指令互動，通常要搭配 -t 才能看到其回應

### 1.5.2 docker logs

拿來輸出 container 本身的 log 囉，預設 container 的輸出就是這個地方，除非有異動，不然都可以看得到日誌的:

### 1.5.3 docker volume ls

可以看到目前所有由 docker 管控的 volume

### 1.5.4 docker network ls

可以看到目前所有由 docker 管控的 network

### 1.5.5 docker inspect

可以拿來檢視 docker 物件的詳細資訊，比方說 docker inspect rabbit，就可以看到 rabbit 這個 container 它的 ip，volume, network …等很多很多的資訊

### 1.5.6 docker ps -a

可以看到目前所有被管控的 container，不論它是開著關著甚至是剛建立都可以看到。

### 1.5.7 docker search

這個可以拿來找 些 docker hub 上比較常見的 Application 相關的 image。

* * *

## 1.6 、建立Dockerfile(用來產生image)

```Dockerfile
FROM php:7.4.33-apache
RUN apt-get update 
COPY /etc/letsencrypt/live/markweb.idv.tw/cert.pem /etc/apache2/ssl
COPY /etc/letsencrypt/live/markweb.idv.tw/privkey.pem /etc/apache2/ssl
COPY /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available
RUN a2enmod rewrite
RUN a2enmod ssl
RUN service apache2 restart
```

* * *

## 1.7 、複製檔案到docker容器

```bash
docker cp /etc/letsencrypt/live/markweb.idv.tw/fullchain.pem e541646c602b:/etc/letsencrypt/live/markweb.idv.tw
```

* * *

## 1.8 、執行dockerfile產生image

```bash
docker build -t lamp/apachessl -f Dockerfile .
```

* * *

## 1.9 、執行docker


小提示 e541646c602b 為容器ID，請下docker ps指令查詢目前容器ID。


```bash
docker run -d -p 38000:80 -p 39000:443 e541646c602b apache2-foreground
```

* * *

## 1.10 、docker-compose.yaml範例

```yaml
version: "3"
services:
  database:
    image: linuxserver/mariadb:latest
    environment:
       - MYSQL_ROOT_PASSWORD=Mark_850409 
       - MYSQL_DATABASE=hedgedoc
       - MYSQL_USER=mark
       - MYSQL_PASSWORD=Mark_850409 
       - PGID=1000
       - PUID=1000
       - TZ=Aisa/Taipei
    volumes:
      - ./db/config:/config 
    restart: always
  codimd:
    image: hackmdio/hackmd:latest 
    environment:
      - CMD_DOMAIN=markweb.idv.tw:443
      #- CMD_HOST=markweb.idv.tw
      #- CMD_PORTS=443
      #- PUID=1000
      #- PGID=1000
      #- TW=Asia/Taipei
      - useSSL=true
      - CMD_ALLOW_ORIGIN=['markweb.idv.tw']
      #- CMD_URL_ADDPORT=true
      - CMD_PROTOCOL_USESSL=true
      - CMD_DB_URL=mysql://mark:Mark_850409@markweb.idv.tw:3306/hedgedoc
      - CMD_USECDN=false
      #- CMD_ALLOW_FREEURL=true
      - CMD_IMAGE_UPLOAD_TYPE=filesystem
      - CMD_HSTS_ENABLE=true
      - CMD_CSP_ENABLE=true
      - CMD_ALLOW_EMAIL_REGISTER=true
      - CMD_ALLOW_ANONYMOUS=true
      #- CMD_ALLOW_EMAIL_REGISTER=false
        #- UPLOADS_MODE=0755
      - NODE_ENV=development
      - CMD_GITHUB_CLIENTID=c50113630d0a20e45fbf
      - CMD_GITHUB_CLIENTSECRET=091cf518c0710082b301be14eb318c5110816503
    depends_on:
      - database
    ports:
      - "3001:3000"
    volumes:
      - ./volumes/uploads:/codimd/public/uploads
    restart: always
volumes:
  database-data: {}
  upload-data: {}
```