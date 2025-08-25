---
title: 如何客製化自己的主題並打包放到npm平台
updated: 2024-07-24 08:09:41Z
created: 2024-02-05 13:57:21Z
latitude: 25.0329694
longitude: 121.5654177
altitude: 0
tags:
  - NPM
  - Custom
  - Theme
---

# 1 如何客製化自己的主題並打包放到npm平台

## 1.1 簡介
自己做出屬於自己風格的gitbook主題，並打包上傳至npm

## 1.2 專案架構
```
pushpublicnpm
├─ .gitignore
├─ .npmignore
├─ .npmrc
├─ index.js
├─ LICENSE
├─ logo.png
├─ package.json
├─ README.md
├─ _assets
│  ├─ fexa.css
│  ├─ fexa.js
│  └─ logo.png
└─ _layouts
   └─ website
      └─ page.html
```

## 1.3 目錄

- [1 如何客製化自己的主題並打包放到npm平台](#1-如何客製化自己的主題並打包放到npm平台)
  - [1.1 簡介](#11-簡介)
  - [1.2 專案架構](#12-專案架構)
  - [1.3 目錄](#13-目錄)
    - [1.3.1 事前準備](#131-事前準備)
    - [1.3.2 操作步驟](#132-操作步驟)


### 1.3.1 事前準備
1. 請先至npm官網註冊帳號，連結如下
https://www.npmjs.com/
2. 註冊完成登入後請先設置 階段認證帳密，不然等等上傳每次都要透過mail收驗證信很麻煩
3. 請先拉取npm上的開源主題專案進行魔改，連結如下
https://www.npmjs.com/package/gitbook-plugin-theme-d4t

<!--more-->
### 1.3.2 操作步驟

1. 撰寫`package.json`設定檔

```json
{
  "name": "gitbook-plugin-theme-customtheme",
  "author": {
    "name": "markhsu"
  },
  "bugs": {
    "url": "https://markweb.idv.tw:10443/gitbooknpmproject/pushpublicnpm-/issues"
  },
  "dependencies": {},
  "description": "Gitbook theme for markhsu",
  "engines": {
    "gitbook": ">=3.0.0"
  },
  "homepage": "https://markweb.idv.tw:10443/gitbooknpmproject/pushpublicnpm-/blob/master/README.md",
  "keywords": [
    "gitbook",
    "theme",
    "customtheme"
  ],
  "main": "index.js",
  "repository": {
    "type": "git",
    "url": "https://markweb.idv.tw:10443/gitbooknpmproject/pushpublicnpm.git"
  },
  "scripts": {},
  "version": "1.0.9"
}
```

2. `logo.png`可以替換成自己想要的

3. 改寫css樣式檔

```css
body {
  font-family: "Helvetica Neue", "Hiragino Sans GB", "Microsoft YaHei", "\9ED1\4F53", Arial, sans-serif;
  letter-spacing: .2px;
  text-rendering: optimizeLegibility;
}
.markdown-section h1,
.markdown-section h2,
.markdown-section h3,
.markdown-section h4,
.markdown-section h5,
.markdown-section h6 {
  margin-bottom: .5em;
  font-weight: 400;
}
.markdown-section p {
  line-height: 2;
}
.markdown-section img {
  padding: 8px;
  background: #e4e4e478;
  transition: all 1s;
  box-sizing: border-box;
  box-shadow: 0 0 4px #dcdcdc;
  margin-left: 10px;
  margin-right: 10px;
  max-width: 95%;
}
.markdown-section img:hover {
  box-shadow: 0 0 10px #bbb
}

.exc-trigger {
  color: #333333;
}

.navigation {
  display: none;
}

/*Book inner page*/

.book-summary-title {
  height: 50px;
  line-height: 50px;
  padding-left: 30px;
  font-size: 16px;
  color: #adadad;
}

.book-summary,
.book-body {
  top: 80px;
}

.book-summary ul.summary li.active {
  border-right: 3px solid #7E57C2;
  background: #f3f1f1;
}

.book-summary ul.summary li.active>a {
  color: #7E57C2;
  text-decoration: none;
}

.book-summary ul.summary li a:hover {
  text-decoration: none;
}

.page-inner {
  max-width: none;
  padding: 20px 270px 40px 40px;
}

.header-inner #book-search-input {
  float: right;
  width: 300px;
  margin: 10px 0;
  padding: 0;
  border: none;
  background: #7E57C2;
  user-select: none;
}

.header-inner #book-search-input input[type="text"] {
  width: 80%;
  background: #e4e4e4;
}

.header-inner #book-search-input #searchBtn {
  color: #ffffff;
  margin-left: 10px;
  cursor: pointer;
}

.header-inner #book-search-input #searchBtn:hover {
  color: #eae8e8;
}

.header-inner {
  width: 100%;
  padding: 10px 30px;
  border-bottom: 1px solid #dededede;
  margin: auto;
  *zoom: 1;
  height: 80px;
}

.header-inner:before,
.header-inner:after {
  content: " ";
  display: table;
  line-height: 0;
}

.header-inner:after {
  clear: both;
}

.header-inner .logo {
  float: left;
  height: 50px;
  width: 120px;
  background: url('./logo.png');
  background-size: 120px 50px;
  background-repeat: no-repeat;
}

.header-inner .logo img {
  display: block;
  height: inherit;
  padding: 5px 0;
}

.header-inner .title {
  float: left;
  font-size: 20px;
  line-height: 60px;
  margin-left: 10px;
  color: #575656;
}

/* 导航 */
.header-inner .header-nav {
  list-style: none;
  margin: 10px 20px 0 0;
  padding: 0;
  float: right;
  display: table;
}

.header-inner .header-nav li {
  display: table-cell;
  vertical-align: middle;
  min-width: 50px;
  margin-right: 20px;
  padding: 8px 10px 8px 10px;
}

.header-inner .header-nav li a {
  color: #333333;
}

.header-inner .header-nav li a:hover,
.header-inner .header-nav li a.active {
  color: #7E57C2;
}

.header-inner .header-nav li a.active:hover {
  cursor: #7E57C2;
}

@media (max-width: 768px) {
  .book-summary,
  .book-body {
    top: 101px;
  }
  .header-inner #book-search-input {
    clear: both;
    width: 100%;
  }
}
/*Book inner page end*/

/* Book  anchor*/
.book-anchor {
  width: 180px;
  position: absolute;
  top: 130px;
  right: 30px;
  padding: 0 10px 10px 10px;
  z-index: 999;
  user-select: none;
  border-left: 2px solid #ececec;
}
.book-anchor-title {
  line-height: 38px;
  font-weight: 400;
  cursor: pointer;
}
.book-anchor a {
  display: block;
  line-height: 25px;
  color: #656565;
  font-size: 13px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.book-anchor a:hover {
  color: #7E57C2;
  text-decoration: none;
}
.book-anchor .selected {
  color: #7E57C2;
  text-decoration: none;
  font-weight: bold;
}
.book-anchor .anchor-h1 {}
.book-anchor .anchor-h2 {
  padding-left: 20px;
}
.book-anchor .anchor-h3{
  padding-left: 30px;
}
```

4. 撰寫`.npmrc`設定檔


```yaml
registry=https://registry.npmjs.com/
//registry.npmjs.com/:_auth="這邊要自己去產生金鑰"
email=[自己的email]
always-auth=true
```

5. 開啟cmd，輸入以下指令，`先進行登入`

```bash
npm login
```
![](https://markweb.idv.tw/uploads/upload_d1df11ca1d612ac5dfc144ccdbcdcbe5.png)

6. 輸入以下指令，進行`npm打包推送`

```bash
npm publish
```

![](https://markweb.idv.tw/uploads/upload_55b942ad2085064c657780d359e34b69.png)


![](https://markweb.idv.tw/uploads/upload_df8fc1ec4bb6ffdb0a31313903a68323.png)





