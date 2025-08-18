---
title: Jenkins自動化部署-建立SWAGGERAPI文件
updated: 2024-07-23 13:30:06Z
created: 2023-10-05 09:22:10Z
latitude: 24.8387226
longitude: 121.0177246
altitude: 0
tags:
  - Jenkins
  - SwaggerAPI
  - Documents
---

# 1. BuildSwaggerAPI

還沒有安裝Jenkins? 請參照這篇[[Jenkins自動化部署-安裝教學]]

## 1.1. 簡介

`自動化佈署`API文件

## 1.2. 專案結構

```
20240331_BuildSwagger
├─ .env
├─ apache
│  ├─ 000-default.conf
│  ├─ apache2.conf
│  ├─ Dockerfile
│  ├─ index.php
│  ├─ letsencrypt
│  │  └─ live
│  │     └─ markweb.idv.tw
│  │        ├─ cert.pem
│  │        ├─ chain.pem
│  │        ├─ fullchain.pem
│  │        ├─ privkey.pem
│  │        └─ README
│  ├─ ports.conf
│  └─ swagger-output.json
├─ autoBuildSwagerAPI.sh
├─ CHANGELOG.md
├─ check_commit_message.sh
├─ custom-release-notes-generator.js
├─ custom.html
├─ deploy_harbor.sh
├─ docker-compose.yml
├─ Jenkinsfile
├─ package-lock.json
├─ package.json
├─ README.md
├─ send_line_notify.sh
└─ style.css

```

## 1.3. 目錄

