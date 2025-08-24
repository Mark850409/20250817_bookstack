---
title: 安裝DockerSSL
updated: 2024-07-23 13:28:13Z
created: 2023-08-04 08:26:29Z
tags:
  - Docker
  - SSL
---

# 1 安裝DockerSSL

還沒有安裝Docker? 請參照這篇[[[安裝Docker]]](app://obsidian.md/%E5%AE%89%E8%A3%9DDocker)

## 1.1 簡介
學習如何建立DockerSSL環境

## 1.2 目錄
- [1 安裝DockerSSL](#1-安裝dockerssl)
  - [1.1 簡介](#11-簡介)
  - [1.2 目錄](#12-目錄)
    - [1.2.1 撰寫yaml](#121-撰寫yaml)
    - [1.2.2 點選佈署](#122-點選佈署)
    - [1.2.3 進入容器查看主機儲存卷](#123-進入容器查看主機儲存卷)
    - [1.2.4 編輯000-default.conf，輸入以下內容](#124-編輯000-defaultconf輸入以下內容)
    - [1.2.5 編輯ports.conf，輸入以下內容](#125-編輯portsconf輸入以下內容)
    - [1.2.6 編輯apache2.conf，在開頭輸入以下內容](#126-編輯apache2conf在開頭輸入以下內容)
    - [1.2.7 確認容器內是否有金鑰檔](#127-確認容器內是否有金鑰檔)
    - [1.2.8 重啟container，讓設定生效](#128-重啟container讓設定生效)
    - [1.2.9 看到此畫面表示設定成功](#129-看到此畫面表示設定成功)
    - [1.2.10 查看憑證資訊](#1210-查看憑證資訊)


### 1.2.1 撰寫yaml

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/7dcfab77-upload-aca249dcf820a03a03d61788198b73db.png)


```yaml
version: '3.9'

services:
  apache:
    image: php:7.4-apache
    container_name: apachetest
    restart: always
    ports:
      - 22443:22443
    volumes:
      - /media/markhsu/Data3/DockerProtainer/apachetest/etc/apache2/:/etc/apache2/
      - /media/markhsu/Data3/DockerProtainer/apachetest/etc/letsencrypt/live/markweb.idv.tw:/etc/letsencrypt/live/markweb.idv.tw
```

> [!note] 小提示 
> 1.  /etc/apache2目錄 定要掛接，且目錄的內容可以先在伺服器安裝apache2後，將整個目錄複製 份到docker容器內，在進行設定。
> 2.  /etc/letsencrypt/live/markweb.idv.tw目錄 定要掛接，內容可以先在伺服器產好憑證後，將整個目錄複製 份到docker容器內，在進行設定。

<!--more-->

### 1.2.2 點選佈署

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/puPfa8a6961-upload-6f876ab65bf9e46566e692d2691ae3fa.png)

* * *

### 1.2.3 進入容器查看主機儲存卷

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/i6Ee7d5d976-upload-93956c4e7bc4dce14e04236d9a681a69.png)

* * *

### 1.2.4 編輯000-default.conf，輸入以下內容

```yaml
<VirtualHost *:22443>
    ServerName markweb.idv.tw:22443
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/markweb.idv.tw/cert.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/markweb.idv.tw/privkey.pem
    SSLCertificateChainFile /etc/letsencrypt/live/markweb.idv.tw/chain.pem
   # ProxyPreserveHost On
   # ProxyRequests Off
   # ProxyPass / http://markweb.idv.tw:9090/
   # ProxyPassReverse / http://markweb.idv.tw:9090/
   # AllowEncodedSlashes NoDecode
   # Protocols h2 http/1.1
   # Header always set Strict-Transport-Security "max-age=31536000; preload"
</VirtualHost>
```

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/dsUcb95b011-upload-d7bf30a0ec1c12a5bda17e1e0ee94bdb.png)

* * *

### 1.2.5 編輯ports.conf，輸入以下內容

```yaml
Listen 80

<IfModule ssl_module>
        Listen 443
        Listen 22443
</IfModule>

<IfModule mod_gnutls.c>
        Listen 443
        Listen 22443
</IfModule>
```

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/Aqo80275336-upload-1138f792ca692686897eccc797cb0a0e.png)

* * *

### 1.2.6 編輯apache2.conf，在開頭輸入以下內容

```bash
LoadModule ssl_module /usr/lib/apache2/modules/mod_ssl.so
```

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/PnL3980ca08-upload-38423d7789e53ca871157fb70b779c07.png)


> [!note] 小提示 
> 此行 定要加在apache2.conf，否則容器會找不到ssl模組，導致無法正常執行 LoadModule ssl\_module /usr/lib/apache2/modules/mod\_ssl.so

### 1.2.7 確認容器內是否有金鑰檔

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/7Wn9f391fc2-upload-341588ace47533026a4176b22d1792d5.png)

* * *

### 1.2.8 重啟container，讓設定生效

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/6bd1c7d2-upload-a11f10ac38b0cfe8da0755ba3df26426.png)

* * *

### 1.2.9 看到此畫面表示設定成功

![](https://markweb.idv.tw/uploads/upload_eca3b771efd3d03261c3cf62f797e7c2.png)

* * *

### 1.2.10 查看憑證資訊

> [!note] 小提示 
> 可點選鎖頭查看憑證資訊

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/0be2f62e-upload-09fdac17273a31b165d42ad26675b1a9.png)