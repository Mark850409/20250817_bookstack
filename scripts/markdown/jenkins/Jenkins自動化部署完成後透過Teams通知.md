---
title: Jenkins自動化部署完成後透過Teams通知
updated: 2024-07-23 13:30:00Z
created: 2024-03-10 06:50:01Z
latitude: 25.0329694
longitude: 121.5654177
altitude: 0
tags:
  - Jenkins
  - Teams
---

# 1. Jenkins自動化部署完成後透過Teams通知

還沒有安裝Jenkins? 請參照這篇[[Jenkins自動化部署-安裝教學]]
## 1.1. 簡介
自動化部署完成後透過Teams通知

## 1.2. 目錄

- [1. Jenkins自動化部署完成後透過Teams通知](#1-jenkins自動化部署完成後透過teams通知)
  - [1.1. 簡介](#11-簡介)
  - [1.2. 目錄](#12-目錄)
  - [1.3. 專案架構](#13-專案架構)
  - [1.4. 操作步驟](#14-操作步驟)
      - [1.4.1. Teams設定](#141-teams設定)
      - [1.4.2. Jenkins設定](#142-jenkins設定)
  - [1.5. 撰寫程式碼](#15-撰寫程式碼)
  - [1.6. 完成畫面](#16-完成畫面)


## 1.3. 專案架構

```
JenkinsNotifyTeams
├─ Jenkinsfile
└─ README.md

```

## 1.4. 操作步驟


#### 1.4.1. Teams設定


進入Teams > 建立團隊 > 選擇連接器 > 點選編輯

![](https://markweb.idv.tw/uploads/upload_c602f06b992b041521af2cc94522de52.png)


若沒有Jenkins外掛要先行安裝 > 安裝後輸入自定義的名稱

![](https://markweb.idv.tw/uploads/upload_a5f794b299088a842b1472a377e48334.png)

<!--more-->
#### 1.4.2. Jenkins設定

進入管理Jenkins > Plugins > 安裝Office 365 Connector

![](https://markweb.idv.tw/uploads/upload_544f2f596bbfe71240e6e4aee09490da.png)

## 1.5. 撰寫程式碼

請撰寫`Jenkinsfile`

```Groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                // 在这里执行构建步骤
                echo '正在构建...'
            }
        }
        stage('Test') {
            steps {
                // 在这里执行测试步骤
                echo '正在运行测试...'
            }
        }
        stage('Deploy') {
            steps {
                // 在这里执行部署步骤
                echo '正在部署...'
            }
        }
    }

    post {
        success {
            // 发送成功通知
            sendTeamsNotification('部署成功！', '資料模型建置成功。')
        }
        failure {
            // 发送失败通知
            sendTeamsNotification('部署失敗！', '資料模型建置失敗。')
        }
    }
}

def sendTeamsNotification(String title, String message) {
    def payload = """
    {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "0072C6",
        "title": "${title}",
        "text": "${message}"
    }
    """
    
    def teamsUrl = "https://soochowmss.webhook.office.com/webhookb2/0bb4d014-5911-4b50-96fe-51ff272b1d55@86254269-e4d3-4c53-bc98-640752566d31/JenkinsCI/89e1a04738bf41d495048cd05b055bd3/4a1e9562-c0bf-4023-9cd0-20be53af0226"
    
    try {
        // 使用 curl 命令发送 HTTP POST 请求
        sh """
        curl -X POST -H 'Content-type: application/json' --data '${payload}' ${teamsUrl}
        """
    } catch (Exception e) {
        error "Failed to send Teams notification: ${e.message}"
    }
}

```

## 1.6. 完成畫面


![](https://markweb.idv.tw/uploads/upload_69be34509d4cf385dc2cb938247874a2.png)