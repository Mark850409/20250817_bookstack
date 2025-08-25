---
title: 如何使用BeautifulSoup進行爬蟲
updated: 2024-07-21 05:25:58Z
created: 2023-08-04 08:26:29Z
tags:
  - python
---

# 1. 如何使用BeautifulSoup進行爬蟲

## 1.1. 簡介
學習如何使用BeautifulSoup進行爬蟲

## 1.2. 目錄

- [1. 如何使用BeautifulSoup進行爬蟲](#1-如何使用beautifulsoup進行爬蟲)
  - [1.1. 簡介](#11-簡介)
  - [1.2. 目錄](#12-目錄)
  - [1.3. 爬蟲步驟](#13-爬蟲步驟)
    - [1.3.1. 請先安裝beautifulsoup4](#131-請先安裝beautifulsoup4)
    - [1.3.2. 接著安裝 pip install requests](#132-接著安裝-pip-install-requests)
    - [1.3.3. 開始爬蟲](#133-開始爬蟲)
    - [1.3.4. FAQ](#134-faq)

## 1.3. 爬蟲步驟


> [!note] 小提示
> 指令請在IDE的terminal輸入，或是使用powershell、CMD(以管理員身分執行皆可)


### 1.3.1. 請先安裝beautifulsoup4
```python
# 請在powershell或是IDE terminal執行喔
pip install beautifulsoup4
```
![](https://markweb.idv.tw/uploads/upload_6e4cd327a1d2d1804be51af65a7c120e.png)

<!--more-->

### 1.3.2. 接著安裝 pip install requests

```python
# 請在powershell或是IDE terminal執行喔
pip install requests
```

![](https://markweb.idv.tw/uploads/upload_d2c25509cc79e7fba98d3bb4b130a2de.png)


### 1.3.3. 開始爬蟲

```python
# 引入套件
from bs4 import BeautifulSoup
import requests
# 如果要換頁要加這 段迴圈
for page in range(1, 13):  
# 取得要爬蟲的HTML
    response = requests.get(
   "https://travel.ettoday.net/category/%E6%A1%83%E5%9C%92/")
    # 進行HTML FORMAT
    soup = BeautifulSoup(response.text, "html.parser")
     # 抓取圖片
    img = soup.select(".box_0 a img")
     # 印出目前抓到第幾頁
    print(f"====================第{str(page)}頁====================")
    # 取得所有頁面的圖片
    for imgs in img:
        print(imgs)
```

![](https://markweb.idv.tw/uploads/upload_4cb28da8761b3193670ff26275283423.png)


### 1.3.4. FAQ

> [!note] 小提示
> 如果出現(因為這個系統上已停用指令碼執行，所以無法載入…)
> https://israynotarray.com/other/20200510/1067127387/


![](https://markweb.idv.tw/uploads/upload_9894fa2c19e49318d99156711de7f06e.png)
