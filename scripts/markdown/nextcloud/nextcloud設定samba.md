---
title: nextcloud設定samba
updated: 2024-07-23 13:31:54Z
created: 2023-08-04 08:26:29Z
tags:
  - nextcloud
  - samba
---

# 1. nextcloud設定samba

## 1.1. 簡介
學習如何在nextcloud設定samba

## 1.2. 目錄

- [1. nextcloud設定samba](#1-nextcloud設定samba)
  - [1.1. 簡介](#11-簡介)
  - [1.2. 目錄](#12-目錄)
  - [1.3. 操作步驟](#13-操作步驟)
    - [1.3.1. 請至nextcloud確認外部儲存空間是否開啟](#131-請至nextcloud確認外部儲存空間是否開啟)
    - [1.3.2. 開啟後請確認是否安裝模組，若未安裝請按照以下步驟安裝](#132-開啟後請確認是否安裝模組若未安裝請按照以下步驟安裝)
    - [1.3.3. 進入nextcloud容器內，執行以下命令](#133-進入nextcloud容器內執行以下命令)
    - [1.3.4. 啟用smb模組，並重啟docker容器](#134-啟用smb模組並重啟docker容器)
    - [1.3.5. 進入nextcloud外部儲存空間設定，即不會再出現警告訊息](#135-進入nextcloud外部儲存空間設定即不會再出現警告訊息)
    - [1.3.6. 在nextcloud設定外部儲存空間，如下圖](#136-在nextcloud設定外部儲存空間如下圖)
    - [1.3.7. 回到所有檔案，即可看見目錄已成功被掛接](#137-回到所有檔案即可看見目錄已成功被掛接)
  - [1.4. 同場加映:如何安裝samba\&windows掛載遠端硬碟](#14-同場加映如何安裝sambawindows掛載遠端硬碟)
    - [1.4.1. 建立docker-compose.yml，並輸入以下指令](#141-建立docker-composeyml並輸入以下指令)
    - [1.4.2. 參數說明](#142-參數說明)
    - [1.4.3. 確認samba容器已啟動](#143-確認samba容器已啟動)
    - [1.4.4. 新增網路位置](#144-新增網路位置)
    - [1.4.5. 下一步設定連線](#145-下一步設定連線)
    - [1.4.6. 點選-設定連線](#146-點選-設定連線)
    - [1.4.7. 輸入分享位址，點選下一步](#147-輸入分享位址點選下一步)
    - [1.4.8. 點選下一步](#148-點選下一步)
    - [1.4.9. 完成](#149-完成)
    - [1.4.10. enjoy](#1410-enjoy)


## 1.3. 操作步驟

### 1.3.1. 請至nextcloud確認外部儲存空間是否開啟
![](https://markweb.idv.tw/uploads/upload_31a6b2fad14d63fca1c86de177aaeed0.png)


### 1.3.2. 開啟後請確認是否安裝模組，若未安裝請按照以下步驟安裝
![](https://markweb.idv.tw/uploads/upload_cbcfbb9dfe16a24dadaca0462c1729eb.png)


### 1.3.3. 進入nextcloud容器內，執行以下命令
```console=
apt update && apt install vim -y && apt-get install libsmbclient-dev -y && pecl install smbclient
```

![](https://markweb.idv.tw/uploads/upload_5246d1a9cfa2be4811e647795b5b4f02.png)

![](https://markweb.idv.tw/uploads/upload_33c975f338a978d9a8294a60c9882a82.png)

<!--more-->
### 1.3.4. 啟用smb模組，並重啟docker容器
```console=
echo "extension=smbclient.so" > /usr/local/etc/php/conf.d/docker-php-ext-smbclient.ini
```
![](https://markweb.idv.tw/uploads/upload_f80cf64b401dd6197634f746e10d22c6.png)

### 1.3.5. 進入nextcloud外部儲存空間設定，即不會再出現警告訊息

![](https://markweb.idv.tw/uploads/upload_3066e781ef8e2c1dc21fe5a98750b04d.png)

### 1.3.6. 在nextcloud設定外部儲存空間，如下圖
![](https://markweb.idv.tw/uploads/upload_16605995c793f8da17b6c677d52037ab.png)


### 1.3.7. 回到所有檔案，即可看見目錄已成功被掛接
![](https://markweb.idv.tw/uploads/upload_0d581411fcdea630bbac2786cc78b167.png)


## 1.4. 同場加映:如何安裝samba&windows掛載遠端硬碟

### 1.4.1. 建立docker-compose.yml，並輸入以下指令
```yaml
version: '3.7'
services:
  samba:
    image: dperson/samba
    environment:

      - WORKGROUP=WORKGROUP
      - USER=mark;mark
      - USERID=1000
      - GROUPID=1000
    networks:
      - default
    ports:
      - '137:137/udp'
      - '138:138/udp'
      - '139:139/tcp'
      - '445:445/tcp'
    read_only: true
    tmpfs:
      - /tmp
    restart: unless-stopped
    stdin_open: true
    tty: true
    volumes:
      - /media/markhsu/Data3/DockerProtainer/samba/mnt:/mnt

    command:
      -u "mark;mark"
      -s "share;/mnt/share;yes;no;yes;all"
      -s "photo;/mnt/photo;yes;no;yes;all"
      -s "nextcloud;/mnt/nextcloud;yes;no;yes;all"
      -p
volumes:
  samba:
```

### 1.4.2. 參數說明

```bash
  -s "<name;/path>[;browse;readonly;guest;users;admins;writelist;comment]"
                Configure a share
                required arg: "<name>;</path>"
                <name> is how it's called for clients
                <path> path to share
                NOTE: for the default value, just leave blank
                [browsable] default:'yes' or 'no'
                [readonly] default:'yes' or 'no'
                [guest] allowed default:'yes' or 'no'
                [users] allowed default:'all' or list of allowed users
                [admins] allowed default:'none' or list of admin users
                [writelist] list of users that can write to a RO share
[comment] description of share
```
               
### 1.4.3. 確認samba容器已啟動
![](https://markweb.idv.tw/uploads/upload_be7c60e257ed82df581450a17a87d55b.png)


### 1.4.4. 新增網路位置
![](https://markweb.idv.tw/uploads/upload_8d07baeb56118bc7e208c1aa7e11d9b3.png)


### 1.4.5. 下一步設定連線

![](https://markweb.idv.tw/uploads/upload_aefee8bd8a15cbde5df1ff18b3a95390.png)

### 1.4.6. 點選-設定連線
![](https://markweb.idv.tw/uploads/upload_2c6fb7025e6cb20ad52487e2991a5021.png)

### 1.4.7. 輸入分享位址，點選下一步
![](https://markweb.idv.tw/uploads/upload_c3ede91a2962ab784fa50a2da17452c7.png)

### 1.4.8. 點選下一步
![](https://markweb.idv.tw/uploads/upload_35ee3408948d488c55f3cf3258cac4da.png)

### 1.4.9. 完成
![](https://markweb.idv.tw/uploads/upload_6645191fb40ff92de6b11961c847d110.png)

### 1.4.10. enjoy
![](https://markweb.idv.tw/uploads/upload_18b9af4cbe8555c2fd411b19380fb263.png)








