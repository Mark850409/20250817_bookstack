---
title: 安裝DockerPortainer
updated: 2024-07-23 13:28:03Z
created: 2023-08-04 08:26:29Z
tags:
  - Docker
---

# 1 安裝DockerPortainer

還沒有安裝Docker? 請參照這篇[[[安裝Docker]]](app://obsidian.md/%E5%AE%89%E8%A3%9DDocker)

## 1.1 簡介
學習如何建立DockerPortainer環境

## 1.2 目錄

- [1 安裝DockerPortainer](#1-安裝dockerportainer)
  - [1.1 簡介](#11-簡介)
  - [1.2 目錄](#12-目錄)
    - [1.2.1 請輸入以下指令](#121-請輸入以下指令)
    - [1.2.2  確認container是否將portainer服務up](#122--確認container是否將portainer服務up)
    - [1.2.3 進入portainer](#123-進入portainer)



### 1.2.1 請輸入以下指令

> [!note] 小提示
>- -p 指令ports(先確認是否會和其他ports衝突)
>- --name container名稱
>- -v 指令volume，如果希望此容器有憑證請在這邊將金鑰的位置掛上去
>- 6053537/portainer-ce:latest 中文版的image


```yaml 
docker run -d -p 9443:9443 -p 8000:8000 \
    --name markwebportainer --restart always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /media/markhsu/Data3/DockerProtainer/portainer-data:/data \
    -v /etc/letsencrypt/live/markweb.idv.tw:/certs/live/markweb.idv.tw:ro \
    -v /etc/letsencrypt/archive/markweb.idv.tw:/certs/archive/markweb.idv.tw:ro \
    6053537/portainer-ce:latest \
    --sslcert /certs/live/markweb.idv.tw/fullchain.pem \
    --sslkey /certs/live/markweb.idv.tw/privkey.pem

```

* * *
<!--more-->

### 1.2.2  確認container是否將portainer服務up

```bash
docker ps
```

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/cEx7427749c-upload-96a75584b411956cd6a18dece7683641.png)

* * *

### 1.2.3 進入portainer

- 第一次登入請先註冊

![](https://markweb.idv.tw/uploads/upload_21441498201422570df0ae3effd35fff.png)

- 恭喜您，已可開始使用!!!

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/KPof02f430d-upload-7cb8c2de1b7c8a6690397d0e8267ed57.png)