---
title: jupyter架設postfix來使用Gmail寄信
updated: 2024-07-21 05:25:55Z
created: 2023-08-04 08:26:29Z
tags:
  - python
  - jupytor
  - postfix
  - gmail
---


> [!note] 小提示
> 以下更多內容可參考此教學文章
> https://hackmd.io/@fourdollars/SkfnuPrhH

# 1 jupyter架設postfix來使用Gmail寄信

## 1.1 簡介
學習如何使用jupyter架設postfix來使用Gmail寄信

## 1.2 目錄

- [1 jupyter架設postfix來使用Gmail寄信](#1-jupyter架設postfix來使用gmail寄信)
  - [1.1 簡介](#11-簡介)
  - [1.2 目錄](#12-目錄)
    - [1.2.1 開啟終端機畫面](#121-開啟終端機畫面)
    - [1.2.2 首先安裝 下 postfix 與 mailutils](#122-首先安裝-下-postfix-與-mailutils)
    - [1.2.3 安裝後修改 /etc/postfix/main.cf 加入](#123-安裝後修改-etcpostfixmaincf-加入)
    - [1.2.4 修改 /etc/postfix/sasl\_passwd 加入密碼](#124-修改-etcpostfixsasl_passwd-加入密碼)
    - [1.2.5 使用 postmap 產生 db](#125-使用-postmap-產生-db)
    - [1.2.6 變更 /etc/postfix/sasl\_passwd\* 權限](#126-變更-etcpostfixsasl_passwd-權限)
    - [1.2.7 設定完成後重啟 postfix](#127-設定完成後重啟-postfix)
    - [1.2.8 最後寫 封信寄給自己看看有沒有成功收到](#128-最後寫-封信寄給自己看看有沒有成功收到)
    - [1.2.9 enjoy](#129-enjoy)
    - [1.2.10 若要查看錯誤訊息，輸入以下指令](#1210-若要查看錯誤訊息輸入以下指令)


### 1.2.1 開啟終端機畫面

![](https://markweb.idv.tw/uploads/upload_2039860c79149d217eb0f7dbdcde677c.png)

----

<!--more-->

### 1.2.2 首先安裝 下 postfix 與 mailutils

```bash
sudo apt install postfix mailutils
```

![](https://markweb.idv.tw/uploads/upload_f263584d0de4fc51f61b380dfad2df9d.png)

----

### 1.2.3 安裝後修改 /etc/postfix/main.cf 加入

```bash
relayhost = [smtp.gmail.com]:587
smtp_sasl_auth_enable = yes
smtp_sasl_password_maps = hash:/etc/postfix/sasl_passwd
smtp_sasl_security_options = noanonymous
smtp_tls_security_level = encrypt
```

![](https://markweb.idv.tw/uploads/upload_c89ab54ba46fd10b669fbdec49309523.png)

----

### 1.2.4 修改 /etc/postfix/sasl_passwd 加入密碼

<https://myaccount.google.com/apppasswords>

![](https://markweb.idv.tw/uploads/upload_a00f91d5415a091345f36cf9d9b8fd73.png)

![](https://markweb.idv.tw/uploads/upload_174a2fe739deb7fd7070887f781f04ca.png)

![](https://markweb.idv.tw/uploads/upload_5670b7df8de49727eb078174871ee469.png)

![](https://markweb.idv.tw/uploads/upload_367078340cd894ad9684ed218efdab7d.png)




```yaml
vim /etc/postfix/sasl_passwd
[smtp.gmail.com]:587 userid@gmail.com:password
```
![](https://markweb.idv.tw/uploads/upload_0c5404ae2e59e0fef42db4afa1e99eec.png)

----

### 1.2.5 使用 postmap 產生 db

```bash
 sudo postmap /etc/postfix/sasl_passwd
```

![](https://markweb.idv.tw/uploads/upload_827ebac7434ffb889df24380c6dc347c.png)

----

### 1.2.6 變更 /etc/postfix/sasl_passwd\* 權限

```bash
sudo chown root:root /etc/postfix/sasl_passwd*
sudo chmod 600 /etc/postfix/sasl_passwd*
```

![](https://markweb.idv.tw/uploads/upload_fba5343939ba6dd7e306dbf4e0e878c3.png)

----

### 1.2.7 設定完成後重啟 postfix

```bash
service postfix reload
```

![](https://markweb.idv.tw/uploads/upload_e6480032f4bac972d0ff47aa9a46cffa.png)

----

### 1.2.8 最後寫 封信寄給自己看看有沒有成功收到

```bash
echo "This is a test mail." | mail -s "test mail" userid@gmail.com
```

![](https://markweb.idv.tw/uploads/upload_4be9ca03d1d96e0352929deed629eb69.png)

----

### 1.2.9 enjoy

![](https://markweb.idv.tw/uploads/upload_4aa86d39a280f83a2e7c28cc95ac1eb4.png)

----

### 1.2.10 若要查看錯誤訊息，輸入以下指令

```bash
grep postfix /var/log/syslog
```

![](https://markweb.idv.tw/uploads/upload_a0a92ee7ab0a6d232958e9af62c71cff.png)