---
title: Ubuntu上架SVN-Apache與權限設定
updated: 2024-07-23 13:30:45Z
created: 2023-08-04 08:26:29Z
tags:
  - Linux
  - SVN
  - Server
  - Access
  - Apache
---

# 1 Ubuntu上架SVN-Apache與權限設定


## 1.1 簡介
學習如何設定SVN-Apache的權限

## 1.2 目錄

- [1 Ubuntu上架SVN-Apache與權限設定](#1-ubuntu上架svn-apache與權限設定)
  - [1.1 簡介](#11-簡介)
  - [1.2 目錄](#12-目錄)
  - [1.3 安裝SVN](#13-安裝svn)
    - [1.3.1 搭配APACHE架設](#131-搭配apache架設)
    - [1.3.2 STANDALONE 架設](#132-standalone-架設)

## 1.3 安裝SVN

```bash
sudo apt-get install subversion
```

<!--more-->

### 1.3.1 搭配APACHE架設

Step1：因為authentication與authorization我打算也讓apache負責，所以要再額外安裝相關的模組

```bash
sudo apt-get install libapache2-mod-svn libapache2-svn libsvn-dev
```

Step2：裝好後啟用剛剛裝的模組，然後重啟apache

```bash
sudo a2enmod dav
sudo a2enmod dav_svn
sudo a2enmod authz_svn
sudo service apache2 restart
```

Step3：新增 個使用者帳號

```bash
htpasswd -c /etc/apache2/dav_svn.passwd joe
```

Step4：創建 個新的專案 myrepo並給予權限

```bash
mkdir -p /var/www/svn
svnadmin create /var/www/svn/myrepo
chown -R www-data:www-data /var/www/svn
```

Step5：編輯 /etc/apache2/sites-enabled/000-default.conf，在 後面加入下面內容

```bash
<Location />
DAV svn
SVNParentPath /var/www/svn
AuthType Basic
AuthName "Subversion Repository"
AuthUserFile /etc/apache2/dav_svn.passwd
Require valid-user
</Location>
```

Step6：最後，啟用 DAV SVN 並重新啟動 Apache

```bash
a2enmod dav_svn
apachectl restart
```

### 1.3.2 STANDALONE 架設

Step1：首先安裝 Subversion

```bash
sudo apt-get install subversion
```

Step2：接著創建 個空白專案

```bash
mkdir ~/svnrepo
svnadmin create ~/svnrepo/myprj
```

Step3：修改 ~/svnrepo/myprj/conf/passwd 來新增帳號

![](https://markweb.idv.tw/uploads/upload_afbbecabb7bec4722784d3d94d2af6df.png)


Step4：接著編輯 ~/svnrepo/myprj/conf/svnserve.conf 修改設定，找到 / 修改下列3個項目，前且移除前面的 "#"，使其生效

```bash
anon-access = none
auth-access = write
password-db = passwd
```

Step5：最後，啟動 SVN Daemon

```bash
svnserve -d --listen-port 12345 -r ~/svnrepo/
```