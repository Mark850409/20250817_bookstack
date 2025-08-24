---
title: GAS-SQL出題程式-隨機單選題
updated: 2024-07-23 13:28:49Z
created: 2023-08-04 08:26:29Z
tags:
  - GAS
---

# 1 GAS-SQL出題程式-隨機單選題

## 1.1 簡介
學習如何在GAS撰寫腳本

## 1.2 目錄

- [1 GAS-SQL出題程式-隨機單選題](#1-gas-sql出題程式-隨機單選題)
  - [1.1 簡介](#11-簡介)
  - [1.2 目錄](#12-目錄)
    - [1.2.1 撰寫選單對話框模板](#121-撰寫選單對話框模板)
    - [1.2.2 撰寫Javascript](#122-撰寫javascript)
    - [1.2.3 測試結果](#123-測試結果)


### 1.2.1 撰寫選單對話框模板

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
      <label for="exampleFormControlInput1" class="form-label">請輸入考題名稱?</label>
      <input type="text" class="form-control" id="quiz_name" name="quiz_name" placeholder="請輸入考題名稱">
    </div>
    <div class="mb-3">
      <label for="exampleFormControlInput1" class="form-label">請輸入出題數量?</label>
      <input type="text" class="form-control" id="question_count" name="question_count" placeholder="請輸入出題數量">
    </div>
    <div class="mb-3">
      <label for="exampleFormControlInput1" class="form-label">請輸入選項數量?</label>
      <input type="text" class="form-control" id="option_count" name="option_count" placeholder="請輸入選項數量">
    </div>
    <div class="mb-3">
      <label for="exampleFormControlInput1" class="form-label">請選擇問題題目是否隨機出題?</label>
      <select class="form-select" id="question_randon" name="question_randon" aria-label="Default select example">
          <option selected>請選擇...</option>
          <option value="0">否</option>
          <option value="1">是</option>
        </select>
    </div>
    <div class="mb-3">
      <label for="exampleFormControlInput1" class="form-label">請選擇問題選項是否隨機出題?</label>
      <select class="form-select" id="option_randon" name="option_randon" aria-label="Default select example">
              <option selected>請選擇...</option>
              <option value="0">否</option>
              <option value="1">是</option>
          </select>
    </div>
    <button type="submit" class="btn btn-primary mb-3" onclick="google.script.run.withSuccessHandler()
.createForms(this.parentNode);">開始建立SQL考題</button>
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

### 1.2.2 撰寫Javascript
```javascript
/**
 * 判斷資料夾是否存在
 */
function folderExists(foldername, parentFolder) {
  let folders;
  if (parentFolder) {
    folders = parentFolder.getFoldersByName(foldername);//only looks at immediate sub folder
  } else {
    folders = DriveApp.getFoldersByName(foldername);//looks on entire drive
  }
  let fA = [];
  while (folders.hasNext()) {
    let folder = folders.next();
    fA.push(folder.getId())
  }
  return fA.length > 0 ? true : false;
}


/**
 * 刪除資料夾所有檔案
 */
function deleteFolder(folderName) {
  if (folderName === undefined) {
    folderName = "Test"
  };

  var folderToDelete = DriveApp.getFoldersByName(folderName).next();
  var returnedFolder = folderToDelete.setTrashed(true);
  Logger.log('returnedFolder is trashed: ' + returnedFolder.isTrashed());
};

/**
 * 在指定目錄下建立子目錄並將問卷搬移至子目錄下
 * @param {object} exam 測驗內容(Sheet內容)
 */

function createFolderAndMoveFile(parentFolderID, formID) {
  var parentFolder = DriveApp.getFolderById(parentFolderID);
  var getCurrentDate = Utilities.formatDate(new Date(), "GMT+8", "yyyyMMdd");
  if (folderExists(getCurrentDate, parentFolder)) {
    deleteFolder(getCurrentDate);
    var createFolder1 = DriveApp.createFolder(getCurrentDate).moveTo(parentFolder);
    DriveApp.getFileById(formID).moveTo(createFolder1);
  }
  else {
    var createFolder1 = DriveApp.createFolder(getCurrentDate).moveTo(parentFolder);
    DriveApp.getFileById(formID).moveTo(createFolder1);
  }
}

/**
 * 將考題產生器封裝成功能按鈕
 * @param {object} exam 測驗內容(Sheet內容)
 */
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('建立SQL考題')
    .addItem('點選建立SQL考題', 'makeDialog')
    .addToUi();
}
/**
 * 建立對話框內容，由html傳入
 * @param {object} exam 測驗內容(Sheet內容)
 */
function makeDialog() {
  var html = HtmlService.createHtmlOutputFromFile('makeSQLQuiz');
  var userInterface = HtmlService.createHtmlOutput(html).setWidth(400)
    .setHeight(500);
  SpreadsheetApp.getUi().showModelessDialog(userInterface, '考題產生器...');
}

/**
 * 前後端串聯，讀取表單提交的參數，並將參數傳入主程式後執行
 * @param {object} exam 測驗內容(Sheet內容)
 */
function createForms(form) {
  var quiz_name = form.quiz_name;
  var question_count = form.question_count;
  var option_count = form.option_count;
  var question_randon = form.question_randon;
  var option_randon = form.option_randon;
  // SpreadsheetApp.getUi().alert("出題數量"+question_count+"-"+"選項數量"+option_count+"-"+"隨機問題"+question_randon+"-"+"隨機選項"+option_randon);

  //表單驗證，如為空值跳出對話框，且不執行主程式
  if (quiz_name == "" || question_count == "" || option_count == "" || question_randon == "" || option_randon == "") {
    SpreadsheetApp.getUi().alert("選項或文字不得為空值，請重新檢查表單!!!");
  }
  else {
    //SpreadsheetApp.getUi().alert(question_count);
    main(quiz_name, question_count, option_count, question_randon, option_randon);
  }

}

/**
 * 主程式
 */
function main(quiz_name, question_count, option_count, question_randon, option_randon) {
  SpreadsheetApp.getUi().alert("開始傳入設定參數...");
  //使用者設定區塊START
  let url = 'https://docs.google.com/spreadsheets/d/1vWB1Cu7DspNsXFmf1UwHkbSUeeQJ95t16jauGOm1Kxs/edit#gid=0'; //試算表網址
  let questionSize = Number(question_count); //匯入題目數
  //console.log(questionSize);
  //SpreadsheetApp.getUi().alert("main="+questionSize);
  let optionLength = Number(option_count); //選項數量
  let sheetCount = 0 //第幾個sheet
  let ran_num_question = Number(question_randon);//0為正常出題，1為隨機亂數
  let ran_num_answer = Number(option_randon);//0為正常出題，1為隨機亂數
  //使用者設定區塊END
  let exam = GetSheet(url, questionSize, optionLength, sheetCount, quiz_name,ran_num_question, ran_num_answer);
  GenerateExam(exam, questionSize, ran_num_question, ran_num_answer);
}


/**
 * 轉換試算表內容為測驗Object
 * @param {string} url 試算表網址
 * @param {int} questionSize 匯入題目數量
 */
function GetSheet(url, questionSize, optionLength, sheetCount, quiz_name,ran_num_question, ran_num_answer) {
  SpreadsheetApp.getUi().alert("開始讀取題目列表...");
  //SpreadsheetApp.getUi().alert("GetSheet="+questionSize);
  let exam = {};
  exam.url = url;
  exam.size = questionSize;
  let questions = [];
  let SpreadSheet = SpreadsheetApp.openByUrl(exam.url);

  let sheet = SpreadSheet.getSheets()[sheetCount];
  let name = quiz_name;
  exam.name = name;

  //從試算表第 列開始取N(題目數量)列
  for (let i = 2; i < exam.size + 2; i++) {
    question = {};
    if (!sheet.getRange(i, 1).isBlank()) {
      //題目類型(第 欄)
      question.type = sheet.getSheetValues(i, 1, 1, 1);
      //題目(第 欄)
      question.description = sheet.getSheetValues(i, 2, 1, 1);
      //正確答案(第 欄)
      question.answer = sheet.getSheetValues(i, 3, 1, 1).toString().split(',').map(function (item) {
        // console.log(item);
        if (item == 'A') {
          item = 1;
        }
        else if (item  == 'B') {
          item = 2;
        }
        else if (item == 'C') {
          item = 3;
        }
        else if (item == 'D') {
          item = 4;
        }
        return parseInt(item, 10);
      });

      let options = [];

      //選項, 第 欄位之後
      for (let j = 4; j < (4 + optionLength); j++) {
        if (!sheet.getRange(i, j).isBlank()) {
          let option = sheet.getSheetValues(i, j, 1, 1);
          options.push(option);
        }
      }
      question.options = options;
      questions.push(question);
    }

  }
  exam.questions = questions;

  return exam;
}

/**
 * 產出測驗表單
 * @param {object} exam 測驗內容(Sheet內容)
 */
function GenerateExam(exam, questionSize, ran_num_question, ran_num_answer) {
  SpreadsheetApp.getUi().alert("開始建立考題...大約兩分鐘!!!");
  // SpreadsheetApp.getUi().alert("GenerateExam="+questionSize);
  let form = FormApp.create(exam.name);
  let formID = form.getId();
  let questions = [];
  form.setIsQuiz(true);
  AddExamineeInfo(form);
  if (ran_num_question > 0) {
    questions = shuffleArray(exam.questions);
  }
  else {
    questions = exam.questions;
  }

  let count = 0;
  for (let i = 0; i < questions.length; i++) {

    if (questions[i].type == 'A') {
      //計算選項A的筆數
      count++;
      //建立單選題
      AddChoiceItem(form, questions[i], questionSize, ran_num_answer);
    } else if (questions[i].type == 'B') {
      //將區段放置最後 題選項A的後面
      if (i == count + 1) {
        form.addPageBreakItem().setTitle('SQL基本簡答題').setHelpText('1.資料結構表請參考以下連結：https://script.google.com/macros/s/AKfycbx_bkzd8IUdaXS04QY9xedT9i0t1JU5uAcbXHSgvA-0mrXQqEmub4rZ0hmUtHwmBQ0P/exec\n2.資料庫語法操作請參考以下連結：https://markweb.idv.tw:4443/phpmyadmin/\n3.以下題目將使用到[school]的資料庫，相關資料結構及操作請參考步驟1、2的連結說明');
      }
      //建立簡答題
      AddTxtItem(form, questions[i], questionSize);

    } else if (questions[i].type == 'C') {
      //建立多選題
      AddChoiceItem(form, questions[i], questionSize, ran_num_answer);
    }
    else if (questions[i].type == 'D') {
      //建立日期時間
      AddDateTime(form, questions[i]);
    }
    else if (questions[i].type == 'E') {
      //建立詳答題
      AddParagraphItem(form, questions[i]);
    }
    else {
      Logger.log('請確認A欄的值並重新執行')
    }
  }
  //建立今天日期目錄並將問卷移動到此目錄下
  createFolderAndMoveFile('1Y88w15ZPaw43WdG4OeqfCntgqBsFKkSf', formID);
  SpreadsheetApp.getUi().alert("SQL考題建立成功.");
}

/**
 * 增加選擇題
 * @param {object} form 表單主體
 * @param {object} question 選擇題題目(Sheet內容)
 */
function AddChoiceItem(form, question, questionSize, ran_num_answer) {
  //SpreadsheetApp.getUi().alert("AddChoiceItem="+questionSize);
  let options = [];
  let answer = [];
  //判斷是否為亂數選項
  if (ran_num_answer > 0) {
    options = shuffleArray(question.options);
  }
  else {
    options = question.options;
  }

  //選項A為單選，其餘為複選
  if (question.type == 'A') {
    item = form.addMultipleChoiceItem();
  } else {
    item = form.addCheckboxItem();
  }

  //設定題目配分
  item.setPoints(parseInt((100/questionSize),10));
  //設定必填
  item.setRequired(true);
  //設定問題
  item.setTitle(question.description);

  let choices = [];
  for (let j = 0; j < options.length; j++) {
    if (question.answer.indexOf(j + 1) > -1) {
      choices.push(item.createChoice(options[j], true));
    } else {
      choices.push(item.createChoice(options[j], false));
    }
  }
  item.setChoices(choices);
}


//陣列亂數
function shuffleArray(array) {
  var i, j, temp;
  for (i = array.length - 1; i > 0; i--) {
    j = Math.floor(Math.random() * (i + 1));
    temp = array[i];
    array[i] = array[j];
    array[j] = temp;
  }
  return array;
}

/**
 * 增加簡答題 - 無法設定解答，需手動調整表單
 * @param {object} form 表單主體
 * @param {object} question 簡答題題目(Sheet內容)
 */
function AddTxtItem(form, question, questionSize) {
  let item = form.addTextItem();
  item.setPoints(parseInt((100/questionSize),10));
  item.setTitle(question.description);
  item.setRequired(true);
}

/**
 * 增加考生基本資料簡答區
 * @param {object} form 表單主體
 */
function AddExamineeInfo(form) {
  let item1 = form.addTextItem();
  item1.setTitle('請輸入您的姓名,例如：王大明');
  item1.setRequired(true);
  //將區段 、區段 分開
  form.addPageBreakItem().setTitle('SQL基本選擇題').setHelpText('1.SQL基礎語法可參考以下連結:https://www.1keydata.com/tw/sql/sql.html\n2.可以讓妳OPENBOOK但請不要猜題阿!!!');
}

/**
 * 增加考生圖片區
 * @param {object} form 表單主體
 */
function AddImageItem(form, imageID, description) {
  var img = DriveApp.getFileById(imageID);
  var blob = img.getBlob();
  form.addImageItem()
    .setTitle("Q：" + description)
    .setImage(blob);

}

/**
 * 增加詳答題 - 無法設定解答，需手動調整表單
 * @param {object} form 表單主體
 * @param {object} question 詳答題題目(Sheet內容)
 */
function AddParagraphItem(form, question) {
  let item = form.addParagraphTextItem();
  item.setTitle(question.description);
  item.setRequired(true);
}

/**
 * 增加日期區
 * @param {object} form 表單主體
 */
function AddDateTime(form, question) {
  let item = form.addDateTimeItem();
  item.setTitle(question.description);
  item.setRequired(true);
}

```

### 1.2.3 測試結果

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/wb14daba040-upload-d46cb5c33115959f325d05ce59464c24.png)


![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/DlP5aecdb00-upload-780b642dacbb9a20485102369a7fc0c2.png)

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/2104db31-upload-0840ae360a1e637f5dbd8bcde1f21d01.png)

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/cab592be-upload-d2a6e6318202d29f8e0238077fad692e.png)


![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/EoG0d748e6c-upload-999bad05fafa6df1d53d01e7ec0b065b.png)


![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/qZDd93d456c-upload-e669d262f18f2b324f171065ee860f28.png)


![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/9558afbd-upload-17b0936d8fe966a3b2e047376ad2bbde.png)


![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/l0b6e6490b8-upload-2437e206389982474364da558e93ed24.png)