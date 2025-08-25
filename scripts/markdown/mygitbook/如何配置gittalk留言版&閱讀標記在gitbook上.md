---
title: 如何配置gittalk留言版&閱讀標記在gitbook上
updated: 2024-07-23 13:31:37Z
created: 2024-07-17 14:46:03Z
latitude: 25.0329694
longitude: 121.5654177
altitude: 0
tags:
  - gittalk
  - Gitbook
  - readmark
  - comment
---

# 1 如何配置gittalk留言版在gitbook上

## 1.1 簡介

作為`閱讀紀錄`和`筆記`的好幫手

## 1.2 專案架構
```
Gitbook
├─ .gitignore
├─ .gitlab-ci.yml
├─ .npmignore
├─ autoBackupMarkdown.bat
├─ autoBackupMarkdownToGitBook.bat
├─ autoBackupMarkdownToHexo.bat
├─ azure
├─ batch
├─ book.json
├─ callmarkdownBuild.bat
├─ CHANGELOG.md
├─ ChatGPT
├─ check_commit_message.sh
├─ commitlint.config.js
├─ custom-release-notes-generator.js
├─ docker
├─ GAS
├─ gitbook-auto-summary-simple.py
├─ gitbook-auto-summary.py
├─ Gitlab
├─ hexo
├─ jenkins
├─ Linux
├─ mygitbook
├─ mysql
├─ nextcloud
├─ note
├─ package.json
├─ PicGo
├─ PowerAutoMate
├─ python
├─ README.md
├─ scripts
│  └─ custom.js
├─ shellscript
├─ sonarqube
├─ styles
│  └─ website.css
├─ SUMMARY.md
├─ thesis
└─ uncopy.txt
```
## 1.3 目錄

- [1 如何配置gittalk留言版在gitbook上](#1-如何配置gittalk留言版在gitbook上)
  - [1.1 簡介](#11-簡介)
  - [1.2 專案架構](#12-專案架構)
  - [1.3 目錄](#13-目錄)
  - [1.4  事前準備](#14--事前準備)
  - [1.5 程式撰寫](#15-程式撰寫)
  - [1.6 完成畫面](#16-完成畫面)


## 1.4  事前準備

請登入自己的`gitlab`，找到setting

![](https://markweb.idv.tw/uploads/202407172253097.png)

點擊`developer settings`

![](https://markweb.idv.tw/uploads/202407172253385.png)

點擊`OAuth Apps`，並點擊`New OAuth APP`新建 個

![](https://markweb.idv.tw/uploads/202407172253683.png)

建立完成之後會有 個`Client ID`，請先記錄下來，等等會使用到，至於`clientSecret`，請點擊紅框處的按鈕，也請先記錄下來，因為只會出現 次

![](https://markweb.idv.tw/uploads/202407172254525.png)

請填寫以下相關參數，說明如下：

> [!note] 小提示 
> * Application name：請務必要和預先建立的倉庫名稱一樣
> * Homepage URL：這邊要填gitbook的網址
> * Authorization callback URL：這邊要填gitbook的網址，務必和Homepage URL填一樣，否則會將網站導向奇怪的地方造成錯誤

完成後點選`Update application`按鈕

![](https://markweb.idv.tw/uploads/202407172255976.png)

<!--more-->
## 1.5 程式撰寫

> [!note] 小提示 
>* id：很多網站都沒說明，但這應該是必填，且最多不能超過50字元，但因為筆記都是中文名，所以要另外處理，否則會出現422 error
> * repo：這邊填寫要注意，倉庫issue設定要開啟，且專案要設為公開(public)


```javascript
    function initializeGitalk() {
     var title=location.pathname.substr(0,50);
       var gitalk = new Gitalk({
         clientID: 'Ov23ctKXv4a6jC9KJB8W',
         clientSecret: 'a0ca08a9cb489f338f0df7b93436130072bba18a',
         repo: '20240716_gitbook_repo',
         owner: 'Mark850409',
         admin: ['Mark850409'],
         distractionFreeMode: false,
         title: 'mycomment',
         id: title
        });
        gitalk.render('gitalk-container');
    }
```



> [!note] 小提示 
>  * initializeGitalk()：page.change是換頁時會觸發的事件，因此要在這邊呼叫gittalk以及readmarker


```javascript
   gitbook.events.on('page.change', function() {
	  setBase();
	  generateSectionNavigator();
	  initializeGitalk();
		
		var chapters = document.querySelectorAll(".chapter");

		chapters.forEach(function(chapter) {
		  var link = chapter.querySelector("a");
		  var chapterTitle = link.textContent.trim();
		  var marker = document.createElement("span");
		  marker.classList.add("read-marker");

		  if (localStorage.getItem(chapterTitle)) {
			if (!link.querySelector(".read-marker")) {
			  link.appendChild(marker);
			}
		  }

		  link.addEventListener("click", function() {
			localStorage.setItem(chapterTitle, "read");
			if (!link.querySelector(".read-marker")) {
			  link.appendChild(marker);
			}
		  });
		});
	});

```


```css
.read-marker {
  display: inline-block;
  width: 16px;
  height: 16px;
  margin-left: 8px; /* 添加 些間距 */
  background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="green" class="bi bi-check" viewBox="0 0 16 16"><path d="M10.97 4.97a.75.75 0 0 1 1.07 1.05L8.477 10.5a.75.75 0 0 1-1.08.02L4.324 7.384a.75.75 0 1 1 1.08-1.04L8 8.477l2.97-3.507z"/></svg>') no-repeat center center !important;
  vertical-align: middle; /* 確保與文字垂直對齊 */
}

.chapter-title {
  display: inline-flex;
  align-items: center;
}
```

## 1.6 完成畫面

![](https://markweb.idv.tw/uploads/202407172319939.png)