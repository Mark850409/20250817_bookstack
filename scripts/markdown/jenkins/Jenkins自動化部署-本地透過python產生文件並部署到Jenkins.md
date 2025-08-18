---
title: Jenkins自動化部署-本地透過python產生文件並部署到Jenkins
updated: 2024-07-23 13:30:11Z
created: 2024-03-31 12:02:29Z
latitude: 25.0329694
longitude: 121.5654177
altitude: 0
tags:
  - Jenkins
  - python
---

# 1. SwaggerFoodPandaAPI

還沒有安裝Jenkins? 請參照這篇[[Jenkins自動化部署-安裝教學]]
### 1.1.  簡介

`自動化產生`API文件並透過Jenkins部署

### 1.2. 專案結構

```
SwaggerAPI
├─ .gitignore
├─ .gitlab-ci.yml
├─ app
│  ├─ app.py
│  ├─ foodpanda_api.py
│  ├─ order
│  │  ├─ routes.py
│  │  └─ __pycache__
│  │     ├─ routes.cpython-311.pyc
│  │     └─ swagger.cpython-311.pyc
│  ├─ panda
│  │  ├─ routes.py
│  │  └─ __pycache__
│  │     ├─ routes.cpython-311.pyc
│  │     └─ swagger.cpython-311.pyc
│  └─ __pycache__
│     └─ app.cpython-311.pyc
├─ autoBuildSwaggerAPI.sh
├─ autoCreateSwaggerJson.bat
├─ CHANGELOG.md
├─ check_commit_message.sh
├─ custom-release-notes-generator.js
├─ custom.html
├─ FoodPanda_Swagger_0.json
├─ FoodPanda_Swagger_1.json
├─ Jenkinsfile
├─ package-lock.json
├─ package.json
├─ pyvenv.cfg
├─ README.md
├─ send_line_notify.sh
└─ style.css

```

### 1.3. 目錄

