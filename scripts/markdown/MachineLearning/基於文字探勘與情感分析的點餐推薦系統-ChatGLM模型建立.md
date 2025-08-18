---
title: 基於文字探勘與情感分析的點餐推薦系統-ChatGLM模型建立
updated: 2024-08-04 11:24:44Z
created: 2024-07-28 15:44:47Z
latitude: 25.0329694
longitude: 121.5654177
altitude: 0
tags:
  - ML
  - python
  - ChatGLM
  - Model
  - Order
---

# 1.  基於文字探勘與情感分析的點餐推薦系統-ChatGLM模型建立

## 1.1. 簡介

手動建立`ChatGLM`，使其不用受到CHATGPT原生模型`付費限制`

## 1.2. 目錄

- [1.  基於文字探勘與情感分析的點餐推薦系統-ChatGLM模型建立](#1--基於文字探勘與情感分析的點餐推薦系統-chatglm模型建立)
  - [1.1. 簡介](#11-簡介)
  - [1.2. 目錄](#12-目錄)
  - [1.3. Windows操作步驟](#13-windows操作步驟)
    - [1.3.1. 請先將Github大神的專案`fork`到自己本機](#131-請先將github大神的專案fork到自己本機)
    - [1.3.2. 撰寫python API測試腳本](#132-撰寫python-api測試腳本)
    - [1.3.3. 開始安裝](#133-開始安裝)
  - [1.4. Colab操作步驟-地端](#14-colab操作步驟-地端)
    - [1.4.1. 地端測試方式](#141-地端測試方式)
    - [1.4.2. 地端測試結果](#142-地端測試結果)
  - [1.5. Colab操作步驟-雲端](#15-colab操作步驟-雲端)
    - [1.5.1. colab雲端測試方式](#151-colab雲端測試方式)
    - [1.5.2. colab雲端測試結果](#152-colab雲端測試結果)
  - [1.6. 完成畫面](#16-完成畫面)

## 1.3. Windows操作步驟

### 1.3.1. 請先將Github大神的專案`fork`到自己本機

https://github.com/THUDM/ChatGLM-6B


### 1.3.2. 撰寫python API測試腳本

### 1.3.3. 開始安裝

安裝所需套件

> [!note] 小提示 
> 這裡的transformers、torch有版本限制，目前實測請依據這版本進行安裝

```python
!pip install protobuf gradio mdtex2html sentencepiece accelerate

!pip install transformers==4.27.1

!pip install cpm_kernels

!pip install torch==2.3.1 torchvision torchaudio --index-url https://download.pytorch.org/whl/test/cu121
```

測試GPU環境
```python
import torch
print(torch.cuda.is_available())
```

Windows記得要安裝`cuda-toolkit`，因為要使用GPU執行比較有效率

https://developer.nvidia.com/cuda-toolkit


 、模型及參數微調

這邊的模型請參考大神的github說明進行微調

```python
model = AutoModel.from_pretrained("THUDM/chatglm-6b-int8", trust_remote_code=True).half().cuda()
```

---
<!--more-->

## 1.4. Colab操作步驟-地端

### 1.4.1. 地端測試方式

第 代模型測試方式

- 使用`curl`指令`測試API`

```bash
curl -X POST "https://d270-35-240-232-241.ngrok-free.app" -H "Content-Type: application/json" -d "{\"prompt\": \"你好，請幫我將以下這幾句話翻譯成英文:\n\n1. 中午站櫃檯的男員工的表情臭到不行就算了,詢問問題不是不回答就是愛理不理,如果不喜歡服務業就回家吃自己,我們客人沒有欠你！\n\n2. 在北醫對面點餐到取飲料流程還ok,也可以「無接觸支付」！今天點無糖烏龍+燕麥烏龍蠻香的！燕麥 點點甜,搭配就剛好 偶爾想喝,願意回來購買\n\n3. 中午用餐時段過去,很多外送訂單店員忙碌,但是還是非常親切,尤其是點單跟做飲料有個叫做金吧台手的林姓店員,圍兜有金邊的,服務特別親切,飲料是真的久等了,雖然有點不耐了,但他奉上飲料還是說了聲「讓您久等了」令人感到這是很棒的服務。\", \"history\": []}"
```

- 使用`python`腳本`測試API`

```python
import requests

# 定義翻譯函數
def translate_to_english(texts):
    translations = []
    url = "https://d270-35-240-232-241.ngrok-free.app"  # 替換為你的 API 端點

    for text in texts:
        # 設定 API 請求參數
        payload = {
            "prompt": f"Translate the following text from Chinese to English:\n\n{text}",
            "history": []
        }
        headers = {
            "Content-Type": "application/json"
        }

        # 發送 POST 請求
        response = requests.post(url, json=payload, headers=headers)

        # 檢查請求是否成功
        if response.status_code == 200:
            # 解析回應
            translation = response.json().get("response", "").strip()
            translations.append(translation)
        else:
            translations.append(f"Error: {response.status_code}")

    return translations

# 測試翻譯
chinese_texts = [
    "中午站櫃檯的男員工的表情臭到不行就算了，詢問問題不是不回答就是愛理不理，如果不喜歡服務業就回家吃自己，我們客人沒有欠你！",
    "在北醫對面點餐到取飲料流程還ok,也可以「無接觸支付」！今天點無糖烏龍+燕麥烏龍蠻香的！燕麥 點點甜，搭配就剛好 偶爾想喝，願意回來購買",
    "中午用餐時段過去，很多外送訂單店員忙碌，但是還是非常親切，尤其是點單跟做飲料有個叫做金吧台手的林姓店員，圍兜有金邊的，服務特別親切，飲料是真的久等了，雖然有點不耐了，但他奉上飲料還是說了聲「讓您久等了」令人感到這是很棒的服務。"
]

english_texts = translate_to_english(chinese_texts)
print(english_texts)
for i, (chinese_text, english_text) in enumerate(zip(chinese_texts, english_texts), start=1):
    print(f"Original Chinese text {i}: {chinese_text}")
    print(f"Translated English text {i}: {english_text}")
    print()
```


第 代模型測試方式

- 可以參考第 代模型測試方式，與第 代測試方式相同


第 代模型測試方式


- 使用`curl`腳本測試第 代模型

```bash
curl -X POST "https://7017-34-147-49-113.ngrok-free.app/v1/chat/completions" ^
-H "Content-Type: application/json" ^
-d "{\"model\": \"your-translation-model\", \"messages\": [{\"role\": \"system\", \"content\": \"You are a translation model trained to translate between Chinese and English. Follow the user's instructions carefully. Respond using markdown.\"}, {\"role\": \"user\", \"content\": \"中午用餐時段過去，很多外送訂單店員忙碌，但是還是非常親切，尤其是點單跟做飲料有個叫做金吧台手的林姓店員，圍兜有金邊的，服務特別親切，飲料是真的久等了，雖然有點不耐了，但他奉上飲料還是說了聲「讓您久等了」令人感到這是很棒的服務。\"}], \"stream\": false, \"max_tokens\": 100, \"temperature\": 0.8, \"top_p\": 0.8}"
```


- 使用`python`腳本測試第 代模型

```python
import requests
import json

def translate_text(texts):
    url = "https://9701-34-74-115-81.ngrok-free.app/v1/chat/completions"
    headers = {
        "Content-Type": "application/json"
    }
    translations = []

    for text in texts:
        data = {
            "model": "your-translation-model",
            "messages": [
                {"role": "system", "content": "You are a translation model trained to translate between Chinese and English. Follow the user's instructions carefully. Respond using markdown."},
                {"role": "user", "content": text}
            ],
            "stream": False,
            "max_tokens": 100,
            "temperature": 0.8,
            "top_p": 0.8
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            translation = response.json()
            translations.append(translation)
        else:
            translations.append({"error": "Failed to get translation", "status_code": response.status_code})

    return translations

# Example usage
texts_to_translate = [
    "中午站櫃檯的男員工的表情臭到不行就算了，詢問問題不是不回答就是愛理不理，如果不喜歡服務業就回家吃自己，我們客人沒有欠你！",
    "在北醫對面點餐到取飲料流程還ok,也可以「無接觸支付」！今天點無糖烏龍+燕麥烏龍蠻香的！燕麥 點點甜，搭配就剛好 偶爾想喝，願意回來購買",
    "中午用餐時段過去，很多外送訂單店員忙碌，但是還是非常親切，尤其是點單跟做飲料有個叫做金吧台手的林姓店員，圍兜有金邊的，服務特別親切，飲料是真的久等了，雖然有點不耐了，但他奉上飲料還是說了聲「讓您久等了」令人感到這是很棒的服務。"
]

translations = translate_text(texts_to_translate)
for i, translation in enumerate(translations):
    print(f"Translation {i+1}:")
    print(json.dumps(translation, indent=2, ensure_ascii=False))
    print()
```

--- 

### 1.4.2. 地端測試結果

第一代模型測試結果
```json
Original Chinese text 1: 中午站櫃檯的男員工的表情臭到不行就算了，詢問問題不是不回答就是愛理不理，如果不喜歡服務業就回家吃自己，我們客人沒有欠你！
Translated English text 1: The male employees who are standing at the bus stop on中午 have a bad的表情， they either don't answer the questions or ignore them. If you don't like the service industry, go back home and eat yourself, we don't欠 you!

Original Chinese text 2: 在北醫對面點餐到取飲料流程還ok,也可以「無接觸支付」！今天點無糖烏龍+燕麥烏龍蠻香的！燕麥 點點甜，搭配就剛好 偶爾想喝，願意回來購買
Translated English text 2: The food and payment process in北醫對面 is still okay, and you can also「無接觸支付」! Today, I'd like to have a no糖 Chinese ice cream + Chinese siniper for free! The Chinese ice cream is delicious and the combination is perfect. If you want to drink it, I'd be happy to buy it back from you.

Original Chinese text 3: 中午用餐時段過去，很多外送訂單店員忙碌，但是還是非常親切，尤其是點單跟做飲料有個叫做金吧台手的林姓店員，圍兜有金邊的，服務特別親切，飲料是真的久等了，雖然有點不耐了，但他奉上飲料還是說了聲「讓您久等了」令人感到這是很棒的服務。
Translated English text 3: The afternoon用餐 period has passed, and many delivery store employees are busy, but they are still very friendly. especially the store employee named Lin Jin, who is known for making the drinks, is particularly friendly. The drinks are really long in waiting, although some people are getting tired, but Lin Jin will still bring them over and say "让您久等了" which makes it a great service.


```


![](https://markweb.idv.tw/uploads/202408041817430.png)


第二代模型測試結果
```json
Original Chinese text 1: 中午站櫃檯的男員工的表情臭到不行就算了，詢問問題不是不回答就是愛理不理，如果不喜歡服務業就回家吃自己，我們客人沒有欠你！
Translated English text 1: The male employee at the receptionist desk had such a stinky expression that it was hard to ignore. Asking questions was either not answered or they gave you a cold shoulder. If they didn't like customer service, they should have gone home and eaten by themselves. We, your customers, don't owe you anything!

Original Chinese text 2: 在北醫對面點餐到取飲料流程還ok,也可以「無接觸支付」！今天點無糖烏龍+燕麥烏龍蠻香的！燕麥 點點甜，搭配就剛好 偶爾想喝，願意回來購買
Translated English text 2: The ordering and pick-up饮料 process at Northern Medical University is still good, and you can even pay "contact-free!" today. The vegetarian black tea and oatmeal black tea are quite fragrant. The oatmeal is a bit sweet, and it's just the right amount to drink when you want to drink it. Sometimes, you would like to drink it and would be willing to come back and buy it.

Original Chinese text 3: 中午用餐時段過去，很多外送訂單店員忙碌，但是還是非常親切，尤其是點單跟做飲料有個叫做金吧台手的林姓店員，圍兜有金邊的，服務特別親切，飲料是真的久等了，雖然有點不耐了，但他奉上飲料還是說了聲「讓您久等了」令人感到這是很棒的服務。
Translated English text 3: After lunchtime, many delivery order staff are busy, but they are still very warm and friendly. Among them, there is a Lin customer service staff who works in the金吧台手 area, who is especially warm and helpful. He is wearing a golden-edged towel and is very courteous in service. As for the delivery, it really took some time, but even though it was a bit frustrating, the staff still apologized and said "I'm sorry for the delay." This made the delivery a truly great service.
```


第三代模型測試結果

```json
E:\Project\developer_project\thesis\flask_crud_vue\venv\Scripts\python.exe E:\Project\developer_project\thesis\20240727_flask_crud_vue\backend\CustomChatGLM3_translate.py 
Translation 1:
{
  "model": "your-translation-model",
  "id": "",
  "object": "chat.completion",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "I'm sorry to hear that you had a bad experience with the male staff at the counter during your lunch break. It's important for customers to receive good service, and it's unfortunate that the staff did not meet your expectations. However, it's also important to remember that everyone has their bad days or times when they may not be as friendly or attentive as usual. It's possible that the staff was having a busy day or was feeling overwhelmed with work",
        "name": null,
        "function_call": null
      },
      "finish_reason": "stop"
    }
  ],
  "created": 1722266565,
  "usage": {
    "prompt_tokens": 76,
    "total_tokens": 176,
    "completion_tokens": 100
  }
}

Translation 2:
{
  "model": "your-translation-model",
  "id": "",
  "object": "chat.completion",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "**Good service at北醫 counter!**\n\nThe ordering process for food and drinks at Bei-Med is acceptable, and you can even make contactless payments! Today, I ordered sugar-free black milk tea and oatmeal black milk tea, which were quite delicious. The oatmeal has a slight sweetness, and it goes well with the drink. I will definitely come back to buy more.",
        "name": null,
        "function_call": null
      },
      "finish_reason": "stop"
    }
  ],
  "created": 1722266621,
  "usage": {
    "prompt_tokens": 89,
    "total_tokens": 177,
    "completion_tokens": 88
  }
}

Translation 3:
{
  "model": "your-translation-model",
  "id": "",
  "object": "chat.completion",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "During lunchtime, many takeout orders were placed, and the store staff were busy. However, they still maintained a friendly attitude. In particular, a store employee named Lin who handled ordering and making drinks had a golden apron. He was very attentive and made sure to serve the drinks with a bow. Despite the long wait for the drinks, he still said \"I'm sorry for the delay\" when he brought them, which made people feel that it was excellent service",
        "name": null,
        "function_call": null
      },
      "finish_reason": "stop"
    }
  ],
  "created": 1722266684,
  "usage": {
    "prompt_tokens": 123,
    "total_tokens": 223,
    "completion_tokens": 100
  }
}


Process finished with exit code 0

```

## 1.5. Colab操作步驟-雲端

### 1.5.1. colab雲端測試方式

請參考本人撰寫的程式碼

https://colab.research.google.com/drive/1l8Ybtknzr_SSpeBVchUUWr83Xm7R9PCS#scrollTo=PshtGWihZb_2

請先設定好執行階段類型

![](https://markweb.idv.tw/uploads/202408041756132.png)

指定預設編碼

![](https://markweb.idv.tw/uploads/202408041757163.png)

印出目前的編碼

![](https://markweb.idv.tw/uploads/202408041757446.png)

掛載雲端硬碟

![](https://markweb.idv.tw/uploads/202408041758790.png)

![](https://markweb.idv.tw/uploads/202408041758319.png)

![](https://markweb.idv.tw/uploads/202408041758366.png)

![](https://markweb.idv.tw/uploads/202408041759498.png)

![](https://markweb.idv.tw/uploads/202408041759690.png)

開始安裝套件(自己選擇要安裝第幾代)

![](https://markweb.idv.tw/uploads/202408041800793.png)

安裝pyngrok進行內網穿透(要先執行)

![](https://markweb.idv.tw/uploads/202408041802128.png)

找到要執行的主程式(例如第 代Gradio)

![](https://markweb.idv.tw/uploads/202408041803808.png)

這步驟表示正在下載並安裝模型，有7個，請耐心等待下載完成

![](https://markweb.idv.tw/uploads/202408041804367.png)

看到這個訊息表示已完成

![](https://markweb.idv.tw/uploads/202408041805916.png)

---

### 1.5.2. colab雲端測試結果

測試回應

![](https://markweb.idv.tw/uploads/202408041806992.png)

測試翻譯

![](https://markweb.idv.tw/uploads/202408041807951.png)

---

## 1.6. 完成畫面

![](https://markweb.idv.tw/uploads/202407282351067.png)

![](https://markweb.idv.tw/uploads/202407290019769.png)

![](https://markweb.idv.tw/uploads/202407290020253.png)

