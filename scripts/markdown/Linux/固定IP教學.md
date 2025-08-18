---
title: 固定IP教學
updated: 2024-07-23 13:30:28Z
created: 2023-08-04 08:26:29Z
tags:
  - Linux
  - IP
---

# 1 固定IP教學

## 1.1 簡介
學習如何利用LINUX進行固定IP設定

## 1.2 目錄

- [1 固定IP教學](#1-固定ip教學)
  - [1.1 簡介](#11-簡介)
  - [1.2 目錄](#12-目錄)
    - [1.2.1 編輯 /etc/netplan/00-installer-config.yaml](#121-編輯-etcnetplan00-installer-configyaml)
    - [1.2.2 設定檔內容編輯](#122-設定檔內容編輯)
    - [1.2.3 使用 sudo netplan apply 命令讓網路進行生效](#123-使用-sudo-netplan-apply-命令讓網路進行生效)


### 1.2.1 編輯 /etc/netplan/00-installer-config.yaml

```bash
sudo vim /etc/netplan/00-installer-config.yaml
```

<!--more-->

### 1.2.2 設定檔內容編輯

```yaml
network:
  version: 2
  ethernets:
    ens33: # 要設定的網卡名稱
      dhcp4: false
      addresses: [192.168.0.10/24] # 輸入要設定的 IP
      gateway4: 192.168.0.1 # 輸入 Gateway (大多數都是 .1)
      nameservers:
        addresses: [1.1.1.1,8.8.8.8]
```


> [!note] 小提示 
> 1.  網卡名稱不一定叫ens33，請進入虛擬機執行ifconfig or ip -a 查詢
>2.  gateway4請在windows cmd 執行 ipconfig 可以找到
>3.  addresses是設定DNS，至少要設定兩組比較好 

### 1.2.3 使用 sudo netplan apply 命令讓網路進行生效

```bash
sudo netplan apply
```

查看訊息後才知道在 Ubuntu 22.04 中原本的 gateway4 的將要被替換掉，雖然該警告訊息不會影響網路的使用，但是在設定的時候出現 串訊息還是不免會讓人害怕，為了要避免警告訊息的出現，我們需要修改 Gateway4，因為 22.04 已經替換為 route。

修改完成如下:

```yaml
# 2 This is the network config written by 'subiquity'
network:
  version: 2
  ethernets:
    ens33:
      dhcp4: false
      addresses: [192.168.0.50/24]
      routes:
      - to: default
        via: 192.168.0.1
      nameservers:
        addresses: [1.1.1.1,8.8.8.8]
```

再次使用命令讓新設定的 IP 生效。

```bash
sudo netplan apply
```

執行後就完全不會跳出警告訊息了