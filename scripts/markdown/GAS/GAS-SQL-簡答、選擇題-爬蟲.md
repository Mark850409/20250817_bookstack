---
title: GAS-SQL-簡答、選擇題-爬蟲
updated: 2024-07-23 13:28:59Z
created: 2023-08-04 08:26:29Z
tags:
  - GAS
---

# 1 GAS-SQL-簡答、選擇題-爬蟲

## 1.1 簡介
學習如何在GAS撰寫腳本

## 1.2 目錄

- [1 GAS-SQL-簡答、選擇題-爬蟲](#1-gas-sql-簡答選擇題-爬蟲)
  - [1.1 簡介](#11-簡介)
  - [1.2 目錄](#12-目錄)
  - [1.3 GAS-SQL簡答程式撰寫](#13-gas-sql簡答程式撰寫)
    - [1.3.1 撰寫html模板](#131-撰寫html模板)
    - [1.3.2 撰寫Javascript](#132-撰寫javascript)
    - [1.3.3 測試結果](#133-測試結果)
  - [1.4 GAS-SQL選擇程式撰寫](#14-gas-sql選擇程式撰寫)
    - [1.4.1 撰寫html模板](#141-撰寫html模板)
    - [1.4.2 撰寫Javascript](#142-撰寫javascript)
    - [1.4.3 測試結果](#143-測試結果)


## 1.3 GAS-SQL簡答程式撰寫

### 1.3.1 撰寫html模板

```html=
<!DOCTYPE html>
<html>
<head>
  <base target="_top">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css" rel="stylesheet"
    integrity="sha384-F3w7mX95PdgyTmZZMECAngseQB83DfGTowi0iMjiWaeVhAn4FJkqJByhZMI3AhiU" crossorigin="anonymous">
</head>

<body>
  <form>
     <div class="mb-3">
      <label for="exampleFormControlInput1" class="form-label">請輸入您要建立的sheet名稱</label>
      <input type="text" class="form-control" id="sheet_name" name="sheet_name" placeholder="請輸入您要建立的sheet名稱">
    </div>
    <button type="submit" class="btn btn-primary mb-3" onclick="google.script.run.withSuccessHandler()
.createForms(this.parentNode);">開始爬蟲</button>
  </form>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.3/jquery.min.js"
    integrity="sha512-STof4xm1wgkfm7heWqFJVn58Hm3EtS31XFaagaa8VMReCXAkQnJZ+jEy8PCC/iT18dFy95WcExNHFTqLyp72eQ=="
    crossorigin="anonymous" referrerpolicy="no-referrer"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/js/bootstrap.bundle.min.js"
    integrity="sha384-/bQdsTh/da6pkI1MST/rWKFNjaCP5gBSY4sEBT38Q/9RBh9AH40zEOg7Hlq2THRZ" crossorigin="anonymous">
  </script>
  <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.10.1/dist/umd/popper.min.js"
    integrity="sha384-W8fXfP3gkOKtndU4JGtKDvXbO53Wy8SZCQHczT5FMiiqmQfUpWbYdTil/SxwZgAN" crossorigin="anonymous">
  </script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/js/bootstrap.min.js"
    integrity="sha384-skAcpIdS7UcVUC05LJ9Dxay8AXcDYfBJqt1CJ85S/CFujBsIzCIv+l9liuYLaMQ/" crossorigin="anonymous">
  </script>
</body>

</html>

```
<!--more-->

### 1.3.2 撰寫Javascript
```javascript
/**
 * 將考題產生器封裝成功能按鈕
 * @param {object} exam 測驗內容(Sheet內容)
 */
function onOpens1() {
  SpreadsheetApp.getUi()
    .createMenu('網路爬蟲-簡答題')
    .addItem('簡答題', 'makeDialog')
    .addToUi();
}
/**
 * 建立對話框內容，由html傳入
 * @param {object} exam 測驗內容(Sheet內容)
 */
function makeDialog() {
  var html = HtmlService.createHtmlOutputFromFile('CreateData');
  var userInterface = HtmlService.createHtmlOutput(html).setWidth(400)
    .setHeight(500);
  SpreadsheetApp.getUi().showModelessDialog(userInterface, '開始爬蟲...先建立個sheet吧!!!');
}

/**
 * 前後端串聯，讀取表單提交的參數，並將參數傳入主程式後執行
 * @param {object} exam 測驗內容(Sheet內容)
 */
function createForms(form) {
  var sheet_name = form.sheet_name;
  //表單驗證，如為空值跳出對話框，且不執行主程式
  if (sheet_name == "") {
    SpreadsheetApp.getUi().alert("選項或文字不得為空值，請重新檢查表單!!!");
  }
  else {
    demoExecuteFunc2(sheet_name);
  }

}

function demoExecuteFunc2(sheet_name) {
  SpreadsheetApp.getUi().alert("爬蟲開始!!!");
  mySheet = createSheet(sheet_name);
  var response = UrlFetchApp.fetch("https://blog.csdn.net/qq_39900031/article/details/119177021");
  //需要加上decodeEntities:false 關閉讀取中文網頁編碼功能,以避免解析時遇到亂碼問題 
  var $ = Cheerio.load(response.getContentText(), { decodeEntities: false });
  writeToSheetDataForHeader(mySheet);
  // 解析並抓取最外層的電影清單表格(div class=release_list) 並只取得release_info_text內電影資訊
  var releaseList = $(".toc li a");
  for (let i = 2; i < releaseList.length; i++) {
    var name = releaseList.eq(i).text();
    writeToSheetData(Object.assign({ name }), mySheet); //將資料寫入google sheets
  }
  SpreadsheetApp.getUi().alert("爬蟲結束!!!");
}

function createSheet(sheetname) {
  //SpreadsheetApp.getUi().alert(sheetname);
  var activeSpreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  var mySheet = activeSpreadsheet.getSheetByName(sheetname);
  if (mySheet != null) {
    activeSpreadsheet.deleteSheet(mySheet);
  }
  mySheet = activeSpreadsheet.insertSheet();
  mySheet.setName(sheetname);
  return mySheet;
}


function writeToSheetDataForHeader(mySheet) {
  mySheet.appendRow(['題型', '題目']);
}

function writeToSheetData(param, mySheet) {
  mySheet.appendRow(['B', param.name]);
}
```

### 1.3.3 測試結果

![](https://markweb.idv.tw/uploads/upload_2c888e837529bad4e6c49013dcebb390.png)

![](https://markweb.idv.tw/uploads/upload_72abf9b8b8ba74b62d5706eeb7727bfb.png)


![](https://markweb.idv.tw/uploads/upload_ddb14206ffd646a2997e5a490ccb452e.png)


![](https://markweb.idv.tw/uploads/upload_dfcb927b5bf7e4704d105772a2a3ddb2.png)


![](https://markweb.idv.tw/uploads/upload_1eb37209e4823074372f92e73b71c24b.png)

## 1.4 GAS-SQL選擇程式撰寫


### 1.4.1 撰寫html模板
```html

<!DOCTYPE html>
<html>
<head>
  <base target="_top">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css" rel="stylesheet"
    integrity="sha384-F3w7mX95PdgyTmZZMECAngseQB83DfGTowi0iMjiWaeVhAn4FJkqJByhZMI3AhiU" crossorigin="anonymous">
</head>

<body>
  <form>
     <div class="mb-3">
      <label for="exampleFormControlInput1" class="form-label">請輸入您要建立的sheet名稱</label>
      <input type="text" class="form-control" id="sheet_name2" name="sheet_name2" placeholder="請輸入您要建立的sheet名稱">
    </div>
    <button type="submit" class="btn btn-primary mb-3" onclick="google.script.run.withSuccessHandler()
.mycreateform(this.parentNode);">開始爬蟲(選擇題)</button>
  </form>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.3/jquery.min.js"
    integrity="sha512-STof4xm1wgkfm7heWqFJVn58Hm3EtS31XFaagaa8VMReCXAkQnJZ+jEy8PCC/iT18dFy95WcExNHFTqLyp72eQ=="
    crossorigin="anonymous" referrerpolicy="no-referrer"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/js/bootstrap.bundle.min.js"
    integrity="sha384-/bQdsTh/da6pkI1MST/rWKFNjaCP5gBSY4sEBT38Q/9RBh9AH40zEOg7Hlq2THRZ" crossorigin="anonymous">
  </script>
  <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.10.1/dist/umd/popper.min.js"
    integrity="sha384-W8fXfP3gkOKtndU4JGtKDvXbO53Wy8SZCQHczT5FMiiqmQfUpWbYdTil/SxwZgAN" crossorigin="anonymous">
  </script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/js/bootstrap.min.js"
    integrity="sha384-skAcpIdS7UcVUC05LJ9Dxay8AXcDYfBJqt1CJ85S/CFujBsIzCIv+l9liuYLaMQ/" crossorigin="anonymous">
  </script>
</body>

</html>

```

### 1.4.2 撰寫Javascript
```javascript
/**
 * 將考題產生器封裝成功能按鈕
 * @param {object} exam 測驗內容(Sheet內容)
 */
function onOpens2() {
  SpreadsheetApp.getUi()
    .createMenu('網路爬蟲-選擇題')
    .addItem('選擇題', 'makeDialogs')
    .addToUi();
}
/**
 * 建立對話框內容，由html傳入
 * @param {object} exam 測驗內容(Sheet內容)
 */
function makeDialogs() {
  var html = HtmlService.createHtmlOutputFromFile('CreateData2');
  var userInterface = HtmlService.createHtmlOutput(html).setWidth(400)
    .setHeight(500);
  SpreadsheetApp.getUi().showModelessDialog(userInterface, '開始爬蟲...先建立個sheet吧!!!');
}

/**
 * 前後端串聯，讀取表單提交的參數，並將參數傳入主程式後執行
 * @param {object} exam 測驗內容(Sheet內容)
 */
function mycreateform(myform) {
  var sheet_name2 = myform.sheet_name2;
  //表單驗證，如為空值跳出對話框，且不執行主程式
  if (sheet_name2 == "") {
    SpreadsheetApp.getUi().alert("選項或文字不得為空值，請重新檢查表單!!!");
  }
  else {
    //SpreadsheetApp.getUi().alert(question_count);
    demoExecuteFunc(sheet_name2);
  }

}


function demoExecuteFunc(sheet_name2) {
   SpreadsheetApp.getUi().alert("開始爬蟲!!!");
  mySheet = onOpen(sheet_name2);
  var response = UrlFetchApp.fetch("https://blog.51cto.com/teayear/5059920");
  //需要加上decodeEntities:false 關閉讀取中文網頁編碼功能,以避免解析時遇到亂碼問題 
  var $ = Cheerio.load(response.getContentText(), { decodeEntities: false });
  writeToSheetDataForHeader2(mySheet);
  var releaseList = $(".main-content table tbody tr");
  for (let i = 1; i < releaseList.length; i++) { // 走訪 tr
    const table_td = releaseList.eq(i).find('td'); // 擷取每個欄位(td)
    const title = table_td.eq(1).text(); // time (台灣時間)
    const optionA = table_td.eq(2).text(); // latitude (緯度)
    const optionB = table_td.eq(3).text(); // longitude (經度)
    const optionC = table_td.eq(4).text(); // magnitude (規模)
    const optionD = table_td.eq(5).text(); // depth (深度)
    const answer = table_td.eq(6).text(); // location (位置)
    let result = answer.includes(",");
    if (result) {
      type = 'C';
    }
    else {
      type = 'A';
    }
    writeToSheetData2(Object.assign({ type, title, answer, optionA, optionB, optionC, optionD }), mySheet);
  }
  SpreadsheetApp.getUi().alert("爬蟲結束!!!");
}

function onOpen(sheet_name2) {
  var activeSpreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  var mySheet = activeSpreadsheet.getSheetByName(sheet_name2);
  if (mySheet != null) {
    activeSpreadsheet.deleteSheet(mySheet);
  }
  mySheet = activeSpreadsheet.insertSheet();
  mySheet.setName(sheet_name2);
  return mySheet;
}

function writeToSheetDataForHeader2(mySheet) {

  mySheet.appendRow(['題型', '題目', '答案', '選項1', '選項2', '選項3', '選項4']);
}

function writeToSheetData2(param, mySheet) {
  mySheet.appendRow([param.type, param.title, param.answer,param.optionA, param.optionB, param.optionC, param.optionD]);
}

```

### 1.4.3 測試結果

![](https://markweb.idv.tw/uploads/upload_d0cff08aff91be9df552977fe1513221.png)

![](https://markweb.idv.tw/uploads/upload_bba6ee405cadfe1704b4e036c70ab096.png)