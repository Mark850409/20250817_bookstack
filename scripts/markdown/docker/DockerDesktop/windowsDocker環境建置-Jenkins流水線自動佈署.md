---
title: windowsDocker環境建置-Jenkins流水線自動佈署
updated: 2024-07-23 13:28:09Z
created: 2023-09-19 01:19:43Z
latitude: 24.8387226
longitude: 121.0177246
altitude: 0
tags:
  - Docker
  - Jenkins
  - Windows
  - Pipeline
---

# 1 windowsDocker環境建置-Jenkins流水線自動佈署

還沒有安裝Docker? 請參照這篇[[[安裝Docker]]](app://obsidian.md/%E5%AE%89%E8%A3%9DDocker)

## 1.1 簡介
學習如何在windows使用jenkins

## 1.2 目錄

- [1 windowsDocker環境建置-Jenkins流水線自動佈署](#1-windowsdocker環境建置-jenkins流水線自動佈署)
  - [1.1 簡介](#11-簡介)
  - [1.2 目錄](#12-目錄)
    - [1.2.1 事前準備](#121-事前準備)
    - [1.2.2 設定docker login](#122-設定docker-login)
    - [1.2.3 Jenkins流水線佈署Python](#123-jenkins流水線佈署python)
    - [1.2.4 問題解法參考](#124-問題解法參考)



### 1.2.1 事前準備

請先到以下網址下載windows desktop版本，並且安裝WSL，否則docker會無法啟動

https://www.docker.com/products/docker-desktop/

https://learn.microsoft.com/zh-tw/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package

![image-20230919093126187](https://markweb.idv.tw/uploads/image-20230919093126187.png)

<!--more-->


### 1.2.2 設定docker login

1.從server抓取產生好的crt憑證
![image-20230919093856847](https://markweb.idv.tw/uploads/image-20230919093856847.png)

2. 透過Openssl進行轉檔，語法如下
```bash
openssl x509 -outform der -in [匯入的憑證檔名].pem -out [匯出的憑證檔名].crt
```

![image-20230919093706112](https://markweb.idv.tw/uploads/image-20230919093706112.png)

3. 將檔案放置到C:\ProgramData\Docker\certs.d\[網域名](這裡是markweb.idv.tw)

![image-20230919093523067](https://markweb.idv.tw/uploads/image-20230919093523067.png)

4. 開啟cmd，輸入以下指令，測試登入

```docker
docker login markweb.idv.tw:29443 -u admin -p admin
```

![image-20230919093333644](https://markweb.idv.tw/uploads/image-20230919093333644.png)

### 1.2.3 Jenkins流水線佈署Python

1. 設定和Git server作連動
![image-20230919224822665](https://markweb.idv.tw/uploads/image-20230919224822665.png)

2. 撰寫Jenkins Pipeline流水線腳本

```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                bat 'call "E:\\Project\\jenkins\\WindowsBuildPython\\autoBuildPython.bat"'
            }
        }
		
    }
	post {
        always {
             emailext mimeType: 'text/html',
			 body: '${FILE,path="custom.html"}', 
             subject: '$DEFAULT_SUBJECT',
             to: '${email}'
        }
    }

}
```

3. 撰寫Windows批次腳本


```powershell
chcp 65001
REM -------------------------------------腳本說明--------------------------------------------
REM 自動佈署python+SSL腳本
REM 使用方式: ./autogetSystemInfo.sh
REM
REM (C) 2023 - markhsu - licensed under markweb License v1.
REM 
REM ----------------------------------------------------------------------------------------
REM                                     切換到專案目錄下
REM ----------------------------------------------------------------------------------------
cd /d E:\Project\jenkins\WindowsBuildPython\python\
REM ----------------------------------------------------------------------------------------
REM                                     先停用所有容器
REM ----------------------------------------------------------------------------------------
docker stop mypython_phpmyadmin 
docker stop mypython_web 
docker stop mypython_db 
REM ----------------------------------------------------------------------------------------
REM                                     移除所有容器
REM ----------------------------------------------------------------------------------------
docker rm mypython_phpmyadmin 
docker rm mypython_web 
docker rm mypython_db 
REM ----------------------------------------------------------------------------------------
REM                                 要把python的image移除，不然不會重新打包
REM ----------------------------------------------------------------------------------------
REM SET version_number=5
REM SET version_number=4
docker rmi mypython:latest
docker login -u admin -p admin markweb.idv.tw:29443
docker-compose up -d
REM ----------------------------------------------------------------------------------------
REM                                 上傳到個人私有倉庫
REM ----------------------------------------------------------------------------------------
REM docker login -u ${user} -p ${password} ${URL}
REM docker tag mypython:${BUILD_NUMBER} ${URL}/jenkinsrepo/mypython:${BUILD_NUMBER}
REM docker push ${URL}/jenkinsrepo/mypython:${BUILD_NUMBER}
REM docker tag mypython_phpmyadmin:${BUILD_NUMBER} ${URL}/jenkinsrepo/mypython_phpmyadmin:${BUILD_NUMBER}
REM docker push ${URL}/jenkinsrepo/mypython_phpmyadmin:${BUILD_NUMBER}
REM docker tag mypython_apache:${BUILD_NUMBER} ${URL}/jenkinsrepo/mypython_apache:${BUILD_NUMBER}
REM docker push ${URL}/jenkinsrepo/mypython_apache:${BUILD_NUMBER}
REM ----------------------------------------------------------------------------------------
REM                              要給執行權限，否則permission_denied
REM ----------------------------------------------------------------------------------------
docker exec mypython_web bash -c "chmod +X main.py && chmod 777 main.py"
pause
```

4. 撰寫寄信範本html

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>${ENV, var="JOB_NAME"}-第${BUILD_NUMBER}次佈署日誌</title>
<style>
.post_body{
    border-bottom: 2px dashed #ccc;
    border: 2px dashed #202124;
    padding: 15px;
    margin-bottom: 20px;
    border-left: 3px solid #202124;
}
textarea{
border: 2px dashed #202124;
}
</style>
</head>
<body leftmargin="8" marginwidth="0" topmargin="8" marginheight="4"
    offset="0">
    <table width="95%" cellpadding="0" cellspacing="0"
        style="font-size: 11pt; font-family: Tahoma, Arial, Helvetica, sans-serif">
        <tr>
            <td>
                <h2>
                    <font>以下来自MarkWeb.Jenkins的郵件通知</font>
                </h2>
            </td>
        </tr>
        <tr>
            <td class='post_body'>
                <b><font color="#0B610B">佈署訊息</font></b>
             </td>
        </tr>
        <tr>
            <td>
                <ul>
                    <li>項目名稱&nbsp;：&nbsp;${PROJECT_NAME}</li>
                    <li>佈署版號&nbsp;：&nbsp;${BUILD_NUMBER}</li>
                    <li>佈署結果&nbsp;：&nbsp;${BUILD_STATUS}</li>
                    <li>佈署日志&nbsp;：&nbsp;<a href="${BUILD_URL}console">${BUILD_URL}console</a></li>
                    <li>觸發原因&nbsp;：${CAUSE}</li>
                    <li>單元測試報告&nbsp;：<a href="${BUILD_URL}testReport/">${BUILD_URL}testReport/</a></li>
                    <li>工作目錄&nbsp;：&nbsp;<a href="${PROJECT_URL}ws">${PROJECT_URL}ws</a></li>
                </ul>
            </td>
        </tr>
        <tr>
            <td class='post_body'><b><font color="#0B610B">佈署日誌:</font></b>
        </tr>
        <br />
        <br />
        <tr>
            <td>
            <textarea cols="120" rows="30" readonly="readonly" style="font-family: Courier New">${BUILD_LOG}</textarea>
            </td>
        </tr>
    </table>
</body>
</html>
```

5. 確認佈署成功

   ![image-20230919225931921](https://markweb.idv.tw/uploads/image-20230919225931921.png)

6. 在Jenkins點選馬上建置，並查看狀態

![image-20230919230258196](https://markweb.idv.tw/uploads/image-20230919230258196.png)


7. 確認有無收到email
![image-20230919230415473](https://markweb.idv.tw/uploads/image-20230919230415473.png)

8. 確認container是否都正常運行

![image-20230919231246622](https://markweb.idv.tw/uploads/image-20230919231246622.png)

9. 查看python是否正常運行

![image-20230919231426883](https://markweb.idv.tw/uploads/image-20230919231426883.png)

10. 查看phpmyadmin是否正常運行

![image-20230919231521382](https://markweb.idv.tw/uploads/image-20230919231521382.png)


> [!error] 小提示 
> 如果有遇到執行main.py的錯誤，請參考以下解決方案?
> 1. 務必將檔案格式轉換為UNIX

![image-20230920160617857](https://markweb.idv.tw/uploads/image-20230920160617857.png)

### 1.2.4 問題解法參考
1. https://blog.csdn.net/weixin_42170236/article/details/113396279
2. https://stackoverflow.com/questions/50768317/docker-pull-certificate-signed-by-unknown-authority
3. https://stackoverflow.com/questions/13732826/convert-pem-to-crt-and-key
4. https://blog.miniasp.com/post/2015/12/24/Jenkins-on-Windows-03-Avoid-messy-words-in-log-messages
5. https://blog.csdn.net/sandy_sweet/article/details/84873053