- [1. SwaggerFoodPandaAPI](#1-swaggerfoodpandaapi)
    - [1.1.  簡介](#11--簡介)
    - [1.2. 專案結構](#12-專案結構)
    - [1.3. 目錄](#13-目錄)
  - [1.3.1 使用方式](#131-使用方式)
  - [1.3.2 執行步驟](#132-執行步驟)
  - [1.3.3 執行結果](#133-執行結果)



## 1.3.1 使用方式
1. 安裝好`git`環境
2. 開啟`cmd`，輸入git clone `倉庫的URL`，拉取此專案到自己的主機
3. 如果要使用`Jenkins`執行`CI/CD佈署`，請參考以下`執行步驟`

<!--more-->
## 1.3.2 執行步驟

請撰寫`Jenkinsfile`

```Groovy
pipeline {
    agent any

    stages {
        stage('從gitlab拉取程式碼') {
            steps {
                script {
                    // 抓取GITLAB程式碼
                    git branch: 'master', credentialsId: 'gitlab', url: 'ssh://git@markweb.idv.tw:2222/godprojectteam/swaggerfoodpandaapi.git'
                }
            }
        }

        stage('部署腳本') {
            steps {
               script {
                    // 部署腳本
                    sh "sh autoBuildSwaggerAPI.sh"
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

                /*
                * LINE NOTIFY
                */
                def buildResult = currentBuild.currentResult
                def jobName = env.JOB_NAME.trim()
                echo "Trimmed value: ${jobName}"
                // 執行LINE NOTIFY腳本
                sh """
                echo "部署结果: ${buildResult}"
                sh send_line_notify.sh $jobName $BUILD_NUMBER $BUILD_URL $GIT_BRANCH $GIT_COMMIT $WORKSPACE ${params.LINE_NOTIFY_TOKEN} ${buildResult}
                """
                

                /*
                * email NOTIFY
                */
                // 讀取HTML模板內容
                def customHtmlTemplate = readFile('custom.html')
                // 寄送郵件
                emailext (
                    subject: "$jobName-#$BUILD_NUMBER-${buildResult}",
                    body: customHtmlTemplate,
                    mimeType: 'text/html',
                    to: "markhsu0704@gmail.com"
                )


                /*
                * 生成CHANGELOG.MD
                */

                // 使用 pandoc 将 markdown 转换为 HTML
                // 将 Bootstrap 5 的 CSS 文件下载到 Jenkins 作业目录
                // 在 HTML 文件中引用 Bootstrap 5 的 CSS 文件
                sh '''
                sed -i 's/### //' CHANGELOG.md 
                sed -i 's/## //' CHANGELOG.md              
                pandoc -f markdown -t html -o changelog.html CHANGELOG.md
                '''

                // 读取自定义 CSS 样式
                def cssContent = readFile('style.css')
                echo "Changelog CSS content:\n>${cssContent}"

                 // 讀取生成的 HTML 文件
                def changelogHtml = readFile('changelog.html')


                // 在 HTML 文件的开头插入居中的 H1 标题
                changelogHtml = "<style>${cssContent}</style><h1>$JOB_NAME-#$BUILD_NUMBER-Git版本變更紀錄</h1>\n" + changelogHtml

                changelogHtml = "<link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css\">" + changelogHtml
                              
                 // 印出 changelogHtml 內容以進行檢查
                echo "Changelog HTML content:\n${changelogHtml}"
                
                // 将变更日志保存到文件
                writeFile file: 'changelog.html', text: changelogHtml


                // 归档 HTML 文件
                archiveArtifacts artifacts: 'changelog.html', onlyIfSuccessful: false
                
                // 在 Jenkins 构建页面上添加 HTML 文件的链接
                publishHTML(target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: false,
                    keepAll: true,
                    reportDir: '.',
                    reportFiles: 'changelog.html',
                    reportName: 'Gitlab版本變更紀錄'
                ])
            }
        }
    }
}
```

請撰寫`autoBuildSwaggerAPI.sh`

```bash
#!/bin/bash
#+-------------------------------------腳本說明--------------------------------------------+
# 自動佈署SwagerAPI腳本
# 使用方式: ./autoBuildSwagerAPI.sh
#
# (C) 2023 - markhsu - licensed under markweb License v1.
# 
#+----------------------------------------------------------------------------------------+
#                                 複製檔案到自己的container
#+----------------------------------------------------------------------------------------+
cp FoodPanda_Swagger_0.json  FoodPanda_Swagger_1.json /Backup/DockerProtainer/Swagger

```

請撰寫`autoCreateSwaggerJson.bat`


```powershell
@echo off
REM 设置虚拟环境目录
set VENV_DIR="E:\todolist"

REM 激活虚拟环境

call %VENV_DIR%\Scripts\activate & start /b cmd /c "python app/app.py"

@REM REM 延迟 段时间以确保 Flask 应用启动
timeout /t 5 /nobreak >nul

REM 打开默认浏览器并导航到 http://localhost:5000
python -c "import webbrowser; webbrowser.open('http://localhost:5000')"

```

> [!note] 小提示 
> 1. 目前json檔案沒辦法自動產生，得依賴半自動的方式，請手動執行autoCreateSwaggerJson.bat
>2. 這邊要注意 下架構層面，標準是看有幾個API就開幾個目錄，且每個目錄 定要有routes.py
>3. app.py 定要放最外層，否則會執行失敗
> 

撰寫`routes.py`&`app.py`

確認文件撰寫無誤，執行`autoCreateSwaggerJson.bat`

## 1.3.3 執行結果

![](https://markweb.idv.tw/uploads/upload_84df020c40446e9f97004f23aa692976.png)

![](https://markweb.idv.tw/uploads/upload_e9a40a6b06b870902decbfdce80365b4.png)


![](https://markweb.idv.tw/uploads/upload_9f3d20a228a3846b544b23e7bf300b2b.png)

![](https://markweb.idv.tw/uploads/upload_5e353cdbebbf9378effd8cedc5dbfef0.png)