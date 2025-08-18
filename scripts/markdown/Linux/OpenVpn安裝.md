---
title: OpenVpn安裝
updated: 2024-07-23 13:30:31Z
created: 2023-08-04 08:26:29Z
tags:
  - Linux
  - OpenVPN
---

# 1 OpenVpn安裝

## 1.1 簡介
學習如何安裝OpenVpn

## 1.2 目錄

- [1 OpenVpn安裝](#1-openvpn安裝)
  - [1.1 簡介](#11-簡介)
  - [1.2 目錄](#12-目錄)
    - [1.2.1 更新套件及版本](#121-更新套件及版本)
    - [1.2.2 查詢IP位址](#122-查詢ip位址)
    - [1.2.3 下載與執行 ubuntu-22.04-lts-vpn-server.sh](#123-下載與執行-ubuntu-2204-lts-vpn-serversh)
    - [1.2.4 給予執行權限](#124-給予執行權限)
    - [1.2.5 切回上層目錄執行此腳本](#125-切回上層目錄執行此腳本)
    - [1.2.6 開始詢問 些問題，依照步驟設定即可](#126-開始詢問-些問題依照步驟設定即可)


> [!note] 小提示 
>  NAT 定要設定，不然會無法連線喔!!! 

### 1.2.1 更新套件及版本

```bash
sudo apt update && sudo apt upgrade
```

<!--more-->

### 1.2.2 查詢IP位址

```bash
ip a show eth0
```


> [!note] 小提示 
> 這邊是作為查詢內網IP，但實際上VPN設定時需要有一組對外IP

### 1.2.3 下載與執行 ubuntu-22.04-lts-vpn-server.sh

```bash
wget https://raw.githubusercontent.com/Nyr/openvpn-install/master/openvpn-install.sh -O ubuntu-22.04-lts-vpn-server.sh
```

### 1.2.4 給予執行權限

```bash
chmod -v +x ubuntu-22.04-lts-vpn-server.sh
```

### 1.2.5 切回上層目錄執行此腳本

```bash
sudo ./ubuntu-22.04-lts-vpn-server.sh
```

### 1.2.6 開始詢問 些問題，依照步驟設定即可

```bash
Tell me a name for the client.
The name must consist of alphanumeric character. It may also include an underscore or a dash.
Client name: androidphoneclient

Do you want to protect the configuration file with a password?
(e.g. encrypt the private key with a password)
   1) Add a passwordless client
   2) Use a password for the client
Select an option [1-2]: 2
⚠️ You will be asked for the client password below ⚠️

Note: using Easy-RSA configuration from: /etc/openvpn/easy-rsa/vars
Using SSL: openssl OpenSSL 3.0.2 15 Mar 2022 (Library: OpenSSL 3.0.2 15 Mar 2022)
Enter PEM pass phrase:VPN_CLIENT_PASSWORD_HERE
Verifying - Enter PEM pass phrase:VPN_CLIENT_PASSWORD_HERE
-----
Using configuration from /etc/openvpn/easy-rsa/pki/easy-rsa-6854.FKbbAQ/tmp.AL66it
Enter pass phrase for /etc/openvpn/easy-rsa/pki/private/ca.key:MY_PASS_PHRASE_HERE
Check that the request matches the signature
Signature ok
The Subject's Distinguished Name is as follows
commonName            :ASN.1 12:'androidphoneclient'
Certificate is to be certified until Aug  7 19:22:53 2024 GMT (825 days)

Write out database with 1 new entries
Data Base Updated

Client androidphoneclient added.

The configuration file has been written to /root/androidphoneclient.ovpn.
Download the .ovpn file and import it in your OpenVPN client.
```


> [!note] 小提示 
> * 停止服務
> sudo systemctl stop openvpn-server@server
>  * 啟動服務
> sudo systemctl start openvpn-server@server
> * 重啟服務
> sudo systemctl restart openvpn-server@server
> * 服務狀態
> sudo systemctl status openvpn-server@server