---
title: python地址轉換ZIPCODE
updated: 2024-07-21 05:25:47Z
created: 2024-02-18 12:29:46Z
latitude: 25.0329694
longitude: 121.5654177
altitude: 0
tags:
  - python
  - ZIPCODE
---

# 1. python地址轉換ZIPCODE


## 1.1. 簡介

透過python程式批次將地址轉換為郵遞區號

## 1.2. 目錄

- [1. python地址轉換ZIPCODE](#1-python地址轉換zipcode)
  - [1.1. 簡介](#11-簡介)
  - [1.2. 目錄](#12-目錄)
  - [1.3. 專案架構](#13-專案架構)
  - [1.4. 操作步驟](#14-操作步驟)
    - [1.4.1. 登入`gitlab`，點擊`Fork`](#141-登入gitlab點擊fork)
    - [1.4.2. 專案URL下拉要選擇`預設命名空間`](#142-專案url下拉要選擇預設命名空間)
    - [1.4.3. 點擊`分叉專案`](#143-點擊分叉專案)
    - [1.4.4. 請先下git指令將程式碼`推送到專案`，這 塊可參考`程式碼片段`](#144-請先下git指令將程式碼推送到專案這-塊可參考程式碼片段)
    - [1.4.5. 點選`原始碼→合併請求`](#145-點選原始碼合併請求)
    - [1.4.6. 點選新建合併請求](#146-點選新建合併請求)
    - [1.4.7. 選擇預設來源分支`master`](#147-選擇預設來源分支master)
    - [1.4.8. 這裡的`描述細節`盡可能`越詳細越好`](#148-這裡的描述細節盡可能越詳細越好)
    - [1.4.9. 被指派者選擇`admin`](#149-被指派者選擇admin)
    - [1.4.10. 點選`建立合併請求`](#1410-點選建立合併請求)
  - [1.5. 程式碼片段參考](#15-程式碼片段參考)
  - [1.6. 專案撰寫步驟](#16-專案撰寫步驟)
    - [1.6.1. 撰寫`transfterZipCode.py`](#161-撰寫transfterzipcodepy)
    - [1.6.2.  完成畫面如下](#162--完成畫面如下)


## 1.3. 專案架構
```
20240208_pythonZipCode
├─ addressV2.xlsx
├─ img
├─ README.md
├─ report.html
├─ static
│  ├─ images
│  │  ├─ case1_error.png
│  │  └─ case1_final.png
│  └─ report
├─ transfterZipCode.py
└─ __pycache__
   └─ transfterZipCode.cpython-311.pyc
```

## 1.4. 操作步驟

### 1.4.1. 登入`gitlab`，點擊`Fork`

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/4CS4e5832b0-upload-8b11d8993b821ec6152435f742be6a1d.png)

### 1.4.2. 專案URL下拉要選擇`預設命名空間`
![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/8d114832-upload-724342e9ea4c1723c3ce17b90c72ac79.png)

### 1.4.3. 點擊`分叉專案`
![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/pBG1e1233ff-upload-0f2505be53399349ec3068bfa98e565e.png)

### 1.4.4. 請先下git指令將程式碼`推送到專案`，這 塊可參考`程式碼片段`


### 1.4.5. 點選`原始碼→合併請求`
![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/ceb3f40c-upload-158481ded5c18e7ad08b299d20bc01ee.png)

### 1.4.6. 點選新建合併請求
![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/8be329ad-upload-39aad826cbcba0c4ec80eca939256131.png)

### 1.4.7. 選擇預設來源分支`master`
![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/511e4682-upload-23523d5fef15bcaa18fe96ad059afbb1.png)

### 1.4.8. 這裡的`描述細節`盡可能`越詳細越好`
![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/rk813fdfdfd-upload-4bfc54bb1ae0bc8234b8cd0882902db3.png)

### 1.4.9. 被指派者選擇`admin`
![](https://markweb.idv.tw/uploads/upload_f673f04d652463772c76e3385e0f5c8b.png)

### 1.4.10. 點選`建立合併請求`
![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/ca79e6c5-upload-3f81aa6586e6a2b52aad474dd4915582.png)


## 1.5. 程式碼片段參考
進入專案 > 點選原始碼 > 程式碼片段

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/S8b6a81c122-upload-71362957f8e0353abe822a7f62d5f8b4.png)

<!--more-->

## 1.6. 專案撰寫步驟

### 1.6.1. 撰寫`transfterZipCode.py`

```python
from selenium import webdriver
## BY: 也就是依照條件尋找元素中XPATH、CLASS NAME、ID、CSS選擇器等都會用到的Library
from selenium.webdriver.common.by import By
## keys: 鍵盤相關的Library
from selenium.webdriver.common.keys import Keys
## Select: 下拉選單相關支援，但前端框架UI工具不適用(ex: Quasar、ElementUI、Bootstrap)
from selenium.webdriver.support.ui import Select
## WebDriverWait: 等待頁面加載完成的顯性等待機制Library
from selenium.webdriver.support.ui import WebDriverWait
## ActionChains: 滑鼠事件相關
from selenium.webdriver.common.action_chains import ActionChains
## expected_conditions: 條件相關
from selenium.webdriver.support import expected_conditions as EC
## BeautifulReport: 產生自動測試報告套件
from BeautifulReport import BeautifulReport
## Chrome WebDriver 需要DRIVER Manager的支援
from webdriver_manager.chrome import ChromeDriverManager
## 延遲時間相關
import time
## 單元測試模組，線性測試用不到
import unittest
## 系統相關
import os
## 將爬蟲資料寫入EXCEL&CSV
import pandas as pd
## 取得日期時間模組
from datetime import datetime

## 取得系統路徑
root_path=os.path.dirname(os.path.realpath(__file__))

## 取得當下日期
get_current_date = datetime.today().strftime("%Y-%m-%d")

## 取得當下日期
get_current_month = datetime.today().strftime("%Y")

## 設定Chrome的瀏覽器彈出時遵照的規則
## 這串設定是防止瀏覽器上頭顯示「Chrome正受自動控制」
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
## 關閉自動記住密碼的提示彈窗
options.add_experimental_option("prefs", {
    "profile.password_manager_enabled": False,
    "credentials_enable_service": False
})
## 背景執行
#options.add_argument('--headless')


## 我們如果要將CASE拆成幾個不同的方法，需要用一個Unitest Class包覆起來
## 然後加上修飾符@classmethod                        
class Test(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.driver = webdriver.Chrome(options)
        self.action = ActionChains(self.driver)
        self.URL = "https://zip5.5432.tw/"
        self.driver.get(self.URL)
        self.driver.maximize_window()
        
        
    
    ## 所有case跑完後就退出瀏覽器
    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    # 當測試案例有錯誤時，截圖
    def save_img(self, test_method):
        img_path = root_path + '\\static\\images\\'
        self.driver.get_screenshot_as_file('{}/{}.png'.format(img_path, test_method))

    #使用者輸入判斷
    def UserInputValidate(self,obj):
        try:
            if not (obj):
                self.assertFalse(obj)
                print("pass")
        except ValueError as e:
            print("e:", e)
    
    #如果目錄不存在就自動建立圖片資料夾
    def create_img_folder(self,path):
        if not os.path.exists(path):
            #shutil.rmtree(path)
            os.makedirs(path)
    
    ## Test Case 的命名方式務必以「test_01_* ~ test_99_*」為主，讓爬蟲依照順序走
    ## """裡面的註解就是報表產生後的CASE描述文字。
    ## time.sleep(number)數字代表一秒
    
    def test_01_UserInputAndSearch(self):
        """
        根據addressV2.xlsx的地址，進入台灣3+2郵遞區號查詢相對應郵遞區號
        """ 
        self.create_img_folder("img")
        time.sleep(2) 
        try:
            # 讀取EXCEL
            myaddress=pd.read_excel("addressV2.xlsx",sheet_name='工作表1', usecols="B")

            # 將資料轉換為DataFrame
            df = pd.DataFrame(myaddress)
            
            #看資料長什麼樣子
            #print(df["SHIP_ADDRE"])

            #將地址欄位所有資料取出
            search_value=df["SHIP_ADDRE"]

            #宣告陣列存放ZIP_CODE
            ZIP_CODE_DATA_5=[]
            ZIP_CODE_DATA_6=[]
            
            #迴圈將地址資料取出，並丟到網站進行查詢
            for search_values in search_value:
                #查詢欄位元素定位
                self.driver.find_element(By.XPATH,"//*[@id='zip5-input']").send_keys(search_values)
                #查詢按鈕元素定位
                self.driver.find_element(By.XPATH,"//*[@id='zip5-btn']").click()
                time.sleep(2)
                #取得郵遞區號
                ZIP_CODE5=self.driver.find_element(By.XPATH,'//*[@id="zipcode"]').text
                ZIP_CODE6=self.driver.find_element(By.XPATH,'//*[@id="zipcode6"]').text
                #印出來看一下
                print("地址："+search_values+"\n5碼郵遞區號為："+ZIP_CODE5+"\n6碼郵遞區號為："+ZIP_CODE6+"\n=================")
                #將3+2郵遞區號存到陣列
                ZIP_CODE_DATA_5.append(ZIP_CODE5)
                ZIP_CODE_DATA_6.append(ZIP_CODE6)
            #將原始檔的資料複製到新的excel
            df1 = df.copy()
            #增加ZIP_CODE的資料
            df1['ZIP_CODE5'] = ZIP_CODE_DATA_5
            df1['ZIP_CODE6'] = ZIP_CODE_DATA_6
            #寫入新的檔案
            with pd.ExcelWriter('addressZipCode.xlsx') as writer:  
                df1.to_excel(writer, sheet_name='addressZipCode',index=False)
        except Exception as error:
            self.save_img("case1_error")
            print("case1：測試執行失敗！")
            raise error   
        else:
            self.save_img("case1_final")
            print("case1：測試執行成功。")
        finally:
            time.sleep(2)

#這邊會產生測試報告
filename = 'report'
description = '我的第一個測試'
theme = 'theme_candy'
#設定報告路徑參數
basedir = root_path + '\\static\\report\\'
if __name__ == '__main__':
    # 取得資料夾目錄底下，符合後面任何副檔名為.py，並進行所有test的測試項目
    test_suite = unittest.defaultTestLoader.discover(root_path, pattern='transfterZipCode.py')
    # 測試結果加入到 BeautifulReport 套件內
    result = BeautifulReport(test_suite)
    # 結果產生Report 檔案名稱為 filename, 敘述為 description, log_path 預設放在跟目錄底下就行
    result.report(filename=filename,description=description, log_path=basedir,theme=theme)
```

### 1.6.2.  完成畫面如下

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/KP9f42999da-upload-14b04c79a15fcbfc025b864e9eca8341.png)