---
title: UFW防火牆設定
updated: 2024-07-23 13:30:41Z
created: 2023-08-04 08:26:29Z
tags:
  - Linux
  - UFW
---

# 1 UFW 防火牆設定

## 1.1 簡介
學習如何設定防火牆

## 1.2 目錄

- [1 UFW 防火牆設定](#1-ufw-防火牆設定)
  - [1.1 簡介](#11-簡介)
  - [1.2 目錄](#12-目錄)
    - [1.2.1 **啟用防火牆**](#121-啟用防火牆)
    - [1.2.2 允許或拒絕連線指定 port](#122-允許或拒絕連線指定-port)
    - [1.2.3 **允許或拒絕特定 IP 連線指定 port**](#123-允許或拒絕特定-ip-連線指定-port)
    - [1.2.4 設定指定 subnet 可以允許或禁止連線指定 port](#124-設定指定-subnet-可以允許或禁止連線指定-port)
    - [1.2.5 設定指定網路介面 (Network Interface) 連線指定 port](#125-設定指定網路介面-network-interface-連線指定-port)
    - [1.2.6 刪除已經建立的規則](#126-刪除已經建立的規則)


### 1.2.1 **啟用防火牆**

可以輸入指令檢查 ufw 是否為啟用狀態，在 ubuntu 伺服器預設是沒有啟用的狀態 `Status: inactive`

```bash
sudo ufw status verbose
```

在啟用前我們要先設定允許 ssh port (22) 可以連線，不然之後會無法 從外部 ssh 連到機器更改東西

```bash
sudo ufw allow 22
```

擋下全部其他 port 的連線，並允許機器能夠連到外面的網路

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

接著啟動 ufw

```bash
sudo ufw enable
```

當 ufw 啟動之後就能看到詳細的防火牆規則了

```bash
sudo ufw status verbose
```

```bash
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), disabled (routed)
New profiles: skip
To                         Action      From
--                         ------      ----
22                         ALLOW IN    Anywhere
22 (v6)                    ALLOW IN    Anywhere (v6)
```

<!--more-->

### 1.2.2 允許或拒絕連線指定 port

如果要允許連線指定 port 可以輸入指令：

```bash
sudo ufw allow <port-number>
sudo ufw deny <port-number>
```

例如：假如要放網站能夠透過外部連線，可以輸入以下指令

```bash
sudo ufw allow 80
sudo ufw allow 443
```

### 1.2.3 **允許或拒絕特定 IP 連線指定 port**

而假如是只允許特定 IP 才能連線的話，可以輸入以下指令

```bash
sudo ufw allow from <IP> to any port <port-number>
sudo ufw deny from <IP> to any port <port-number>
```

例如允許 `159.66.109.6` 連線 80 port

```bash
sudo ufw allow from 159.66.109.6 to any port 80
```

### 1.2.4 設定指定 subnet 可以允許或禁止連線指定 port

有時會設定需要允許子網路可以連線到，可以輸入以下指令

```bash
sudo ufw allow from <IP-with-mask> to any port <port-number>
sudo ufw deny from <IP-with-mask> to any port <port-number>
```

例如允許要允許 `159.66.109.0` ~ `159.66.109.254` 能夠連線 22 port

```bash
sudo ufw allow from 159.66.109.0/24 to any port 22
```

### 1.2.5 設定指定網路介面 (Network Interface) 連線指定 port

而如果不是想針對 IP 來設定連線，而是想針對網路介面進行設定的話，首先可以輸入查目前有哪些網路介面

```bash
ip addr
```

並且設定該網路介面能否允許連線至指定port

```bash
sudo ufw allow in on <network-interface-name> to any port <port-number>
```

例如允許介面 eth0 可以連線 80 port

```bash
sudo ufw allow in on eth0 to any port 80
```

### 1.2.6 刪除已經建立的規則

如果要刪除已經建立的防火牆規則，要先查看規則所對應的編號

```bash
sudo ufw status numbered
```

```bash
Status: active
     To                         Action      From
     --                         ------      ----
[ 1] 22                         ALLOW IN    Anywhere
[ 2] 80                         ALLOW IN    Anywhere
[ 3] 443                        ALLOW IN    Anywhere
[ 4] 22 (v6)                    ALLOW IN    Anywhere (v6)
[ 5] 80 (v6)                    ALLOW IN    Anywhere (v6)
[ 6] 443 (v6)                   ALLOW IN    Anywhere (v6)
```

知道指定編號可以輸入以下指令來刪除規則：

```bash
sudo ufw delete <rule-number>
```

例如：要刪除 IPv4 的 80 port 連線

```bash
sudo ufw delete 2
```

```bash
Deleting:
 allow 80
 Proceed with operation (y|n)? y
 Rule deleted
```