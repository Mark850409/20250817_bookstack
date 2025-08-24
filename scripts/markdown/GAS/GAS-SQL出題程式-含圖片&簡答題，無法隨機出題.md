---
title: GAS-SQL出題程式-含圖片&簡答題，無法隨機出題
updated: 2024-07-23 13:28:54Z
created: 2023-08-04 08:26:29Z
tags:
  - GAS
---

# 1 GAS-SQL出題程式-含圖片&簡答題，無法隨機出題

## 1.1 簡介
學習如何在GAS撰寫腳本

## 1.2 目錄

- [1 GAS-SQL出題程式-含圖片\&簡答題，無法隨機出題](#1-gas-sql出題程式-含圖片簡答題無法隨機出題)
  - [1.1 簡介](#11-簡介)
  - [1.2 目錄](#12-目錄)
    - [1.2.1 撰寫Javascript](#121-撰寫javascript)
    - [1.2.2 測試結果](#122-測試結果)


### 1.2.1 撰寫Javascript

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
 * 主程式
 */
function main() {
  //使用者設定區塊START
  let url = 'https://docs.google.com/spreadsheets/d/17J4_ikeIc2bRUHXpt5sS5zAzGwIwPA7D3yrVMwDBXxo/edit#gid=0'; //試算表網址
  let questionSize = 20; //匯入題目數
  let optionLength = 7; //選項數量
  let sheetCount = 0 //第幾個sheet
  //使用者設定區塊END
  let exam = GetSheet(url, questionSize, optionLength, sheetCount);
  GenerateExam(exam, questionSize);
}


/**
 * 轉換試算表內容為測驗Object
 * @param {string} url 試算表網址
 * @param {int} questionSize 匯入題目數量
 */
function GetSheet(url, questionSize, optionLength, sheetCount) {
  let exam = {};
  exam.url = url;
  exam.size = questionSize;
  let questions = [];
  let SpreadSheet = SpreadsheetApp.openByUrl(exam.url);

  let sheet = SpreadSheet.getSheets()[sheetCount];
  let name = sheet.getSheetName();
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
        console.log(item);
        if (item = "A") {
          item = "1";
        }
        else if (item = "B") {
          item = "2";
        }
        else if (item = "C") {
          item = "3";
        }
        else if (item = "D") {
          item = "4";
        }
        else if (item = "E") {
          item = "5";
        }
        else if (item = "F") {
          item = "6";
        }
        else if (item = "G") {
          item = "7";
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
      //題目圖片ID(第  欄)
      question.imgurl = sheet.getRange(i, 11, 1, 1).getValue();
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
function GenerateExam(exam, questionSize) {
  let form = FormApp.create(exam.name);
  let formID = form.getId();
  form.setIsQuiz(true);
  AddExamineeInfo(form);
  let questions = exam.questions;
  let count = 0;
  for (let i = 0; i < questions.length; i++) {
    if (questions[i].type == 'A') {
      //計算選項A的筆數
      count++;
      //建立單選題
      AddChoiceItem(form, questions[i], questionSize);
    } else if (questions[i].type == 'B') {
      //將區段放置最後 題選項A的後面
      if (i == count + 1) {
        form.addPageBreakItem().setTitle('SQL基本簡答題').setHelpText('1.資料結構表請參考以下連結：https://script.google.com/macros/s/AKfycbx_bkzd8IUdaXS04QY9xedT9i0t1JU5uAcbXHSgvA-0mrXQqEmub4rZ0hmUtHwmBQ0P/exec\n2.資料庫語法操作請參考以下連結：https://markweb.idv.tw:4443/phpmyadmin/\n3.以下題目將使用到[school]的資料庫，相關資料結構及操作請參考步驟1、2的連結說明');
      }
      //建立簡答題
      AddTxtItem(form, questions[i], questionSize);

    } else if (questions[i].type == 'C') {
      //建立多選題
      AddChoiceItem(form, questions[i], questionSize);
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
  Logger.log("done.");
}

/**
 * 增加選擇題
 * @param {object} form 表單主體
 * @param {object} question 選擇題題目(Sheet內容)
 */
function AddChoiceItem(form, question, questionSize) {
  let options = question.options;

  //題目是否有圖片
  if (question.imgurl.length > 0) {
    AddImageItem(form, question.imgurl, question.description);
  }
  //選項A為單選，其餘為複選
  if (question.type == 'A') {
    item = form.addMultipleChoiceItem();
  } else {
    item = form.addCheckboxItem();
  }
  //考慮圖片是否已加題目說明
  if (question.imgurl.length > 0) {
    let description = "A：承上題，您的答案是..."
    item.setTitle(description);
  }
  else {
    item.setTitle(question.description);
  }
  //設定題目配分
  item.setPoints(100 / questionSize);
  //設定必填
  item.setRequired(true);

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


/**
 * 增加簡答題 - 無法設定解答，需手動調整表單
 * @param {object} form 表單主體
 * @param {object} question 簡答題題目(Sheet內容)
 */
function AddTxtItem(form, question, questionSize) {
  let item = form.addTextItem();
  item.setPoints(100 / questionSize);
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

<!--more-->

### 1.2.2 測試結果

![](https://markweb.idv.tw/uploads/upload_04de48d4736b57997de6407d17835743.png)


![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/6da6d9e4-upload-4c26ea23872e062669026e2d979b7a7c.png)