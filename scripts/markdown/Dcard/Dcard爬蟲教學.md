---
title: Dcard爬蟲教學
created: 2025-01-06 12:28:16Z
updated: 2025-01-06 20:21:59Z
tags:
  - Dcard
  - python
---
# 1. Dcard爬蟲教學

## 1.1. 簡介

用來爬取Dcard所有看版文章、文章搜尋爬取、留言爬取

<!--more-->
## 1.2. 目錄



## 1.3. 使用方式

請先安裝套件

```python
pip install -r requirement.txt
```

請先執行這個腳本，爬取`Dcrad`看板代號和名稱

```python
python dcard_type_spider.py
```

主程式：爬取文章標題、名稱、按讚數、留言數、分享數、摘要、時間
```python
python dcard_articles_spider.py
```


![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/VNTfb96dff8-202411121833001.png)


![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/Nvobdea337a-202411121834347.png)


![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/kwt011dc7fb-202411121834573.png)

主程式執行完畢會取得`dcard_articles.csv`，其中`article_link`是我們爬取文章留言需要的欄位

接著執行此程式爬取Dcard留言

```python
python dcard_comments_spider.py
```

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/xS5004e770f-202411121834541.png)