- [1. BuildSwaggerAPI](#1-buildswaggerapi)
  - [1.1. 簡介](#11-簡介)
  - [1.2. 專案結構](#12-專案結構)
  - [1.3. 目錄](#13-目錄)
    - [1.3.1. 使用方式](#131-使用方式)
    - [1.3.2. 執行步驟](#132-執行步驟)
    - [1.3.3. 執行結果](#133-執行結果)


### 1.3.1. 使用方式
1. 安裝好`git`環境
2. 開啟`cmd`，輸入git clone `倉庫的URL`，拉取此專案到自己的主機
3. 如果要使用`Jenkins`執行`CI/CD佈署`，請參考以下`執行步驟`

<!--more-->
### 1.3.2. 執行步驟


> [!note] 小提示 
> 1. docker-compose環境變數要和json檔案做綁定，因此請參考以下設定<br>
> 2. 目前json檔案沒辦法自動產生，得依賴半自動的方式


 請撰寫`Jenkinsfile`

```Groovy
pipeline {
    agent any

    parameters {
        string(name: 'HARBOR_REGISTRY', defaultValue: 'markweb.idv.tw:29443', description: 'Harbor倉庫地址')
        string(name: 'HARBOR_USERNAME', defaultValue: 'admin', description: 'Harbor用户名')
        password(name: 'HARBOR_PASSWORD', defaultValue: 'admin', description: 'Harbor密碼')
        string(name: 'INITIAL_VERSION', defaultValue: '1.0.0', description: '初始版本號')
        string(name: 'EMAIL_RECIPIENTS', defaultValue: 'markhsu0704@gmail.com', description: '收件人地址')
        string(name: 'LINE_NOTIFY_TOKEN', defaultValue: 'MMvIR1dQ5g1uPYR8FEMN4d3gesRC1WSsBnNKApn7LKW', description: 'line notify 的token')
        string(name: 'DOCKER_PROJECT', defaultValue: 'myswaggerrepo', description: 'Harbor倉庫名稱')
    }

    // environment {
    //     ENV_FILE = ".env"
    // }

    stages {
        stage('從gitlab拉取程式碼') {
            steps {
                script {
                    // 抓取GITLAB程式碼
                    git branch: 'master', credentialsId: 'gitlab', url: 'ssh://git@markweb.idv.tw:2222/jenkinsjob/BuildSwaggerAPI.git'
                }
            }
        }

        stage('部署腳本') {
            steps {
               script {
                    // 部署腳本
                    sh "sh deploy_harbor.sh ${HARBOR_REGISTRY} ${HARBOR_USERNAME} ${HARBOR_PASSWORD} ${INITIAL_VERSION} 'swaggerapi' 'Dockerfile' ${DOCKER_PROJECT}"
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

請撰寫`docker-compose.yml`

```yaml
version: '3'
services:
  apache:
    container_name: swagger-apache
    image: ${IMAGE_NAME}
    restart: always
    ports:
      - ${swagger_editor_SSLPORTS}:443
      - ${swagger_ui_SSLPORTS}:24443
  swagger-editor:
   image: swaggerapi/swagger-editor
   container_name: swagger-editor-container
   volumes:
    - /media/markhsu/Data/DockerProtainer/Swagger/FoodPanda_Swagger_0.json:/FoodPanda_Swagger_0.json
   environment:
    - SWAGGER_FILE=/FoodPanda_Swagger_0.json  # 指定使用自定義的 JSON 檔案
   ports:
    - ${swagger_editor_PORTS}:8080
   restart: always
   networks:
      - swagger-net
  swagger-ui:
   image: swaggerapi/swagger-ui
   container_name: swagger-ui-container
   volumes:
    - /media/markhsu/Data/DockerProtainer/Swagger/FoodPanda_Swagger_0.json:/FoodPanda_Swagger_0.json
    - /media/markhsu/Data/DockerProtainer/Swagger/FoodPanda_Swagger_1.json:/FoodPanda_Swagger_1.json
   ports:
    - ${swagger_ui_PORTS}:8080
   environment:
    - SWAGGER_JSON=/FoodPanda_Swagger_0.json
    - SWAGGER_JSON=/FoodPanda_Swagger_1.json
   restart: always
   networks:
      - swagger-net
networks:
  swagger-net:
```

 請撰寫`autoBuildSwagerAPI.sh`

```bash
#!/bin/bash
#+-------------------------------------腳本說明--------------------------------------------+
# 自動佈署SwagerAPI腳本
# 使用方式: ./autoBuildSwagerAPI.sh
#
# (C) 2023 - markhsu - licensed under markweb License v1.
# 
#+----------------------------------------------------------------------------------------+
#                                     先停用所有容器
#+----------------------------------------------------------------------------------------+
docker stop swagger-apache 
docker stop swagger-ui-container 
docker stop swagger-editor-container 
#+----------------------------------------------------------------------------------------+
#                                     移除所有容器
#+----------------------------------------------------------------------------------------+
docker rm swagger-apache  
docker rm swagger-ui-container 
docker rm swagger-editor-container 
#+----------------------------------------------------------------------------------------+
#                           要把swagger-ui的image移除，不然不會重新打包
#+----------------------------------------------------------------------------------------+
version_number=${BUILD_NUMBER}
version_number=$(($version_number-1))
docker rmi swagger-ui-container:${version_number}
BUILD_NUMBER=${BUILD_NUMBER} docker-compose up -d
#+----------------------------------------------------------------------------------------+
#                                 上傳到個人私有倉庫
#+----------------------------------------------------------------------------------------+
docker login -u ${user} -p ${password} ${URL}
docker tag myswaggerapache:${BUILD_NUMBER} ${URL}/jenkinsrepo/myswaggerapache:${BUILD_NUMBER}
docker push ${URL}/jenkinsrepo/myswaggerapache:${BUILD_NUMBER}
#+----------------------------------------------------------------------------------------+
#                                 複製檔案到自己的SFTP SERVER
#+----------------------------------------------------------------------------------------+
cp swagger-output.json /var/jenkins_home/sftp
```

請撰寫`.env`
```bash
#APACHE參數設定
APACHE_PORTS=50443
APACHE_PORTS2=51443
#swagger參數設定
swagger_editor_PORTS=9024
swagger_ui_PORTS=9025
API_URL=https://markweb.idv.tw:2223/swagger-output.json
```

### 1.3.3. 執行結果

![](https://markweb.idv.tw/uploads/upload_30fddfcaaa647274b7bc6f0ac6bfc900.png)


![](https://markweb.idv.tw/uploads/upload_b458c32b5456548eefe4670d4e66ae30.png)

![](https://markweb.idv.tw/uploads/upload_e822eae869cb053c4535b396958baf8d.png)