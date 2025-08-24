---
title: redmine中整合git版本庫
updated: 2024-07-23 13:32:10Z
created: 2023-09-17 12:14:50Z
latitude: 24.8387226
longitude: 121.0177246
altitude: 0
tags:
  - Redmine
  - Gitlab
---

# 1 redmine中整合git版本庫

## 1.1 簡介
學習如何透過redmine中整合git版本庫

## 1.2 目錄

- [1 redmine中整合git版本庫](#1-redmine中整合git版本庫)
  - [1.1 簡介](#11-簡介)
  - [1.2 目錄](#12-目錄)
    - [1.2.1 事前準備](#121-事前準備)
    - [1.2.2 設定redmine儲存機制\&建立關鍵字進行事件觸發](#122-設定redmine儲存機制建立關鍵字進行事件觸發)
    - [1.2.3 透過Jenkins進行事件觸發\&撰寫自動更新腳本](#123-透過jenkins進行事件觸發撰寫自動更新腳本)

### 1.2.1 事前準備

請先建立好gitea倉庫

![image-20230917201642307](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/J6c47501508-image-20230917201642307.png)

在redmine開 個新issue

![image-20230917202010429](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/8KH302d5927-image-20230917202010429.png)

<!--more-->

### 1.2.2 設定redmine儲存機制&建立關鍵字進行事件觸發

設定→儲存機制→建立新儲存機制
![image-20230917202220585](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/1a477a34-image-20230917202220585.png)


按照圖片進行相關設定
![image-20230917202515300](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/1dd40f53-image-20230917202515300.png)

### 1.2.3 透過Jenkins進行事件觸發&撰寫自動更新腳本

設定GIT_URL
![image-20230917202711770](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/s0Te6a7d08d-image-20230917202711770.png)


設定PROJECT
![image-20230917202800333](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/6efa47df-image-20230917202800333.png)


綁定GIT
![image-20230917202848539](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/UNJe381803a-image-20230917202848539.png)


設定每分鐘觸發 次事件
![image-20230917203014533](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/4t928d5974f-image-20230917203014533.png)

撰寫腳本

```bash
#!/bin/bash
#+-------------------------------------腳本說明--------------------------------------------+
# Redmine自動更新腳本
# 使用方式: ./autoSyncRedminegit.sh
#
# (C) 2023 - markhsu - licensed under markweb License v1.
#
#+----------------------------------------------------------------------------------------+
#                                    每分鐘同步一次 repos, 依照需求自行增加
#+----------------------------------------------------------------------------------------+
docker exec redmine bash -c "if [ -d "/data/redmine/repos/${PROJECT}" ]; then cd /data/redmine/repos/'${PROJECT}' && git fetch --all; else git clone --mirror ${GIT_URL} && cd /data/redmine/repos/'${PROJECT}' && git fetch --all ; fi"
```

![image-20230917203054726](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/SIR05294aa7-image-20230917203054726.png)

建置後不論成功或失敗都要寄信

![image-20230917203146001](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/LlB85984174-image-20230917203146001.png)


以下為成功畫面

![image-20230917203316600](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/02cb413a-image-20230917203316600.png)

![image-20230917203419580](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/72166443-image-20230917203419580.png)

![image-20230917203559762](https://markweb.idv.tw/uploads/image-20230917203559762.png)