---
title: giteaWebServer架設
updated: 2024-07-23 13:30:24Z
created: 2023-08-04 08:26:29Z
tags:
  - Linux
  - Gitea
  - Server
---

# 1. 1 giteaWebServer架設

## 1.1. 簡介
學習如何架設giteaWebServer

## 1.2. 目錄
- [1. 1 giteaWebServer架設](#1-1-giteawebserver架設)
  - [1.1. 簡介](#11-簡介)
  - [1.2. 目錄](#12-目錄)
  - [1.3. 操作步驟](#13-操作步驟)
    - [1.3.1. 安裝git](#131-安裝git)
    - [1.3.2. 建立資料庫](#132-建立資料庫)
    - [1.3.3. 安裝gitea](#133-安裝gitea)
    - [1.3.4. 加入執行權限](#134-加入執行權限)
    - [1.3.5. 查看版本](#135-查看版本)
    - [1.3.6. 加入新的user](#136-加入新的user)
    - [1.3.7. 加入git的專案目錄](#137-加入git的專案目錄)
    - [1.3.8. 賦予權限](#138-賦予權限)
    - [1.3.9. 加入git的設定檔目錄](#139-加入git的設定檔目錄)
    - [1.3.10. 加入gitea.service](#1310-加入giteaservice)
    - [1.3.11. 啟動Gitea](#1311-啟動gitea)
    - [1.3.12. 查看Gitea狀態](#1312-查看gitea狀態)
    - [1.3.13. 開機自動啟動Gitea](#1313-開機自動啟動gitea)
    - [1.3.14. 成功畫面](#1314-成功畫面)

## 1.3. 操作步驟
### 1.3.1. 安裝git

```bash
sudo apt install git
```

<!--more-->

### 1.3.2. 建立資料庫

```sql
# 2 進入mysql
mysql -u root -p
```

```sql
--建立user帳號及密碼
CREATE USER 'gitea'@'localhost' IDENTIFIED BY 'Mark_850409';
--賦予權限
GRANT ALL PRIVILEGES ON *.* TO 'gitea'@'localhost' WITH GRANT OPTION;
--更新權限
FLUSH PRIVILEGES;
--離開mysql
QUIT;
```

### 1.3.3. 安裝gitea

> [!note] 小提示 
>  可從這個網站尋找最新版，把版號記錄下來https://dl.gitea.com/gitea/

```bash
sudo wget -O /usr/local/bin/gitea https://dl.gitea.io/gitea/1.19.0/
gitea-1.19.0-linux-amd64
```

### 1.3.4. 加入執行權限

```bash
sudo chmod +x /usr/local/bin/gitea
```

### 1.3.5. 查看版本

```bash
gitea --version
```

### 1.3.6. 加入新的user

```bash
sudo adduser --system --shell /bin/bash --gecos 'Git Version Control'
 --group --disabled-password --home /home/git git
```

### 1.3.7. 加入git的專案目錄

```bash
sudo mkdir -pv /var/lib/gitea/{custom,data,log}
```

### 1.3.8. 賦予權限

```bash
sudo chown -Rv git:git /var/lib/gitea
sudo chmod -Rv 750 /var/lib/gitea
```

### 1.3.9. 加入git的設定檔目錄

```bash
sudo mkdir -v /etc/gitea
sudo chown -Rv root:git /etc/gitea
sudo chmod -Rv 770 /etc/gitea
```

### 1.3.10. 加入gitea.service

```bash
sudo nano /etc/systemd/system/gitea.service
```

```bash
[Unit]
Description=Gitea
After=syslog.target
After=network.target

RestartSec=3s
Type=simple
User=git
Group=git
WorkingDirectory=/var/lib/gitea/

ExecStart=/usr/local/bin/gitea web --config /etc/gitea/app.ini
Restart=always
Environment=USER=git HOME=/home/git GITEA_WORK_DIR=/var/lib/gitea

[Install]
WantedBy=multi-user.target
```

### 1.3.11. 啟動Gitea

```bash
sudo systemctl start gitea
```

### 1.3.12. 查看Gitea狀態

```bash
sudo systemctl status gitea
```

### 1.3.13. 開機自動啟動Gitea

```bash
sudo systemctl enable gitea
```

### 1.3.14. 成功畫面

![](https://markweb.idv.tw/uploads/upload_2fec87493fa31620d2ccb3ce9a6c1e6a.png)