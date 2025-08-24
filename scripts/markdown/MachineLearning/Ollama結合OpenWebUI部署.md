---
title: Ollama結合OpenWebUI部署
created: 2024-08-17 02:39:46Z
updated: 2024-08-17 03:39:46Z
tags:
  - Ollama
  - OpenWebUI
  - ML
  - Docker
---
# 1. Ollama結合OpenWebUI部署

安裝Docker[^1]


## 1.1. 簡介

透過Ollama結合OpenWebUI，實現地端ChatGPT

## 1.2. 目錄

- [1. Ollama結合OpenWebUI部署](#1-ollama結合openwebui部署)
  - [1.1. 簡介](#11-簡介)
  - [1.2. 目錄](#12-目錄)
  - [1.3. 操作步驟](#13-操作步驟)
    - [1.3.1. 撰寫docker-compose.yml](#131-撰寫docker-composeyml)
    - [1.3.2. 執行以下指令](#132-執行以下指令)
    - [1.3.3. 請確認容器都是running的狀態](#133-請確認容器都是running的狀態)
    - [1.3.4. 拉取Ollama模型](#134-拉取ollama模型)
  - [1.4. 完成畫面](#14-完成畫面)
  - [1.5. 問題處理](#15-問題處理)
    - [1.5.1. 參考資料](#151-參考資料)


<!--more-->
## 1.3. 操作步驟

### 1.3.1. 撰寫docker-compose.yml

```yaml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - NVIDIA_DRIVER_CAPABILITIES=compute,utility
      - OLLAMA_KEEP_ALIVE=-1
      - OLLAMA_ORIGINS=app://obsidian.md*
    container_name: ollama
    volumes:
      - C:\WorkSpace\ollama\data:/root/.ollama/models  # 將本地的 data 目錄掛載到容器內
    ports:
      - "80:11434"  # 替換成你需要的端口配置
    restart: unless-stopped

  webgui:
    image: ghcr.io/open-webui/open-webui:ollama
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]
    container_name: ollama-webgui
    ports:
      - "8081:8080"  # Ollama Web GUI 端口
    volumes:
      - C:\WorkSpace\ollama\data:/root/.ollama/models  # 將本地的 data 目錄掛載到容器內
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - NVIDIA_DRIVER_CAPABILITIES=compute,utility
      - OLLAMA_API_URL=http://ollama:80  # 指向 Ollama API 的URL
      - OLLAMA_KEEP_ALIVE=-1
      - OLLAMA_ORIGINS=app://obsidian.md*
    depends_on:
      - ollama  # 確保 Web GUI 在 Ollama API 啟動後再啟動
    restart: unless-stopped
```


### 1.3.2. 執行以下指令

```bash
docker-compose up -d
```


### 1.3.3. 請確認容器都是running的狀態

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/z2f69a8efb0-202408142222136.png)



> [!note] 小提示
> 1. 因為OpenWebUI是和Ollama作連動，啟動時會比較慢實屬正常
> 2. 請確認有看到如下圖字樣才表示啟動成功喔
> 3. 安裝python(建議3.10版本)
> 4. 安裝完成後可以執行pip install ollama，這樣就可以在本機拉取ollama模型


![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/rurcbcbac11-202408142224768.png)


### 1.3.4. 拉取Ollama模型

請到Ollama官網查看模型 [^2]

例如：我想要抓取mistral:7b

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/zKdc0024367-202408142233739.png)


執行指令

```bash
ollama list
```

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/4b40d438-202408142235211.png)


執行指令

```bash
ollama list
```

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/9b6123a35d6-202408142230593.png)

## 1.4. 完成畫面

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/2Wk60ed0b3a-202408142217664.png)


![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/2ar49a8e508-202408142217682.png)

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/Kc3fbd55101-202408142218986.png)


## 1.5. 問題處理

請參考此網站[^3]

> [!note]  gpu VRAM usage didn't recover within timeout
>  `**OLLAMA_KEEP_ALIVE**`：大模型在記憶體中保留的時間，預設為5分鐘（5m）。例如，像 300 這樣的純數字表示 300 秒，0 表示模型在處理請求後立即卸載，任何負數表示模型無限期地保持載入狀態。可設定為24h，使模型在記憶體中保留24小時，提高存取速度

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/c36ef3bb-202408142325268.png)
### 1.5.1. 參考資料

[^1]: [[安裝Docker]]
[^2]: Ollama 模型參考 https://ollama.com/library/
[^3]:  https://medium.com/@researchgraph/how-to-run-ollama-on-windows-8a1622525ada


