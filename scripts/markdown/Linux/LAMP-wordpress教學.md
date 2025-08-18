---
title: LAMP-wordpress教學
updated: 2024-07-23 13:31:07Z
created: 2023-08-04 08:26:29Z
tags:
  - Linux
  - LAMP
  - Wordpress
---

# 1 LAMP-wordpress教學

## 1.1 簡介
學習如何利用LAMP架設wordpress

## 1.2 目錄

- [1 LAMP-wordpress教學](#1-lamp-wordpress教學)
  - [1.1 簡介](#11-簡介)
  - [1.2 目錄](#12-目錄)
    - [1.2.1 Apache2安裝教學](#121-apache2安裝教學)
    - [1.2.2 MYSQL安裝教學](#122-mysql安裝教學)
    - [1.2.3 安裝PHP](#123-安裝php)
    - [1.2.4 安裝PHPMYADMIN](#124-安裝phpmyadmin)
    - [1.2.5 Wordpress](#125-wordpress)


### 1.2.1 Apache2安裝教學

更新所有套件及版本

```bash
sudo apt update && sudo apt upgrade && sudo apt dist-upgrade
```

安裝apache2

```bash
sudo apt install apache2
```

檢查Apache是否正常運行：

```bash
sudo systemctl status apache2
```

接著要調整UFW防火牆設定以允許Apache進行遠端連線，以指令查看ufw application profile：

```bash
sudo ufw app list
```

執行下列指令以允許HTTP和HTTPS傳輸：

```bash
sudo ufw allow in "Apache Full"
```

<!--more-->

### 1.2.2 MYSQL安裝教學

* * *

安裝MYSQL

```bash
sudo apt install mysql-server
```

檢查MYSQL是否正常運行：

```bash
sudo systemctl status mysql
```

進入MYSQL prompt：

```bash
sudo mysql
```

查看目前所有用戶的驗證方式：

```mysql
SELECT user,authentication_string,plugin,host from mysql.user;
```

以指令更改：

```mysql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '[Your Password]';
```

再查看 次：

```mysql
SELECT user,authentication_string,plugin,host FROM mysql.user;
```

修改成功！現在離開MYSQL prompt，準備安裝PHP：

```bash
exit
```

### 1.2.3 安裝PHP

安裝PHP

```bash
sudo apt install php libapache2-mod-php php-mysql
```

Apache預設會優先查找名為index.html的檔案，若想將php檔案列為優先查找，則需去dir.conf中將index.php改至第 順位：

```bash
sudo vi /etc/apache2/mods-enabled/dir.conf
```

 樣需重啟Apache讓設定生效：

```bash
sudo systemctl restart apache2
```

接著要調整UFW防火牆設定以允許Apache進行遠端連線，以指令查看ufw application profile：

```bash
sudo ufw app list
```

執行下列指令以允許HTTP和HTTPS傳輸：

```bash
sudo ufw allow in "Apache Full"
```

### 1.2.4 安裝PHPMYADMIN

首先需啟用universe repository (預設為關閉)： ****

```bash
sudo add-apt-repository universe
```

接著下載安裝：

```bash
sudo apt install phpmyadmin php-mbstring php-gettext
```


> [!error] 小提示 
> 如果出現以下錯誤的話：
> E: Unable to locate package php-gettext
單獨安裝gettext就好，接著再執行 sudo apt install phpmyadmin php-mbstring php-gettext

```bash
sudo apt-get install gettext
```

```bash
sudo apt install phpmyadmin php-mbstring php-gettext
```

完成後會出現phpMyAdmin安裝選單，web server選擇 apache2，然後都選擇 OK，並設定兩次密碼完成安裝，接著啟用 mbstring module：

```bash
sudo phpenmod mbstring
```

安裝好後我們來創建新的使用者，phpMyAdmin預設已經有 root和 phpmyadmin這兩個使用者。首先以 root登入MYSQL：

```mysql
mysql -u root -p
```

創建新的使用者：

```mysql
CREATE USER '[Your Account]'@'localhost' IDENTIFIED BY '[Your Password]';
```

開通此帳號的權限：

```mysql
GRANT ALL PRIVILEGES ON *.* TO '[Your Account]'@'localhost' WITH GRANT OPTION;
```

結束離開：

```bash
exit
```

現在打開 http://\[ Your IP-Address\]/phpmyadmin並用剛才創建的新帳號登入phpMyAdmin：

![](https://markweb.idv.tw/uploads/upload_b1f8f7dc41088d8dc6815d873be2f966.png)

如果看不到PHPMyadmin，要記得在Apache2設定擋加入

SHIFT+G可以移動到vi編輯器最後 行

```bash
sudo vim /etc/apache2/apache2.conf
Include /etc/phpmyadmin/apache.conf
sudo /etc/init.d/apache2 restart
sudo systemctl restart apache2
```

### 1.2.5 Wordpress

接下來建立給WordPress的資料庫以及使用者

進入資料庫

```SQL
mysql -u root -p
```

建立資料庫

```SQL
CREATE DATABASE wordpress;
```

**建立 database 的帳戶：**

CREATE USER wordpressuser@localhost IDENTIFIED BY 'password';

建立使用者及權限

```SQL
CREATE USER 'wpuser'@'localhost' IDENTIFIED BY 'blahblah';
GRANT ALL PRIVILEGES ON wordpress.* TO 'wpuser'@'localhost';
```

刷新權限

```SQL
FLUSH PRIVILEGES;
```

安裝WordPress

先切換到網站目錄下，等等比較方便操作。

```bash
cd /var/www/html/
```

下載WordPress安裝最新版本(https://tw.wordpress.org/wordpress-latest-zh_TW.tar.gz)

> [!note] 小提示 
> 如何指定最新Wordpress版本呢?

1.  wordpress-latest-zh\_TW.tar.gz(要指定為latest，zh\_TW表示中文版本) 

```bash
sudo wget https://tw.wordpress.org/wordpress-latest-zh_TW.tar.gz
```

解壓縮檔案，會有 個wordpress目錄

```bash
sudo tar -xzvf latest.tar.gz
```

將檔案移置網站更目錄，記得要先切換到上 層

```bash
sudo mv /var/www/html/wordpress/* /var/www/html
```

將sample的設定檔複製 份並且更名(拿掉-sample)

```bash
sudo mv wp-config-sample.php wp-config.php
```

修改設定檔，將Database, user, password改成我們剛剛建立的

(用vi, nano都可以，這裡用nano)

```bash
sudo nano wp-config.php
```

最後，讓我們看看成果吧～

```bash
http://YOUR_IP/wordpress/wp-login.php
```