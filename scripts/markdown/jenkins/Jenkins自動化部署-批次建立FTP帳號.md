---
title: Jenkins自動化部署-批次建立FTP帳號
updated: 2024-07-23 13:30:16Z
created: 2023-10-05 07:10:20Z
latitude: 24.8387226
longitude: 121.0177246
altitude: 0
tags:
  - Jenkins
  - FTP
  - Batch
---

# 1. Jenkins自動化部署-批次建立FTP帳號

還沒有安裝Jenkins? 請參照這篇[[Jenkins自動化部署-安裝教學]]

## 1.1.  簡介

`自動化建置`SFTP帳號，免去`人工建置`的困擾

## 1.2. 專案結構

```
├── .env
├── /.git/
├── autoBuildSFTP.sh
├── custom.html
├── docker-compose.yml
├── README.md
├── /SFTP/
│  ├── Dockerfile
│  ├── run_user.sh
│  └── user.txt
```
## 1.3. 目錄

- [1. Jenkins自動化部署-批次建立FTP帳號](#1-jenkins自動化部署-批次建立ftp帳號)
  - [1.1.  簡介](#11--簡介)
  - [1.2. 專案結構](#12-專案結構)
  - [1.3. 目錄](#13-目錄)
  - [1.4. 使用方式](#14-使用方式)
  - [1.5. 執行步驟](#15-執行步驟)
    - [1.5.1. 建立Gitea倉庫](#151-建立gitea倉庫)
    - [1.5.2. 開始撰寫腳本](#152-開始撰寫腳本)
    - [1.5.3. 使用Jenkins設計腳本流程](#153-使用jenkins設計腳本流程)
    - [1.5.4. 執行結果](#154-執行結果)


## 1.4. 使用方式
1. 安裝好`git`環境
2. 開啟`cmd`，輸入git clone `倉庫的URL`，拉取此專案到自己的主機
3. cd到此`專案資料夾`，執行`./autoBuildSFTP.sh`
4. 如果要使用`Jenkins`執行`CI/CD佈署`，請參考以下`執行步驟`

<!--more-->
## 1.5. 執行步驟

### 1.5.1. 建立Gitea倉庫

請到`gitea`建立 個新的倉庫

![image-20231005151331914](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/2JBf24cd078-image-20231005151331914.png)


點選設定→`Webhook`確認是否有和`Jenkins`綁定成功

![image-20231005151426424](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/2f04f268-image-20231005151426424.png)

### 1.5.2. 開始撰寫腳本

建立SFTP `DockerFile`，輸入以下指令
```docker
FROM atmoz/sftp
RUN apt update && apt install vim -y
COPY ./run_user.sh /etc/sftp/run_user.sh
COPY ./user.txt /etc/sftp/users.txt
```

建立`user.txt`，輸入以下內容

```
jason:jason:1002:1002:jason
joe:joe:1003:1003:joe
Bin:Bin:1004:1004:Bin
dean:dean:1005:1005:dean
sharon:sharon:1006:1006:sharon
```

建立`run_user.sh`，輸入以下指令
```bash
#!/bin/bash
FILENAME="users.txt"
sftpDir="/home"
cd /etc/sftp
while IFS=: read -r USERNAME PASSWORD UID GID directory || [ -n "$USERNAME" ];
do

if $(getent passwd ${USERNAME}) ;then
        userdel ${USERNAME}
        rm -rf /home/${USERNAME}
        echo "delete user from:" ${USERNAME}
else
        mkdir -p ${sftpDir}/${USERNAME}/uploads
        useradd -m -d /home/${USERNAME}/uploads ${USERNAME}
        echo "$USERNAME:$PASSWORD" | chpasswd
        echo "my passwd is:" $PASSWORD
        chmod -R 755 /home
        chown root:root /home/${USERNAME}
        chown ${USERNAME}:${USERNAME} /home/${USERNAME}/uploads
fi
done < "$FILENAME"
```

建立`autoBuildSFTP.sh`，輸入以下指令
```bash
#!/bin/bash
#+-------------------------------------腳本說明--------------------------------------------+
# 自動佈署SFTP腳本
# 使用方式: ./autoBuildSFTP.sh
#
# (C) 2023 - markhsu - licensed under markweb License v1.
# 
#+----------------------------------------------------------------------------------------+
date=$(date +%Y-%m-%d)
#+----------------------------------------------------------------------------------------+
#                                     先停用所有容器
#+----------------------------------------------------------------------------------------+
docker stop markweb_sftp 
docker stop markweb_sftp_apache	 
#+----------------------------------------------------------------------------------------+
#                                     移除所有容器
#+----------------------------------------------------------------------------------------+
docker rm markweb_sftp 
docker rm markweb_sftp_apache 
#+----------------------------------------------------------------------------------------+
#                                 要把SFTP的image移除，不然不會重新打包
#+----------------------------------------------------------------------------------------+
version_number=${BUILD_NUMBER}
version_number=$(($version_number-1))
docker rmi mysftp:${version_number}
BUILD_NUMBER=${BUILD_NUMBER} docker-compose up -d
#+----------------------------------------------------------------------------------------+
#                                 要給執行權限，否則permission_denied
#+----------------------------------------------------------------------------------------+
docker exec markweb_sftp bash -c 'chmod +x /etc/sftp/run_user.sh && sh /etc/sftp/run_user.sh'
docker exec markweb_sftp_apache bash -c "sed -i 's|/var/www/|/var/www/html|g' /etc/apache2/apache2.conf"
docker exec markweb_sftp_apache bash -c "sed -i '/<Directory \/var\/www\/html>/,/<\/Directory>/ s/AllowOverride None/AllowOverride all/' /etc/apache2/apache2.conf"

#+----------------------------------------------------------------------------------------+
#                                 上傳到個人私有倉庫
#+----------------------------------------------------------------------------------------+
docker login -u ${user} -p ${password} ${URL}
docker tag mysftp:${BUILD_NUMBER} ${URL}/jenkinsrepo/mysftp:${BUILD_NUMBER}
docker push ${URL}/jenkinsrepo/mysftp:${BUILD_NUMBER}
```

建立`docker-compose.yml`，輸入以下指令
```yaml
version: '3.3'
services:
 apache:
    image: markweb.idv.tw:29443/mydockerrepo/apache_local:1.0
    container_name: markweb_sftp_apache
    restart: always
    volumes:
        - ${APACHE_BIND_SOURCE}:/var/www/html
    ports:
      - ${APACHE_PORTS}:443
 sftp:
    build: ./SFTP
    container_name: markweb_sftp
    image: mysftp:${BUILD_NUMBER}
    restart: always
    volumes:
        - ${SFTP_UPLOAD}:/home
    cap_add:
        - SYS_ADMIN
    command: 
        - ${USER}:${PASSWORD}:1001:1001:${UPLOAD_FOLDER}
    ports:
        - ${SFTP_PORTS}:22

```

建立`.env，輸入以下指令
```
#APACHE參數設定
APACHE_PORTS=2223
APACHE_BIND_SOURCE=/home/markhsu/sftp
#SFTP參數設定
SFTP_PORTS=2224
SFTP_UPLOAD=/home/markhsu/sftp
BIND_SOURCE=/home/markhsu/sftp
USER=markhsu
PASSWORD=Mark_850409
UPLOAD_FOLDER=uploads
```

### 1.5.3. 使用Jenkins設計腳本流程

登入`Jenkins`，點選新增作業

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/LMCf7b8e279-upload-8ae9fb12cf730d58d6792b55cac5678a.png)

在原始碼管理，點選`Git`，輸入URL並選取憑證

![image-20231005153057942](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/1287c2b8-image-20231005153057942.png)


建置觸發程序，請將`GitHub hook trigger for GITScm polling`&`輪詢 SCM`打勾，排程設定為`每分鐘`執行 次

```bash
*/1 * * * * 
```

![image-20231005153131823](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/aWU5820dae8-image-20231005153131823.png)

建置環境，勾選在`「畫面輸出」`中加入時間戳記

![image-20231005153204356](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/ve034cc6be7-image-20231005153204356.png)

建置步驟，選擇`執行shell`，請輸入以下指令

```bash
chmod +X autoBuildSFTP.sh
sh autoBuildSFTP.sh
```

![image-20231005153247283](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/sdD7a81176a-image-20231005153247283.png)

建置後動作，選擇`附上建置紀錄`，如下圖

![image-20231005153316696](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/tVA5c7d7de3-image-20231005153316696.png)

### 1.5.4. 執行結果

![image-20231005153746306](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/3exf426300d-image-20231005153746306.png)

![image-20231005153925795](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/779ddd55-image-20231005153925795.png)

![image-20231005154005042](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/ceb5fe54-image-20231005154005042.png)

![image-20231005154113849](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/44079bc6-image-20231005154113849.png)
