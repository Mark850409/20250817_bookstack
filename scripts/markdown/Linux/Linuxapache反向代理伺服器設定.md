---
title: Linuxapache反向代理伺服器設定
updated: 2024-07-23 13:31:02Z
created: 2023-08-04 08:26:29Z
tags:
  - Linux
  - reverse_proxy
---

# 1 Linuxapache反向代理伺服器設定

## 1.1 簡介
學習如何利用Linux apache設定反向代理

## 1.2 目錄

- [1 Linuxapache反向代理伺服器設定](#1-linuxapache反向代理伺服器設定)
  - [1.1 簡介](#11-簡介)
  - [1.2 目錄](#12-目錄)
    - [1.2.1 查看預設站台設定目錄](#121-查看預設站台設定目錄)
    - [1.2.2 建立 組自定義ports，假設是9098，重定向至5088](#122-建立-組自定義ports假設是9098重定向至5088)
    - [1.2.3 建立一組5088ports](#123-建立一組5088ports)
    - [1.2.4 開啟Proxy模組](#124-開啟proxy模組)
    - [1.2.5 進入/etc/apache2/ports.conf，將webserver要使用的ports開啟](#125-進入etcapache2portsconf將webserver要使用的ports開啟)
    - [1.2.6 檢查5088 ports是否在監聽狀態](#126-檢查5088-ports是否在監聽狀態)



Git server屬於服務，起9000 ports如何設定SSL?

切換到apache根目錄並查看

```bash
cd /etc/apache2
ll
```

![](https://markweb.idv.tw/uploads/upload_755d59e5d5a2cb6b7a878515d710c937.jpg)

<!--more-->

### 1.2.1 查看預設站台設定目錄

```bash
vim sites-available/000-default.conf
```

![](https://markweb.idv.tw/uploads/upload_09f5c63822f241795cbb22b65950d81f.jpg)

### 1.2.2 建立 組自定義ports，假設是9098，重定向至5088

```bash
<VirtualHost *:9098>
   #網域名稱要給，記得要帶ports
   ServerName markweb.idv.tw:9098
   #重定向至5088ports(SSL)
   Redirect permanent / https://markweb.idv.tw:5088/
</VirtualHost>
```

![](https://markweb.idv.tw/uploads/upload_5fcd660018ae74027c1abefa4c00217a.jpg)

### 1.2.3 建立一組5088ports

```bash
<VirtualHost *:5088>
    #網域名稱要給，記得要帶ports
    ServerName markweb.idv.tw:5088
    #SSLEngine要開
    SSLEngine on
    #SSL金鑰認證
    SSLCertificateFile /etc/letsencrypt/live/markweb.idv.tw/cert.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/markweb.idv.tw/privkey.pem
    SSLCertificateChainFile /etc/letsencrypt/live/markweb.idv.tw/chain.pem
    #代理伺服器設定
    ProxyPreserveHost On
    ProxyRequests Off
    #重點是這兩行(假設服務是開9090ports，那麼ports就帶9090)
    ProxyPass / http://markweb.idv.tw:9090/
    ProxyPassReverse / http://markweb.idv.tw:9090/
    Protocols h2 http/1.1
    Header always set Strict-Transport-Security "max-age=31536000; preload"
</VirtualHost>
```

![](https://markweb.idv.tw/uploads/upload_c7f179b8a7f3e6bc972e5e1905ba66af.jpg)

### 1.2.4 開啟Proxy模組

```bash
sudo a2enmod proxy proxy_http proxy_balancer lbmethod_byrequests
```

### 1.2.5 進入/etc/apache2/ports.conf，將webserver要使用的ports開啟

```bash
Listen 80
Listen 8088
Listen 9000
Listen 9088
Listen 9098
Listen 10108
<IfModule ssl_module>
        Listen 443
        Listen 4443
        Listen 4446
        Listen 5000
        Listen 5088
        Listen 6088
</IfModule>

<IfModule mod_gnutls.c>
        Listen 443
        Listen 4443
        Listen 4446
        Listen 5000
        Listen 5088
        Listen 6088
</IfModule>
```

![](https://markweb.idv.tw/uploads/upload_32622768699555a2c3c4fbe92476b913.jpg)

### 1.2.6 檢查5088 ports是否在監聽狀態

```bash
netstat -an|grep 5088
```

![](https://markweb.idv.tw/uploads/upload_1deea9318e8241f3bfde75b1f7663d4d.jpg)