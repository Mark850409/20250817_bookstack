---
title: GAS-作業上傳腳本
updated: 2024-07-23 13:28:43Z
created: 2023-08-04 08:26:29Z
tags:
  - GAS
---

# 1 GAS-作業上傳腳本

## 1.1 簡介
學習如何在GAS撰寫腳本

## 1.2 目錄

- [1 GAS-作業上傳腳本](#1-gas-作業上傳腳本)
  - [1.1 簡介](#11-簡介)
  - [1.2 目錄](#12-目錄)
    - [1.2.1 撰寫html模板](#121-撰寫html模板)
    - [1.2.2 撰寫Javascript](#122-撰寫javascript)
    - [1.2.3 測試結果](#123-測試結果)


### 1.2.1 撰寫html模板
```html
<!DOCTYPE html>
<html lang="en" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:v="urn:schemas-microsoft-com:vml">
<head>
  <title></title>
  <meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
  <meta content="width=device-width, initial-scale=1.0" name="viewport" />
  <!--[if mso]><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch><o:AllowPNG/></o:OfficeDocumentSettings></xml><![endif]-->
  <style>
    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      padding: 0;
    }

    a[x-apple-data-detectors] {
      color: inherit !important;
      text-decoration: inherit !important;
    }

    #MessageViewBody a {
      color: inherit;
      text-decoration: none;
    }

    p {
      line-height: inherit
    }

    .desktop_hide,
    .desktop_hide table {
      mso-hide: all;
      display: none;
      max-height: 0px;
      overflow: hidden;
    }

    @media (max-width:520px) {
      .desktop_hide table.icons-inner {
        display: inline-block !important;
      }

      .icons-inner {
        text-align: center;
      }

      .icons-inner td {
        margin: 0 auto;
      }

      .row-content {
        width: 100% !important;
      }

      .mobile_hide {
        display: none;
      }

      .stack .column {
        width: 100%;
        display: block;
      }

      .mobile_hide {
        min-height: 0;
        max-height: 0;
        max-width: 0;
        overflow: hidden;
        font-size: 0px;
      }

      .desktop_hide,
      .desktop_hide table {
        display: table !important;
        max-height: none !important;
      }
    }
  </style>
</head>

<body style="background-color: #FFFFFF; margin: 0; padding: 0; -webkit-text-size-adjust: none; text-size-adjust: none;">
  <table border="0" cellpadding="0" cellspacing="0" class="nl-container" role="presentation"
    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #FFFFFF;" width="100%">
    <tbody>
      <tr>
        <td>
          <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-1" role="presentation"
            style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
            <tbody>
              <tr>
                <td>
                  <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 500px;" width="500">
                    <tbody>
                      <tr>
                        <td class="column column-1"
                          style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
                          width="100%">
                          <table border="0" cellpadding="0" cellspacing="0" class="heading_block block-1"
                            role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
                            <tr>
                              <td class="pad" style="text-align:center;width:100%;">
                                <h1
                                  style="margin: 0; color: #555555; direction: ltr; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; font-size: 23px; font-weight: 700; letter-spacing: normal; line-height: 120%; text-align: center; margin-top: 0; margin-bottom: 0;">
                                  <span class="tinyMce-placeholder">[作業上傳] 檔案區</span></h1>
                              </td>
                            </tr>
                          </table>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </td>
              </tr>
            </tbody>
          </table>
          <table align="center" border="0" cellpadding="0" cellspacing="0" class="row row-2" role="presentation"
            style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
            <tbody>
              <tr>
                <td>
                  <table align="center" border="0" cellpadding="0" cellspacing="0" class="row-content stack"
                    role="presentation"
                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 500px;" width="500">
                    <tbody>
                      <tr>
                        <td class="column column-1"
                          style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;"
                          width="100%">
                          <table border="0" cellpadding="10" cellspacing="0" class="divider_block block-1"
                            role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
                            <tr>
                              <td class="pad">
                                <div align="center" class="alignment">
                                  <table border="0" cellpadding="0" cellspacing="0" role="presentation"
                                    style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;" width="100%">
                                    <tr>
                                      <td class="divider_inner"
                                        style="font-size: 1px; line-height: 1px; border-top: solid 1px #dddddd;">
                                        <span> </span></td>
                                    </tr>
                                  </table>
                                </div>
                              </td>
                            </tr>
                          </table>
                          <table border="0" cellpadding="10" cellspacing="0" class="paragraph_block block-2"
                            role="presentation"
                            style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
                            <tr>
                              <td class="pad">
                                <div
                                  style="color:#101112;font-size:16px;font-family:Arial, Helvetica Neue, Helvetica, sans-serif;font-weight:400;line-height:120%;text-align:left;direction:ltr;letter-spacing:0px;mso-line-height-alt:19.2px;">
                                  <p style="margin: 0; margin-bottom: 16px;font-size:14px;">姓名：<?=name?></p>
                                  <p style="margin: 0; margin-bottom: 16px;font-size:14px;">主旨：<?=subject?></p>
                                  <p style="margin: 0; margin-bottom: 16px;font-size:14px;">電子郵件：<?=email?></p><span id="people"></span>
                                   <p style="margin: 0; margin-bottom: 16px;font-size:14px;">作業連結:<?=homework?></p><span id="people"></span>
                                </div>
                              </td>
                            </tr>
                          </table>
                          <table border="0" cellpadding="10" cellspacing="0" class="paragraph_block block-3"
                            role="presentation"
                            style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;" width="100%">
                            <tr>
                              <td class="pad">
                                <div
                                  style="color:#101112;font-size:16px;font-family:Arial, Helvetica Neue, Helvetica, sans-serif;font-weight:400;line-height:120%;text-align:center;direction:ltr;letter-spacing:0px;mso-line-height-alt:19.2px;">
                                  <p style="margin: 0;">Copyright © 2023 MarkWebSite [All rights reserved].</p>
                                </div>
                              </td>
                            </tr>
                          </table>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </td>
              </tr>
            </tbody>
          </table>
        </td>
      </tr>
    </tbody>
  </table><!-- End -->
</body>

</html>
```

<!--more-->

### 1.2.2 撰寫Javascript

```javascript
/**
 * 建立全域變數
 */

//輸入自己 LINE BOT 的 channel_access_token
var CHANNEL_ACCESS_TOKEN = '' 
//專屬於你的User ID
var userid = ''; 
//Line 貼圖分類編號
var stickerPackageId = 11537;
//Line 貼圖編號  
var stickerId = 52002735; 
//Line 表情分類編號        
var productId = '238';
//Line 表情編號
var emojiId = '009';


/**
 * 取得檔案上傳的ID
 */
function getIdSheetFromUrl(url) {
  var id = url.split('id=')[1];
  if (!id) {
    id = url.split('/d/')[1];
    id = id.split('/edit')[0]; // here we have the id
  }
  return id;
}

/**
 * 取得指定資料夾ID
 */
function getFolderByName(folderName) {
  var folders = DriveApp.getFoldersByName(folderName);
  var folderID = null;
  if (folders.hasNext())
    folderID = folders.next();
  return folderID;
}

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
 * 建立資料夾並將上傳的檔案移至指定目錄
 */
function createFolderandAddFile(url, email, output, cc, subject, name) {
  var parentFolder = DriveApp.getFolderById("1r0w5udCtTA51-oSvmYaFPvy2N-UJwp85t6P972dk0jlCRCyUufjgLQCtBnlSRPudqLcgVJBB");
  var urls = url.toString().split(",");
  var getCurrentDate = Utilities.formatDate(new Date(), "GMT+8", "yyyyMMdd");
  if (folderExists(getCurrentDate, parentFolder)) {
    deleteFolder(getCurrentDate);
    getattachmentandSendemail(urls, email, output, cc, subject, getCurrentDate, parentFolder, name);
  }
  else {
    getattachmentandSendemail(urls, email, output, cc, subject, getCurrentDate, parentFolder, name);

  }
}

/**
 * 將���錄下所有檔案夾帶附檔寄出
 */
function getattachmentandSendemail(urls, email, output, cc, subject, getCurrentDate, parentFolder, name) {
  var fileID = [];
  //將今天日期的目錄建立後移到指定根目錄下
  var createFolder1 = DriveApp.createFolder(getCurrentDate).moveTo(parentFolder);
  //取得所有圖檔的URL並轉換為ID存入陣列
  for (i = 0; i < urls.length; i++) {
    fileID.push(getIdSheetFromUrl(urls[i]));
  }
  //取得所有圖檔的ID並將圖檔移到今天日期目錄下
  for (i = 0; i < fileID.length; i++) {
    DriveApp.getFileById(fileID[i]).moveTo(createFolder1);
  }
  //取得今天日期目錄下所有檔案
  var contents = getFolderByName(getCurrentDate).getFiles();
  var attachments = [];
  //將檔案寫入陣列裡
  while (contents.hasNext()) {
    var file = contents.next();
    attachments.push(file);
    //清空陣列，避免附檔重複上傳...
    attachments=[];
  }
  //將信件寄出
  MailApp.sendEmail({
    to: email,
    cc: cc,
    subject: subject + " - " + name,
    htmlBody: output,
    attachments: attachments
  });

}

/**
 * 主程式跑的地方(main)
 */

//當網頁有Post請求時就會依據網址來執行這doPost
function doPost(e) {  
  //將事件(e)內的文字訊息解析出來
   //msg內部存放著全部LINE事件產生的全部訊息
  var msg = JSON.parse(e.postData.contents); 
   //replyToken是每個能夠reply的事件 定會附屬的令牌
  var replyToken = msg.events[0].replyToken; 
  //解析使用者傳出的訊息內容
  var userMessage = msg.events[0].message.text; 
  //專屬於你的User ID
  var userid = msg.events[0].source.userId; 
  //使用reply_message這function來回覆訊息
  //reply_message(replyToken,userid); 

  //請先取得userID
  push_message_userid("您的userID是:" + userid, userid);

}

/**
 * 這是對於訊息發送的程式碼
 */
function push_message_userid(reply, userid) {
  UrlFetchApp.fetch('https://api.line.me/v2/bot/message/multicast', {
    'headers': {
      'Content-Type': 'application/json; charset=UTF-8',
      'Authorization': 'Bearer ' + CHANNEL_ACCESS_TOKEN,
    },
    'method': 'post',
    'payload': JSON.stringify({
      'to': [userid],
      'messages': [{
        'type': 'text', 'text': reply
      }]
    }),
  });
}

/**
 * 取得問卷所有欄位資料
 */
function onSubmit(datas) {

  // 取得提交的值（你的欄位名稱可能與我不同）
  var data = datas.namedValues;
  var name = data['姓名'][0];
  var email = data['電子郵件'][0];
  var subject = data['主旨'][0];
  var cc = data['副本'][0];
  var homework = data['作業檔案上傳'][0];


  // 取得上傳的 HTML 檔
  var edmHTML = HtmlService.createTemplateFromFile('homework_template');

  // 設定HTML的資料
  edmHTML.name = name;
  edmHTML.email = email;
  edmHTML.subject = subject;
  edmHTML.homework = homework;


  // 產出成要發送的 HTML
  var output = edmHTML.evaluate().getContent();

  // 建立資料夾並將上傳的檔案移至指定目錄
  createFolderandAddFile(homework, email, output, cc, subject, name);

}
```

### 1.2.3 測試結果

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/b34600c7-upload-d6148acf16c1629b59bf89513a04c644.png)


![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/d4dd5073-upload-c8754040d91e36a3a3aa04aa07e177b4.png)


![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/pyJ35a91819-upload-fc332fcde09b82fa04c9a99c87392011.png)


![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/NMzdf0cce56-upload-6c8eac8df8dc5b90b0005fd0f3f4c106.png)


![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/wCA3e2bc82f-upload-d979785bad8d92db8ac6230290aab2bd.png)