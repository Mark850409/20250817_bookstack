---
title: AI部署到zeabur
created: 2025-01-09 12:28:16Z
tags:
  - AI
  - Zeabur
  - 人工智慧
  - LINEBOT
  - LangChain
  - LangFlow
---
# 1. 簡介
建立`LangFlow`聊天機器人，並與`zeabur`平台串接

# 2. 目錄
- [1. 簡介](#1-簡介)
- [2. 目錄](#2-目錄)
- [3. 使用方式](#3-使用方式)
  - [3.1. LangFlow環境架設](#31-langflow環境架設)
  - [3.2. LineBotAPI架設](#32-linebotapi架設)
  - [3.3. LINE DEVELOPERS設定Webhook URL](#33-line-developers設定webhook-url)

# 3. 使用方式

## 3.1. LangFlow環境架設

請先到這個網頁進行註冊(最好有GitHub帳號)

https://zeabur.com/zh-TW

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/7OT413dc436-202501091835364.png)

請點擊`建立專案`
![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/288cb340-202501091836881.png)


> [!NOTE]
> 免費用戶將於24小時以後，自動刪除該主機，若要正式上線，請付費

這邊測試使用，可選擇`Free Trail`
![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/6kz6c1bcd0f-202501091837955.png)

這邊可選擇要部署的方式，若有版控需求，建議選擇`Github`
![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/33f8d480-202501091901872.png)

這邊請查看是否會有網域，如果沒有要`手動新增`
![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/Nrpbbc206b9-202501091902570.png)



![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/YDz20e09d25-202501091907037.png)

<!--more-->
## 3.2. LineBotAPI架設

請撰寫`app.py`

```python
import logging
import json
import requests
# LineBotApi
from linebot import LineBotApi, WebhookHandler  
from linebot.exceptions import InvalidSignatureError  
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,JoinEvent,FollowEvent
)
# 環境變數相關
import os
from dotenv import load_dotenv  # pip install python-dotenv
from flask import Flask,request

# 設置日誌模板
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 載入 .env 檔案
load_dotenv()

app = Flask(__name__)

#取得LINEBOT的CHANNEL_SECRET&CHANNEL_ACCESS_TOKEN&USER_ID
LANGFLOW_BASE_URL = os.getenv("LANGFLOW_BASE_URL") 
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")

if not LANGFLOW_BASE_URL or not CHANNEL_ACCESS_TOKEN or not CHANNEL_SECRET:
    logger.error("環境變數缺失，請確認 .env 檔案設置是否正確！")
    raise ValueError("必要的環境變數未設置！")

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


# LINE WEBHOOK串接進入點
@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)  # 取得收到的訊息內容
    signature = request.headers['X-Line-Signature']  # 加入回傳的 headers
    try:
        handler.handle(body, signature)  # 綁定訊息回傳的相關資訊
        json_data = json.loads(body)  # json 格式化訊息內容
    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        print(f"Error: {e}")  # 印出錯誤訊息
        print(body)  # 印出收到的內容

    return 'OK'  # 驗證 Webhook 使用，不能省略

#文字訊息觸發點
@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
   #取得文字內容
    input_text = event.message.text.strip()
    if input_text:
        try:
            result = call_api(input_text)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=result)
            )
        except Exception as e:
            logger.error(f"API 呼叫失敗: {e}")
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="無法處理您的請求，請稍後再試！")
            )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="您輸入的內容有誤，請重新嘗試！")
        )

    
#第一次加入好友觸發點
@handler.add(JoinEvent)
def handle_join(event):
    user_id = event.source.user_id  
    profile = line_bot_api.get_profile(user_id)  
    user_name = profile.display_name  
    text=''
    text+=f"{user_name}您好!\n"
    text+="我是關於韓國團體的十萬個為什麼\n"
    text+="感謝您加入好友😘\n\n"
    text+="您可以向我詢問了解韓國團體相關問題，我會盡可能提供回覆說明"
    line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=text)
        )
    
#封鎖後重新加入好友觸發點
@handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id  
    profile = line_bot_api.get_profile(user_id)  
    user_name = profile.display_name  
    text=''
    text+=f"{user_name}您好!\n"
    text+="我是關於韓國團體的十萬個為什麼\n"
    text+="感謝您加入好友😘\n\n"
    text+="您可以向我詢問了解韓國團體相關問題，我會盡可能提供回覆說明"
    line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=text)
        )

# 1、呼叫LangFlow API
def call_api(input_text):
    
    url = f"{LANGFLOW_BASE_URL}api/v1/run/ragflow?stream=false"
    headers = {"Content-Type": "application/json"}
    data = {
        "input_value": input_text,
        "output_type": "chat",
        "input_type": "chat",
        "ChatInput-AEgML": {
            "background_color": "",
            "chat_icon": "",
            "files": "",
            "input_value": "BLACKPINK成員有誰?",
            "sender": "User",
            "sender_name": "User",
            "session_id": "",
            "should_store_message": True,
            "text_color": ""
        },
        "ParseData-5gm6a": {
            "sep": "\n",
            "template": "{text}"
        },
        "Prompt-mXovt": {
            "context": "",
            "question": "",
            "template": "{context}\n\n---\n\nGiven the context above, answer the question as best as possible.\n\nQuestion: {question}\n\nAnswer: "
        },
        "SplitText-NVr6U": {
            "chunk_overlap": 200,
            "chunk_size": 1000,
            "separator": "\n"
        },
        "ChatOutput-cpZXc": {
            "background_color": "",
            "chat_icon": "",
            "data_template": "{text}",
            "input_value": "",
            "sender": "Machine",
            "sender_name": "AI",
            "session_id": "",
            "should_store_message": True,
            "text_color": ""
        },
        "OpenAIEmbeddings-EONzf": {
            "chunk_size": 1000,
            "client": "",
            "default_headers": {},
            "default_query": {},
            "deployment": "",
            "dimensions": None,
            "embedding_ctx_length": 1536,
            "max_retries": 3,
            "model": "text-embedding-3-small",
            "model_kwargs": {},
            "openai_api_base": "",
            "openai_api_key": "",
            "openai_api_type": "",
            "openai_api_version": "",
            "openai_organization": "",
            "openai_proxy": "",
            "request_timeout": None,
            "show_progress_bar": False,
            "skip_empty": False,
            "tiktoken_enable": True,
            "tiktoken_model_name": ""
        },
        "Chroma-gPLzo": {
            "allow_duplicates": False,
            "chroma_server_cors_allow_origins": "",
            "chroma_server_grpc_port": None,
            "chroma_server_host": "",
            "chroma_server_http_port": None,
            "chroma_server_ssl_enabled": False,
            "collection_name": "KPOP",
            "limit": None,
            "number_of_results": 10,
            "persist_directory": "KPOP_1227",
            "search_query": "",
            "search_type": "Similarity"
        },
        "Directory-zgZD3": {
            "depth": 0,
            "load_hidden": False,
            "max_concurrency": 2,
            "path": "/mnt/data",
            "recursive": False,
            "silent_errors": False,
            "types": "",
            "use_multithreading": False
        },
        "OpenAIEmbeddings-5fBe2": {
            "chunk_size": 1000,
            "client": "",
            "default_headers": {},
            "default_query": {},
            "deployment": "",
            "dimensions": None,
            "embedding_ctx_length": 1536,
            "max_retries": 3,
            "model": "text-embedding-3-small",
            "model_kwargs": {},
            "openai_api_base": "",
            "openai_api_key": "",
            "openai_api_type": "",
            "openai_api_version": "",
            "openai_organization": "",
            "openai_proxy": "",
            "request_timeout": None,
            "show_progress_bar": False,
            "skip_empty": False,
            "tiktoken_enable": True,
            "tiktoken_model_name": ""
        },
        "Chroma-XecOe": {
            "allow_duplicates": False,
            "chroma_server_cors_allow_origins": "",
            "chroma_server_grpc_port": None,
            "chroma_server_host": "",
            "chroma_server_http_port": None,
            "chroma_server_ssl_enabled": False,
            "collection_name": "KPOP",
            "limit": None,
            "number_of_results": 10,
            "persist_directory": "KPOP_1227",
            "search_query": "",
            "search_type": "Similarity"
        },
        "OllamaModel-tvBgy": {
            "base_url": "",
            "format": "",
            "input_value": "",
            "metadata": {},
            "mirostat": "Disabled",
            "mirostat_eta": None,
            "mirostat_tau": None,
            "model_name": "llama3.2:latest",
            "num_ctx": None,
            "num_gpu": None,
            "num_thread": None,
            "repeat_last_n": None,
            "repeat_penalty": None,
            "stop_tokens": "",
            "stream": False,
            "system": "",
            "system_message": "System Promt",
            "tags": "",
            "temperature": 0.5,
            "template": "",
            "tfs_z": None,
            "timeout": None,
            "top_k": None,
            "top_p": None,
            "verbose": False
        }
    }

    # 2、發送 POST 請求進行測試
    response = requests.post(url, headers=headers, data=json.dumps(data))
    logger.info(f"輸出響應內容是: {response}\n")
    # 3、檢查響應狀態碼
    if response.status_code == 200:
        try:
            logger.info(f"輸出響應內容是: {response.status_code}\n")
            logger.info(f"輸出響應內容是: {response.json()}\n")
            # 解析具體回覆的內容
            content = response.json()['outputs'][0]['outputs'][0]['results']['message']['data']['text']
            # 確保正確顯示中文，使用 print 並避免轉義
            print(json.dumps(content, ensure_ascii=False))  # 正確顯示中文
            return content
        except requests.exceptions.JSONDecodeError:
            # 響應不是 JSON 格式
            logger.info("響應內容不是有效的 JSON")
    else:
        logger.info(f"請求失敗，狀態碼為 {response.status_code}")

if __name__ == "__main__":
    logger.info("LINE Bot 已啟動！")
    app.run(host='0.0.0.0', port=5000)
```

請撰寫`requirements.txt`
```python
Flask==2.2.2
line-bot-sdk==3.13.0
Werkzeug==2.2.2
python-dotenv
requests
```


若python執行時有相關的環境變數，請在這邊進行設定

```
LANGFLOW_BASE_URL = <你的LangFlow的網址>
CHANNEL_ACCESS_TOKEN = <你的Line後台申請的CHANNEL_ACCESS_TOKEN>
CHANNEL_SECRET = <你的Line後台申請的CHANNEL_SECRET>
```

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/sSS02f75fc0-202501091920295.png)

點擊`部署`
![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/Mkiaf99facd-202501091920300.png)

## 3.3. LINE DEVELOPERS設定Webhook URL

填入剛才架設好的API網址，路由必須要指向`callback`
![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/7e0fddf4-202501091924751.png)

點擊`verify`，出現`Success`代表串接成功
![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/3044fdf5-202501091925814.png)