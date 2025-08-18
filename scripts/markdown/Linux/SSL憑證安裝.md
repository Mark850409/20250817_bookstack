---
title: SSL憑證安裝
updated: 2024-07-23 13:30:57Z
created: 2023-08-04 08:26:29Z
tags:
  - Linux
  - SSL
---

# 1 SSL憑證安裝

## 1.1 簡介
學習如何安裝SSL憑證

## 1.2 目錄

- [1 SSL憑證安裝](#1-ssl憑證安裝)
  - [1.1 簡介](#11-簡介)
  - [1.2 目錄](#12-目錄)
    - [1.2.1 下載和安裝Certbot套件。](#121-下載和安裝certbot套件)
    - [1.2.2 設定Let's Encrypt憑證。](#122-設定lets-encrypt憑證)
    - [1.2.3 編輯Apache設定檔。](#123-編輯apache設定檔)


### 1.2.1 下載和安裝Certbot套件。

Step1：先將Debian/Ubuntu系統的套件資訊更新到最新。

```bash
sudo apt-get update -y
```

<!--more-->

Step2：安裝Certbot套件。

```bash
sudo apt-get install certbot python3-certbot-apache -y
```

Step3：編輯Apace設定檔，這邊的config檔路徑和名稱會跟大家不 樣，請自行設定你主機原有的config檔。以下指令筆者用Vim編輯器來編輯Vhost設定。

```bash
sudo vim /etc/apache2/sites-available/<apache-config>
```

Step4：Certbot工具需要能在Apache設定檔的『VirtualHost』區塊中辨識到『ServerName』與『ServerAlias』的域名和你要申請的憑證 樣，比如筆者要申請的憑證為『imkjie.com』和『www.imkjie.com』，那config會是如下：

```bash
Listen 80
<VirtualHost *:80>
    ##Certbot會看的設定如下『ServerName』和『ServerAlias』
    ServerName imkjie.com
    ServerAlias www.imkjie.com
    DocumentRoot /var/www/kjnotes

    # ...

</VirtualHost>
```

Step5：測試Apache設定檔，查看執行有沒有錯誤及重新載入Apache的config檔。

```bash
sudo apache2ctl configtest
```

如看到以下的訊息，則表示此次設定是正確的：

```bash
Syntax OK
```

重新載入Apache的config檔指令如下：

```bash
sudo systemctl reload apache2
```

### 1.2.2 設定Let's Encrypt憑證。

Step1：輸入以下指令來申請憑證，分別輸入你的電子郵件，同意Let's Encrypt相關的許可協議，及輸入要申請憑證的域名，域名的格式為『-d &lt;第 組域名&gt; -d &lt;第 組域名&gt; -d &lt;第 組域名&gt;』以此類推。

**下面是使用『certbot --nginx』方式取得憑證的指令，這指令可以讓Certbot工具協助設定Apache的config檔：

```bash
sudo certbot --apache --email email@example.com --agree-tos -d example.com -d www.example.com
```

**如果只需要申請憑證，那需加入『certonly』，指令為『certbot certonly --apache』，後面的部分需自己手動設定Apache的config檔；本文教學是使用下面這串指令：

```bash
sudo certbot certonly --apache --email email@example.com --agree-tos -d example.com -d www.example.com
```

Step2：申請過程會詢問 些問題，比如下面會詢問你是否需要收到Let's Encrypt組織相關的郵件，筆者這邊是選擇『n』。

```bash
demo@kjnotes:~$ sudo certbot certonly --apache --email email@example.com --agree-tos -d imkjie.com -d www.imkjie.com
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Plugins selected: Authenticator apache, Installer apache

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Would you be willing to share your email address with the Electronic Frontier
Foundation, a founding partner of the Let's Encrypt project and the non-profit
organization that develops Certbot? We'd like to send you email about our work
encrypting the web, EFF news, campaigns, and ways to support digital freedom.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
(Y)es/(N)o: n
```

Step3：憑證申請成功後，會出現『Congratulations!』的訊息，而申請成功的憑證會存放在『/etc/letsencrypt/live/example.com』目錄中。

```bash
sudo certbot certonly --nginx --email email@example.com --agree-tos -d example.com -d www.example.com --dry-run
```
### 1.2.3 編輯Apache設定檔。

Step1：編輯Apache設定檔，這邊的config檔路徑和名稱會跟大家不 樣，請自行設定你主機原有的config檔。以下指令筆者用Vim編輯器來設定自己的config檔。

```bash
sudo vim /etc/apache2/sites-available/<apache-config>
```

Step2：設定Apache HTTP自動轉址至HTTPS。

```bash
<VirtualHost *:80>
    ServerName example.com
    ServerAlias www.example.com
    Redirect permanent / https://example.com/
</VirtualHost>
```

Step3：配置申請好的SSL憑證。

```bash
<VirtualHost *:443>
    ServerName example.com
    ServerAlias www.example.com
    
    #HTTPS-有www轉址到沒有www
    <If "%{HTTP_HOST} == 'www.example.com'">
        Redirect permanent / https://example.com/
    </If>
    
    DocumentRoot /var/www/example
    
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/example.com/cert.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/example.com/privkey.pem
    SSLCertificateChainFile /etc/letsencrypt/live/example.com/chain.pem
    Protocols h2 http/1.1
    Header always set Strict-Transport-Security "max-age=31536000; preload"
    
    # ...
    
</VirtualHost>

SSLOpenSSLConfCmd Curves X25519:secp384r1
SSLSessionCache shmcb:/var/cache/mod_ssl/scache(512000)
SSLSessionCacheTimeout 300
SSLSessionTickets Off
SSLProtocol -all +TLSv1.2 +TLSv1.3
SSLCipherSuite TLS13-AES-256-GCM-SHA384:TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-128-CCM-8-SHA256:TLS13-AES-128-CCM-SHA256:EECDH+CHACHA20:EECDH+CHACHA20-draft:EECDH+ECDSA+AES128:EECDH+aRSA+AES128:RSA+AES128:EECDH+ECDSA+AES256:EECDH+aRSA+AES256:RSA+AES256:EECDH+ECDSA+3DES:EECDH+aRSA+3DES:RSA+3DES:!MD5;
SSLHonorCipherOrder on
SSLCompression off
SSLUseStapling on
SSLStaplingResponderTimeout 5
SSLStaplingReturnResponderErrors off
SSLStaplingCache shmcb:logs/ssl_stapling(128000)

# 2 ...
```

Step4：測試Apache設定檔，查看執行有沒有錯誤及重新載入Apache的config檔。

```bash
sudo apache2ctl configtest
```

Step5：若此主機的Apache伺服器未啟用過SSL服務，會看到『SSLEngine』和『Header』錯誤訊息，那須個別啟用以下的服務。

```bash
demo@kjnotes:~$ sudo apache2ctl configtest
AH00526: Syntax error on line XX of /etc/apache2/sites-enabled/example.conf:
Invalid command 'SSLEngine', perhaps misspelled or defined by a module not included in the server configuration
Action 'configtest' failed.
The Apache error log may have more information.
```

Step6：啟用headers、SSL模組。

```bash
sudo a2enmod ssl
sudo a2enmod headers
```

如能看到以下的訊息，則表示此次設定是正確的：

```bash
Syntax OK
```

重新載入Apache的config檔指令如下：

```bash
sudo systemctl reload apache2
```