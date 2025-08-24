---
title: LINE串接ChaptGPT實作
updated: 2024-10-22 20:21:59Z
created: 2024-02-18 12:28:16Z
tags:
  - ChatGPT
  - LINEBOT
  - API
---
# 1. LINE串接ChaptGPT實作

## 1.1. 簡介
LINEBOT串接OpenAI，讓LINE擁有ChatGPT一般的功能

## 1.2. 目錄

- [1. LINE串接ChaptGPT實作](#1-line串接chaptgpt實作)
  - [1.1. 簡介](#11-簡介)
  - [1.2. 目錄](#12-目錄)
  - [1.3. 專案架構](#13-專案架構)
    - [1.3.1. 完成畫面](#131-完成畫面)
    - [1.3.2. 注意事項](#132-注意事項)
    - [1.3.3. 撰寫程式](#133-撰寫程式)
    - [1.3.4. 測試方式](#134-測試方式)


## 1.3. 專案架構
```
20240101_AzureGradioAPI
├─ flagged
├─ mytestgradio.py
├─ README.md
└─ __pycache__
   ├─ gradio.cpython-311.pyc
   └─ mytestgradio.cpython-311.pyc
```

### 1.3.1. 完成畫面

![image-20240101172925968](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/1bZ372bf366-image-20240101172925968.png)


![image-20240101172955045](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/Qsf9ca6ccbb-image-20240101172955045.png)



### 1.3.2. 注意事項

>[!NOTE] 小提示
>1. 執行時若出現got an unexpected keyword argument ‘socket_options，請手動執行pip install -U httpx==0.24.1
>2. 不要使用最新版，會出錯，請指定版本，pip install openai==0.28.0
>3. 安裝完成後最好使用此指令更新一下pip，python.exe -m pip install --upgrade pip
>4. 最後使用pip list確認套件庫是否正確安裝
>5. 請記得要在chatgpt事先申請api key


### 1.3.3. 撰寫程式

在mytestgradio.py撰寫以下程式碼

<div class="code-filename">
<i class="fa fa-file-code-o"></i>mytestgradio.py
</div>




```python
import openai
import gradio as gr
from functools import partial

#初始化訊息
def initialize():
    initialMessage = [
        {
            "role": "system",
            "content": """你是一個親切的天氣助手，將會協助我取得我需要的天氣資訊。
            我將透過以下形式來提供你查詢的資訊：
            城市：日期
            你需要回答我這個城市在我指定的日期將會是什麽樣的天氣。
            """
        },
        {
            "role": "user",
            "content": """請提供我以下城市的天氣資訊
            台北：2023/2/28
            """,
        },
        {
            "role": "assistant",
            "content": "陰雨"
        }
    ]
    return initialMessage

#更新角色
def updateMessageList(message, role, messageList):
    
    try:
        messageList.append({
            "role": role,
            "content": message,
        })
    except Exception as e:
        print(e)
    
    return messageList

#取得ChatGPT回傳內容
def getResponse(promot, history=[], messageList={}):
    
    # 將使用者輸入內容更新至訊息紀錄
    updateMessageList(promot, 'user', messageList)

    # 與API互動並取得回應
    responseDict = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messageList,
    )
  
    # 擷取回覆字串
    responseMessage = responseDict['choices'][0]['message']['content']

    # 將回覆更新至訊息紀錄
    updateMessageList(responseMessage, 'assistant', messageList)
    
    # 將使用者以及機器人的訊息整理為兩個串列
    userContext = [content['content'] for content in messageList if content['role'] == 'user']
    assistantContext = [content['content'] for content in messageList if content['role'] == 'assistant']
    
    # 利用使用者以及機器人訊息構成對話紀錄
    response = [(_user, _response) for _user, _response in zip(userContext[1:], assistantContext[1:])]

    # 回傳對話紀錄，由於我們使用自定義的方法進行訊息紀錄，故不需要回傳紀錄
    return response, []

#主程式進入點
def main():

    #設定openAPIKey
    openai.api_key = '自己的token ID'

    messageList = initialize()

    partialGetResponse = partial(getResponse, messageList=messageList)

    #使用Gradio初始化模組
    with gr.Blocks() as demo:
        gr.Markdown(
        """
        # CHATGPT聊天機器人上線囉!!!
        趕快和AI互動吧!!!
        """)
        chatbot = gr.Chatbot()
        state = gr.State([])

        with gr.Row():
            text = gr.Textbox(
                show_label=False,
                placeholder="對ChatGPT說些什麽.....",
                
            ).style(container=False)
        greet_btn=gr.Button("提交")
        greet_btn.click(fn=partialGetResponse,inputs=[text, state], outputs=[chatbot, state])
    #share=True這個參數是設定可以產生公開連結
    demo.launch(share=True)


if __name__ == '__main__':
    main()
```

### 1.3.4. 測試方式

>[!NOTE] 小提示
>1. 輸入`python mytestgradio.py`執行
>2. 使用`VSCODE`，建立好python環境，點選`執行`按鈕