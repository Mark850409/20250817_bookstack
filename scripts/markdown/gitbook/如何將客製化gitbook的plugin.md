---
title: 如何將客製化gitbook的plugin
updated: 2024-07-23 13:31:33Z
created: 2024-07-14 07:33:37Z
latitude: 25.0329694
longitude: 121.5654177
altitude: 0
tags:
  - Gitbook
  - NPM
---

# 1 如何將客製化gitbook的plugin

## 1.1 簡介
自己做出屬於自己風格的`npm package`，並打包上傳至`npm`

## 1.2 專案架構

```
GitbookCustomPlugin
├─ assets
│  ├─ lib
│  │  └─ plugin.js
│  └─ style
│     └─ plugin.css
├─ doc
│  └─ images
│     └─ gitbook-plugin-page-footer-ex-demo.jpg
├─ index.js
├─ LICENSE
├─ package.json
└─ README.md

```

## 1.3 目錄

- [1 如何將客製化gitbook的plugin](#1-如何將客製化gitbook的plugin)
  - [1.1 簡介](#11-簡介)
  - [1.2 專案架構](#12-專案架構)
  - [1.3 目錄](#13-目錄)
  - [1.4 事前準備](#14-事前準備)
  - [1.5 操作步驟](#15-操作步驟)
    - [1.5.1 登入NPM](#151-登入npm)
    - [1.5.2 部署到NPM](#152-部署到npm)
  - [1.6 完成畫面](#16-完成畫面)


## 1.4 事前準備

請拿Github大神的專案模改即可

https://github.com/zq99299/gitbook-plugin-page-footer-ex/tree/master


> [!note] 小提示 
>1. 首先先說明 下如果要使用**gitlab npm registry**的話，gitlab對於 **package name**名稱是有限制的
>* package name  定要是 @{scope}/ 開頭
>* 如果是 group project 那 {scope} 便是 group name
>* 而如果是 personal project 那 {scope} 便是 user name
>* 而斜線後面的名字則沒有強制規定要跟 repo 名稱相同
>2. 必填參數如下:
>* name：請按照上述格式
>* version：版號也請記得要手動更新，且不能夠重複
>* description：增加專案描述
>* repository：若是自架gitlab，請放置自訂倉庫位址
>* homepage：請指向README.MD的文件

```json
{
  "name": "gitbook-plugin-mycustompage-footer-ex",
  "version": "1.0.2",
  "description": "定義每篇文章的footer，可以增加版權宣告及修改時間，並加入時區(使用GMT+8)",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "repository": {
    "type": "git",
    "url": "git+https://markweb.idv.tw:10443/gitbooknpmproject/gitbook-plugin-mycustom-footer-ex.git"
  },
  "author": "markhsu",
  "license": "GPL-3.0",
  "bugs": {
    "url": "https://markweb.idv.tw:10443/gitbooknpmproject/gitbook-plugin-mycustom-footer-ex/issues"
  },
  "homepage": "https://markweb.idv.tw:10443/gitbooknpmproject/gitbook-plugin-mycustom-footer-ex#readme",
  "dependencies": {
    "moment": "^2.10.6"
  },
  "engines": {
    "gitbook": ">=3.0.0"
  },
  "gitbook": {
    "properties": {
      "copyright": {
        "type": "string",
        "default": "© All Rights Reserved",
        "title": "你的版權宣告",
        "description": "The left-aligned text in the footer."
      },
      "markdown": {
        "type": "boolean",
        "default": false,
        "title": "是否支持Markdown格式",
        "description": "True if copyright and update_label are in Markdown, false if plain text or HTML."
      },
      "update_label": {
        "type": "string",
        "default": "updated",
        "title": "文件更新時間",
        "description": "Text before date."
      },
      "update_format": {
        "type": "string",
        "default": "YYYY-MM-DD HH:mm:ss",
        "title": "時間格式",
        "description": "Moment.js date format."
      }
    }
  }
}

```

請修改`assets\lib\plugins.js`，進行時間格式調整

```javascript
// 引入 moment-timezone 模組
var moment = require('moment-timezone');

module.exports = function(book, page) {
    /**
     * 在 package.json 中配置的默认值，这里可以直接使用
     * [config: config option]
     * @type {Object}
     */
    var config = book.config.get('pluginsConfig')['mycustompage-footer-ex'];

    var wrapIfMarkdown = function(input) {
        if (!config.markdown) {
            return input;
        } else {
            return book.renderInline('markdown', input);
        }
    };

    // 使用 Promise.all 確保所有異步操作完成後再處理結果
    return Promise.all([wrapIfMarkdown(config.copyright), wrapIfMarkdown(config.update_label)])
        .then(function(labels) {
            var copyright = labels[0];
            var updateLabel = labels[1];

            // 使用 moment-timezone 轉換日期時間到 GMT+8
            // 檢查 page.file 和 page.file.mtime 是否存在
            var mtime = page.file && page.file.mtime ? moment(page.file.mtime).tz('Asia/Taipei') : moment().tz('Asia/Taipei');

            // 格式化日期時間
            var formattedTime = mtime.format(config.update_format);

            // 構建 footer HTML
            page.content += '\n\n' + [
                '<footer class="page-footer-ex">',
                    '<span class="page-footer-ex-copyright">',
                        copyright,
                    '</span>',
                    '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;',
                    '<span class="page-footer-ex-footer-update">',
                        updateLabel,
                        formattedTime,
                    '</span>',
                '</footer>'
            ].join(' ');

            return page;
        });
};

```

## 1.5 操作步驟

1. 請先將專案推送到`gitlab`或是`github`

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/fff1dcc0-202407141547355.png)

2. 登入並部署到NPM

<!--more-->

### 1.5.1 登入NPM

```
npm login
```

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/ef49d759-202407141542345.png)


### 1.5.2 部署到NPM
```
npm publish
```

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/b594f3a7-202407141544484.png)


## 1.6 完成畫面

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/kNC56aa7160-202407141546043.png)