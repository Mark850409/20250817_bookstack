---
title: nextcloud安裝onlyoffice
updated: 2024-07-23 13:31:49Z
created: 2023-08-04 08:26:29Z
tags:
  - nextcloud
  - onlyoffice
---

# 1. nextcloud安裝onlyoffice

## 1.1. 簡介
學習如何在nextcloud安裝onlyoffice

## 1.2. 目錄

- [1. nextcloud安裝onlyoffice](#1-nextcloud安裝onlyoffice)
  - [1.1. 簡介](#11-簡介)
  - [1.2. 目錄](#12-目錄)
  - [1.3. 操作步驟](#13-操作步驟)
    - [1.3.1. 請另起 個服務，避免和nextcloud服務衝突](#131-請另起-個服務避免和nextcloud服務衝突)
    - [1.3.2. 請查看nextcloud apache設定檔路徑，並進入設定檔加入以下設定](#132-請查看nextcloud-apache設定檔路徑並進入設定檔加入以下設定)
    - [1.3.3. 打開瀏覽器，看到此畫面代表設定成功，輸入https://markweb.idv.tw:6443/](#133-打開瀏覽器看到此畫面代表設定成功輸入httpsmarkwebidvtw6443)
    - [1.3.4. 查詢隨機random的secret](#134-查詢隨機random的secret)
    - [1.3.5. 啟動文件伺服器](#135-啟動文件伺服器)
    - [1.3.6. 設定開機自動啟動文件伺服器](#136-設定開機自動啟動文件伺服器)
    - [1.3.7. 看到以下圖片表示設定成功](#137-看到以下圖片表示設定成功)
    - [1.3.8. 進入nextcloud查看，確認設定無誤](#138-進入nextcloud查看確認設定無誤)
    - [1.3.9. enjoy office](#139-enjoy-office)
  - [1.4. 同場加映，如何自動啟動onlyoffice](#14-同場加映如何自動啟動onlyoffice)
    - [1.4.1. 進入onlyoffice容器查看容器ID](#141-進入onlyoffice容器查看容器id)
    - [1.4.2. 確認要調整的內容，如下圖紅框處](#142-確認要調整的內容如下圖紅框處)
    - [1.4.3. 在本機目錄建立腳本](#143-在本機目錄建立腳本)
    - [1.4.4. 新增以下指令](#144-新增以下指令)
    - [1.4.5. 編輯vim /etc/crontab ，新增以下指令，並重啟CRONTAB服務](#145-編輯vim-etccrontab-新增以下指令並重啟crontab服務)


## 1.3. 操作步驟

### 1.3.1. 請另起 個服務，避免和nextcloud服務衝突
```bash
docker run -i -t -d -p <改成自己的ports>:80 --restart=always \
    -e JWT_ENABLED=true \
    -e JWT_SECRET=ni87bSds623nk932ds32342 \
    -e JWT_HEADER=Authorization \
    -e JWT_IN_BODY=true \
    -v /app/onlyoffice/DocumentServer/data:/var/www/onlyoffice/Data onlyoffice/documentserver
```
----
<!--more-->

### 1.3.2. 請查看nextcloud apache設定檔路徑，並進入設定檔加入以下設定
![](https://markweb.idv.tw/uploads/upload_4597608da5cd6b6f2410efb68a2d89c0.png)


```yaml
<VirtualHost *:443>
   ServerName markweb.idv.tw:443
   SSLEngine on
   SSLCertificateFile /etc/letsencrypt/live/markweb.idv.tw/cert.pem
   SSLCertificateKeyFile /etc/letsencrypt/live/markweb.idv.tw/privkey.pem
   SSLCertificateChainFile /etc/letsencrypt/live/markweb.idv.tw/chain.pem
   SSLProtocol all -SSLv2 -SSLv3
   SSLCipherSuite ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA:ECDHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA256:DHE-RSA-AES256-SHA:ECDHE-ECDSA-DES-CBC3-SHA:ECDHE-RSA-DES-CBC3-SHA:EDH-RSA-DES-CBC3-SHA:AES128-GCM-SHA256:AES256-GCM-SHA384:AES128-SHA256:AES256-SHA256:AES128-SHA:AES256-SHA:DES-CBC3-SHA:!DSS
   SSLHonorCipherOrder on
   SSLCompression off
   SetEnvIf Host "^(.*)$" THE_HOST=$1
   RequestHeader setifempty X-Forwarded-Proto https
   RequestHeader setifempty X-Forwarded-Host %{THE_HOST}e
   ProxyAddHeaders Off
   ProxyPassMatch (.*)(\/websocket)$ "ws://markweb.idv.tw:<更改為自己的ports>/$1$2"
   ProxyPass / http://markweb.idv.tw:<更改為自己的ports>/
   ProxyPassReverse / http://markweb.idv.tw:<更改為自己的ports>/
</VirtualHost>
```
----
### 1.3.3. 打開瀏覽器，看到此畫面代表設定成功，輸入https://markweb.idv.tw:6443/

![](https://markweb.idv.tw/uploads/upload_21eab1667b62ba276a6671d09419de0c.png)

----

### 1.3.4. 查詢隨機random的secret
```bash
 sudo docker exec 284180350e24 /var/www/onlyoffice/documentserver/npm/json -f /etc/onlyoffice/documentserver/local.json 'services.CoAuthoring.secret.session.string'
```
----
### 1.3.5. 啟動文件伺服器
```bash
sudo docker exec 284180350e24 sudo supervisorctl start ds:example
```
----
### 1.3.6. 設定開機自動啟動文件伺服器

```bash
sudo docker exec 284180350e24 sudo sed 's,autostart=false,autostart=true,' -i /etc/supervisor/conf.d/ds-example.conf
```
![](https://markweb.idv.tw/uploads/upload_42fce152bed8752ba273e434062ec417.png)



> [!note] 小提示
> 1. Error when trying to connect (Error occurred in the document service: Error while downloading the document file to be converted.) (version 7.2.1.34)
>* 這兩個設定檔的設定務必要一致，否則會連線失敗
>* 請檢查office服務是否設為開機自動啟動，否則會出現502 error
>* https://forum.onlyoffice.com/t/error-when-trying-to-connect-error-occurred-in-the-document-service-error-while-downloading-the-document-file-to-be-converted-version-7-2-1-34/3356
>* https://help.nextcloud.com/t/onlyoffice-secret-key-issue/56464/12
>* 檢查紅框處，/var/www/nextcloud/config/config.php設定



![](https://markweb.idv.tw/uploads/upload_776f9d6abf0076de94b3f7b08e616555.png)

* 檢查紅框處，/etc/onlyoffice/documentserver/local.json
![](https://markweb.idv.tw/uploads/upload_d9d884ef20bedea11532b8ca5facc7a6.png)


### 1.3.7. 看到以下圖片表示設定成功
![](https://markweb.idv.tw/uploads/upload_0a27621e4b8f77b222e869c0b5208b08.png)


### 1.3.8. 進入nextcloud查看，確認設定無誤

![](https://markweb.idv.tw/uploads/upload_76737d0c407770b1d4d4399c853ad934.png)

### 1.3.9. enjoy office

![](https://markweb.idv.tw/uploads/upload_56ca783e8148112f74096de87ca1711d.png)

![](https://markweb.idv.tw/uploads/upload_59a705288a190a55be008b300de4ef78.png)

![](https://markweb.idv.tw/uploads/upload_bbda2833558920504c2c0ab8df75dc46.png)

![](https://markweb.idv.tw/uploads/upload_f9d370742fdb422ddfc36bc72d8be230.png)

![](https://markweb.idv.tw/uploads/upload_2576b45c90df64ebccb5a8cfb8de8f43.png)


## 1.4. 同場加映，如何自動啟動onlyoffice

### 1.4.1. 進入onlyoffice容器查看容器ID
![](https://markweb.idv.tw/uploads/upload_3c72f229b461a83fa7c2123a4c8f0d47.png)

### 1.4.2. 確認要調整的內容，如下圖紅框處
![](https://markweb.idv.tw/uploads/upload_00c320f05b187cd61738791425558127.png)


### 1.4.3. 在本機目錄建立腳本

![](https://markweb.idv.tw/uploads/upload_48c31e1989fb76aae983c3470148ce4a.png)

### 1.4.4. 新增以下指令
```bash
docker exec 284180350e24 sudo sed -i '21c "header": "AuthorizeJwt",' /etc/onlyoffice/documentserver/local.json
docker exec 284180350e24 sudo sed -i '22c "inBody": false' /etc/onlyoffice/documentserver/local.json
docker exec 284180350e24 sudo sed -i '25c "header": "AuthorizeJwt",' /etc/onlyoffice/documentserver/local.json
docker exec 284180350e24 sudo sed -i '26c "inBody": false' /etc/onlyoffice/documentserver/local.json
docker exec 284180350e24 sudo supervisorctl restart all
```
![](https://markweb.idv.tw/uploads/upload_461093926729c7cde9da01c41ebb2eaa.png)

### 1.4.5. 編輯vim /etc/crontab ，新增以下指令，並重啟CRONTAB服務

```bash
@reboot root sh /home/markhsu/autostartoffice.sh
```
![](https://markweb.idv.tw/uploads/upload_1b9cb4341548aaf9fce339a901b04e4b.png)