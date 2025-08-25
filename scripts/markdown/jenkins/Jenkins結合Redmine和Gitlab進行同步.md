---
title: Jenkins結合Redmine和Gitlab進行同步
updated: 2024-07-23 13:29:52Z
created: 2024-03-10 03:55:50Z
latitude: 25.0329694
longitude: 121.5654177
altitude: 0
tags:
  - Jenkins
  - Redmine
  - Gitlab
---

# 1. Jenkins結合Redmine和Gitlab進行同步

還沒有安裝Jenkins? 請參照這篇[[Jenkins自動化部署-安裝教學]]
## 1.1. 簡介

使用Jenkins讓Redmine和Gitlab可以連動

## 1.2. 專案架構

```
RedmineGitlabSync
├─ autoSyncRedminegit.sh
├─ CHANGELOG.md
├─ check_commit_message.sh
├─ custom-release-notes-generator.js
├─ custom.html
├─ Jenkinsfile
├─ package-lock.json
├─ package.json
├─ README.md
└─ send_line_notify.sh
```

## 1.3. 目錄

- [1. Jenkins結合Redmine和Gitlab進行同步](#1-jenkins結合redmine和gitlab進行同步)
  - [1.1. 簡介](#11-簡介)
  - [1.2. 專案架構](#12-專案架構)
  - [1.3. 目錄](#13-目錄)
  - [1.4. 操作步驟](#14-操作步驟)
    - [1.4.1. GITLAB相關設定](#141-gitlab相關設定)
    - [1.4.2. REDMINE相關設定](#142-redmine相關設定)
    - [1.4.3. 程式碼撰寫](#143-程式碼撰寫)
  - [1.5. 完成畫面](#15-完成畫面)


## 1.4. 操作步驟

### 1.4.1. GITLAB相關設定

進入Gitlab > 管理員設定 > 系統鉤子

> [!note] 小提示 
>1.KEY要在Redmine那邊先設定好
>2.自己的網域名稱要適時調整，這裡是markweb.idv.tw:18443
>3.觸發器可以看需求調整，這裡是設定都打勾
> 4.如果網站有掛SSL這裡要打勾

![](https://markweb.idv.tw/uploads/upload_7820c1d9c0c76c4f7fedef4db2701849.png)

<!--more-->

### 1.4.2. REDMINE相關設定

進入Redmine > 網站管理 > 設定 > 儲存機制清單

> [!note] 小提示 
> 1.Git這邊要打勾：
> 2.儲存機制的金耀這邊可以點選自動產生，產生一組金鑰
> 3.觸發關鍵字可以依照需求設定
> 4.觸發關鍵字對應的完成狀態及需求也可進行設定
> 5.點選儲存

專案管理 > 設定 > 儲存機制清單 > 建立新儲存機制

> [!note] 小提示 
>1.版本控管選擇git
>2.代碼可以自訂
>3.儲存機制路徑，這裡可以手動配置或透過Jenkins配置，下方會說明
>4.下方選項可勾可不勾
>5.點選建立

![](https://markweb.idv.tw/uploads/upload_ef43ae9e18d08c513d268e438af44927.png)

![](https://markweb.idv.tw/uploads/upload_5244685bbdd7665bde63742594681cba.png)

![](https://markweb.idv.tw/uploads/upload_e211319e8ef91b8457fc48542c3bb3de.png)

![](https://markweb.idv.tw/uploads/upload_e6cf138b255382786a2e0ef1cd1d5b18.png)


最後回到儲存機制，若可看到此畫面表示設定成功

![](https://markweb.idv.tw/uploads/upload_98b23e653e1a81081e51040f395a31b2.png)

![](https://markweb.idv.tw/uploads/upload_8f07982773dbbfc0aabe36c0496ce98e.png)


### 1.4.3. 程式碼撰寫

請撰寫`autoSyncRedminegit.sh`自動同步腳本

```bash
#!/bin/bash
#+-------------------------------------腳本說明--------------------------------------------+
# Redmine自動更新腳本
# 使用方式: ./autoSyncRedminegit.sh
#
# (C) 2023 - markhsu - licensed under markweb License v1.
#
#+----------------------------------------------------------------------------------------+
#                                    每分鐘同步一次 repos, 依照需求自行增加
#+----------------------------------------------------------------------------------------+
# 进入容器并执行操作
docker exec redmine bash -c '
    if [ ! -d /usr/src/redmine/repos/'$1' ]; then
        # 如果目录不存在，则从git clone目录并做fetch
        cd /usr/src/redmine/repos
        git clone --mirror '$2'
        cd '$1'
        git fetch --all
    else
        # 否则直接fetch
        cd /usr/src/redmine/repos/'$1'
        git fetch --all
    fi
'

```

請撰寫`Jenkins pipeline`腳本

```groovy
pipeline {
    agent any

    parameters {
        string(name: 'INITIAL_VERSION', defaultValue: '1.0.0', description: '初始版本號')
        string(name: 'EMAIL_RECIPIENTS', defaultValue: 'markhsu0704@gmail.com', description: '收件人地址')
        string(name: 'LINE_NOTIFY_TOKEN', defaultValue: 'MMvIR1dQ5g1uPYR8FEMN4d3gesRC1WSsBnNKApn7LKW', description: 'line notify 的token')
        string(name: 'PROJECT', defaultValue: 'redminegitlabsync.git', description: 'git專案名稱')
        string(name: 'MY_GIT_URL', defaultValue: 'https://root:mark850409@markweb.idv.tw:10443/godprojectteam/redminegitlabsync.git', description: 'MY_GIT_URL')
    }

    stages {
        stage('從gitlab拉取程式碼') {
            steps {
                script {
                    // 抓取GITLAB程式碼
                    git branch: 'master', credentialsId: 'gitlab', url: 'ssh://git@markweb.idv.tw:2222/godprojectteam/redminegitlabsync.git'
                }
            }
        }

        stage('部署腳本') {
            steps {
                script {
                    sh """
                    echo "MY_GIT_URL: ${params.PROJECT}"
                    echo "PROJECT: ${params.MY_GIT_URL}"
                    sh autoSyncRedminegit.sh ${params.PROJECT} ${params.MY_GIT_URL}
                    """
                }
            }
        }
    }

    post {
        always {
         // 安装 curl & pandoc
            script {
                sh '''
                if ! command -v curl &> /dev/null; then sudo apt update && sudo apt install -y curl; fi
                if ! command -v pandoc &> /dev/null; then apt update && apt install -y pandoc; fi
                '''
            }

            script {
                def buildResult = currentBuild.currentResult
                def jobName = env.JOB_NAME.trim()
                echo "Trimmed value: ${jobName}"
                // 執行LINE NOTIFY腳本
                sh """
                echo "部署结果: ${buildResult}"
                sh send_line_notify.sh $jobName $BUILD_NUMBER $BUILD_URL $GIT_BRANCH $GIT_COMMIT $WORKSPACE ${params.LINE_NOTIFY_TOKEN} ${buildResult}
                """
                
                // 讀取HTML模板內容
                def customHtmlTemplate = readFile('custom.html')
                // 寄送郵件
                emailext (
                    subject: "$jobName-#$BUILD_NUMBER-${buildResult}",
                    body: customHtmlTemplate,
                    mimeType: 'text/html',
                    to: "markhsu0704@gmail.com"
                )
            }
        }
    }
}
```


> [!note] 小提示 
>如果程式碼有結合語意化版本自動跳版號，請移除package.json2當中的emoji設定，否則Redmine和Gitlab關聯時會發生500 error!!!

## 1.5. 完成畫面

![](https://markweb.idv.tw/uploads/upload_fbf1ba2104dc58f9b61764b1a31a6c32.png)

![](https://markweb.idv.tw/uploads/upload_649a4f2fa5fc8637a65a9c13b969e32f.png)

![](https://markweb.idv.tw/uploads/upload_33f70c8d15732cda6c4b382c4a75fbba.png)