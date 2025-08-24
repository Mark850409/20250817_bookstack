---
title: 如何將打包好的npmpackage上傳到Gitlab
updated: 2024-07-23 13:31:28Z
created: 2024-02-05 13:56:13Z
latitude: 25.0329694
longitude: 121.5654177
altitude: 0
tags:
  - NPM
  - Gitlab
---

# 1 如何將打包好的npm package上傳到Gitlab

## 1.1 簡介
自己做出屬於自己風格的`npm package`，並打包上傳至`Gitlab`

## 1.2 專案架構

```
20240204_GitlabNPMcustomTheme
├─ .gitignore
├─ .gitlab-ci.yml
├─ .npmignore
├─ .npmrc
├─ index.js
├─ LICENSE
├─ logo.png
├─ package.json
├─ preview.png
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

- [1 如何將打包好的npm package上傳到Gitlab](#1-如何將打包好的npm-package上傳到gitlab)
  - [1.1 簡介](#11-簡介)
  - [1.2 專案架構](#12-專案架構)
  - [1.3 目錄](#13-目錄)
  - [1.4 事前準備](#14-事前準備)
  - [1.5 操作步驟](#15-操作步驟)
    - [1.5.1 在gitlab新增token](#151-在gitlab新增token)
    - [1.5.2 自動化部署到gitlab](#152-自動化部署到gitlab)
    - [1.5.3 下載npm安裝包到本地安裝](#153-下載npm安裝包到本地安裝)



## 1.4 事前準備

請建立`package.json`檔案，此為必要設定檔

> [!note] 小提示 
> 1. 首先先說明 下如果要使用**gitlab npm registry**的話，gitlab對於 **package name**名稱是有限制的
>* package name  定要是 @{scope}/ 開頭
>* 如果是 group project 那 {scope} 便是 group name
>* 而如果是 personal project 那 {scope} 便是 user name
>* 而斜線後面的名字則沒有強制規定要跟 repo 名稱相同
>2. 必填參數如下:
>* name:請按照上述格式
>* publishConfig:[project_id]請記得更改
>* version:版號也請記得要手動更新，且不能夠重複

```json
{
  "name": "@GitbookNPMProject/mypackage",
  "private": false,
  "repository": {
    "type": "git",
    "url": "https://markweb.idv.tw:10443/gitbooknpmproject/gitlabnpmcustomtheme"
  },
  "scripts": {
    "build:production": "node --version",
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "publishConfig": {
    "@GitbookNPMProject:registry": " https://markweb.idv.tw:10443/api/v4/projects/<project_id>/packages/npm/"
  },
  "version": "1.0.0"
}
```

請建立`.gitlab-ci.yml`，進行自動化部署

```yaml
image: node:15.4

stages:
  - deploy

deploy:
  stage: deploy
  script:
    - npm install --package-lock-only
    - echo CI_PROJECT_ID $CI_PROJECT_ID
    - echo CI_JOB_TOKEN $CI_JOB_TOKEN
    - cat .npmrc
    - npm ci
    - npm run build:production
    - echo "@gitbooknpmproject:registry=https://markweb.idv.tw:10443/api/v4/packages/npm/" >> .npmrc
    - echo "//markweb.idv.tw:10443//api/v4/packages/npm/:_authToken=${CI_JOB_TOKEN}" >> .npmrc
    - echo "//markweb.idv.tw:10443/api/v4/projects/${CI_PROJECT_ID}/packages/npm/:_authToken=${CI_JOB_TOKEN}" >> .npmrc
    - ls -al
    - npm publish

```

## 1.5 操作步驟


### 1.5.1 在gitlab新增token

在`Gitlab專案`下，點選`存取憑證`，並點選`新增令牌`

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/b9071c9e-upload-96ddba6e7ac2701666906019e30f63ee.png)

輸入令牌名稱，選取範圍`勾選API`，並點選`建立`

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/NXPbd6b8d5c-upload-ff12152bb69f6e23e23aa66aeac36e7a.png)

請先複製起來放到`記事本`或`NOTEPAD++`，免得不見要再產生 次

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/WEQe5eb49fe-upload-27e43a60540dfc2bc58b5c3c37341159.png)

<!--more-->
### 1.5.2 自動化部署到gitlab

在本地端下`git push`指令，將專案推送到`gitlab`

![](https://markweb.idv.tw/uploads/upload_0508c8031830770775a5e80d3d534756.png)

看到此畫面表示`部署成功`

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/50a87dd4-upload-21532d3d9a418dc55dc6345246f8903c.png)

到專案下的`package`進行查看，發現有 個新的安裝包

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/fb94d4cb-upload-f9ea0c5889a8aa9b1e92e5c5f74bf1c3.png)


### 1.5.3 下載npm安裝包到本地安裝
```bash
npm config set @GitbookNPMProject:registry https://markweb.idv.tw:10443/api/v4/packages/npm/
npm config set -- '//markweb.idv.tw:10443/api/v4/packages/npm/:_authToken' "<你的token>"
npm i @GitbookNPMProject/<你的package名稱>
```
完成畫面如下

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/f2706041-upload-377080c3f1176cb419ea19923ef9fba5.png)