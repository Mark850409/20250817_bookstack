---
title: Gitlab安裝教學
updated: 2024-07-23 13:29:05Z
created: 2024-02-18 13:16:14Z
latitude: 25.0329694
longitude: 121.5654177
altitude: 0
tags:
  - Gitlab
---

# 1. Gitlab安裝教學

### 1.1. 簡介

`Gitlab` 架設教學


### 1.2. 目錄

- [1. Gitlab安裝教學](#1-gitlab安裝教學)
    - [1.1. 簡介](#11-簡介)
    - [1.2. 目錄](#12-目錄)
  - [1.1 使用方式](#11-使用方式)
    - [1.1.1 操作步驟](#111-操作步驟)
  - [1.2 執行步驟](#12-執行步驟)
    - [1.2.1 架設Gitlab](#121-架設gitlab)
    - [1.2.2 架設GitRunner](#122-架設gitrunner)
    - [1.2.3 SSH KEY 建立](#123-ssh-key-建立)
      - [1.2.3.1 Windows操作步驟](#1231-windows操作步驟)
      - [1.2.3.2 LINUX操作步驟差異在config寫法不同](#1232-linux操作步驟差異在config寫法不同)
  - [1.3 問題解決步驟](#13-問題解決步驟)
    - [1.3.1 HARBOR SSL連線失敗解決方案](#131-harbor-ssl連線失敗解決方案)
    - [1.3.2 找不到Gitlab內建存放庫](#132-找不到gitlab內建存放庫)
    - [1.3.3 Gitlab Web編輯器無法正常登入](#133-gitlab-web編輯器無法正常登入)
    - [1.3.4 參考資料如下](#134-參考資料如下)



## 1.1 使用方式

### 1.1.1 操作步驟
1. 安裝好`git`環境
2. 開啟`cmd`，輸入git clone `倉庫的URL`，拉取此專案到自己的主機

<!--more-->

## 1.2 執行步驟

### 1.2.1 架設Gitlab

1. 撰寫docker-compose.yml

```yaml
version: "3.6"
services:
  gitlab:
    image: gitlab/gitlab-ce:latest
    container_name: gitlab
    restart: always
    environment:
      GITLAB_OMNIBUS_CONFIG: |
       external_url 'https://markweb.idv.tw:10443'
    ports:
      - '8082:80'
      - '2222:22'
    volumes:
      - '/home/markhsu/gitlab/data:/var/opt/gitlab'
      - '/home/markhsu/gitlab/logs:/var/log/gitlab'
      - '/home/markhsu/gitlab/config:/etc/gitlab'
      - '/media/markhsu/Data/DockerProtainer/nextcloud/web/data/admin/files/photo:/var/opt/gitlab/photo'
      - '/media/markhsu/Data/DockerProtainer:/var/opt/gitlab/host_data'
  gitlab-runner:
    image: gitlab/gitlab-runner:latest
    container_name: gitlab-runner
    restart: always
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /media/markhsu/Data/DockerProtainer/gitlab/gitlab-runner:/etc/gitlab-runner
  registry:
    image: registry:2
    restart: always
    container_name: gitlab_registry
    ports:
      - 5300:5000
    volumes:
      - /media/markhsu/Data/DockerProtainer/gitlab/registry/data:/var/lib/registry
  apache:
    image: php:7.4-apache
    restart: always
    ports:
      - 10443:443
    volumes:
      - /media/markhsu/Data/DockerProtainer/gitlab/etc/apache2:/etc/apache2
      - /media/markhsu/Data/DockerProtainer/gitlab/etc/letsencrypt/live/markweb.idv.tw:/etc/letsencrypt/live/markweb.idv.tw
```

2. 撰寫000-default.conf


```bash
<VirtualHost *:80>
	# The ServerName directive sets the request scheme, hostname and port that
	# the server uses to identify itself. This is used when creating
	# redirection URLs. In the context of virtual hosts, the ServerName
	# specifies what hostname must appear in the request's Host: header to
	# match this virtual host. For the default virtual host (this file) this
	# value is not decisive as it is used as a last resort host regardless.
	# However, you must set it for any further virtual host explicitly.
	ServerName markweb.idv.tw

	#ServerAdmin webmaster@localhost
	DocumentRoot /var/www/html

	# Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
	# error, crit, alert, emerg.
	# It is also possible to configure the loglevel for particular
	# modules, e.g.
	#LogLevel info ssl:warn

	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined

	# For most configuration files from conf-available/, which are
	# enabled or disabled at a global level, it is possible to
	# include a line for only one particular virtual host. For example the
	# following line enables the CGI configuration for this host only
	# after it has been globally disabled with "a2disconf".
	#Include conf-available/serve-cgi-bin.conf
</VirtualHost>

<VirtualHost *:443>
   ServerName markweb.idv.tw:443
   SSLEngine on
   SSLCertificateFile /etc/letsencrypt/live/markweb.idv.tw/cert.pem
   SSLCertificateKeyFile /etc/letsencrypt/live/markweb.idv.tw/privkey.pem
   SSLCertificateChainFile /etc/letsencrypt/live/markweb.idv.tw/chain.pem
   ProxyPreserveHost On
   ProxyRequests Off
   ProxyPass / http://markweb.idv.tw:8082/ nocanon
   ProxyPassReverse / http://markweb.idv.tw:8082/
   AllowEncodedSlashes NoDecode
</VirtualHost>
```

3. 進入DockerPortainer部署，並查看gitlab容器是否已執行

![image-20240117213835210](https://markweb.idv.tw/uploads/image-20240117213835210.png)

---
### 1.2.2 架設GitRunner


1. 進入gitlab建立群組

![image-20240117214753574](https://markweb.idv.tw/uploads/image-20240117214753574.png)

2. 在建置→runners，點擊 個點點，複製token，等等會用到

![image-20240117214904273](https://markweb.idv.tw/uploads/image-20240117214904273.png)

3. 執行以下指令

```bash
gitlab-runner register
```

執行畫面如下
```bash
user@CPUNode:~/workplace/devops$ docker exec -it gitlab-runner gitlab-runner register
Runtime platform                                    arch=amd64 os=linux pid=1337 revision=7f093137 version=15.2.0
Running in system-mode.                            

Enter the GitLab instance URL (for example, https://gitlab.com/):
https://gitlab.me
Enter the registration token:
<PLACE YOUR TOKEN HERE>
Enter a description for the runner:
[4b3193ddb657]: cpu
Enter tags for the runner (comma-separated):
cpu
Enter optional maintenance note for the runner:
cpu
Registering runner... succeeded                     runner=GR1348941bf4A3CAE
Enter an executor: virtualbox, kubernetes, custom, docker, parallels, ssh, docker-ssh, shell, docker+machine, docker-ssh+machine:
docker
Enter the default Docker image (for example, ruby:2.7):
python:3.9.13
Runner registered successfully. Feel free to start it, but if it's running already the config should be automatically reloaded!

Configuration (with the authentication token) was saved in "/etc/gitlab-runner/config.toml" 
```

4. 打開`config.toml`，更改畫面紅框處

> [!note] 小提示 
> * Runner 的 config 會存放在 **/etc/gitlab-runner/config.toml**
>* 這幾次測試時發現，gitlab 似乎會隨機挑選runner(每次執行都會是不同的)，因此這邊設定標籤要注意，不要將沒有註冊docker環境的執行器設定標籤，否則在自動化腳本會出錯
> * 若要同時執行多個環境的docker而不需要等待目前已執行的執行器，可多建立幾個runner，且註冊好執行環境即可，可按照下圖方式配置

![image-20240121152858713](https://markweb.idv.tw/uploads/image-20240121152858713.png)

![](https://markweb.idv.tw/uploads/202407172350324.png)

![](https://markweb.idv.tw/uploads/202407172351435.png)

### 1.2.3 SSH KEY 建立

#### 1.2.3.1 Windows操作步驟

1. 使用以下指令建立 組`金鑰`

```bash
ssh-keygen -t rsa -b 8192
```

![image-20240117220235153](https://markweb.idv.tw/uploads/image-20240117220235153.png)


2. 在`config`檔案新增以下指令


```yaml
Host gitlab
  #domain name
  HostName markweb.idv.tw
  User root
  Port 2222
  #通常會用 publickey
  PreferredAuthentications publickey
  #添加到 ssh-agent 將私鑰和密碼交给他管理、進行身份認證
  AddKeysToAgent yes
  #要綁定的 ssh key
  IdentityFile ~/.ssh/gitlab_rsa
```

3. 進入`Gitlab`，添加 組剛剛產生的公開金鑰`gitlab_rsa.pub`

![image-20240117220507713](https://markweb.idv.tw/uploads/image-20240117220507713.png)

4. 測試windows是否可以成功

![image-20240117222325693](https://markweb.idv.tw/uploads/image-20240117222325693.png)

---
#### 1.2.3.2 LINUX操作步驟差異在config寫法不同
![image-20240117222455660](https://markweb.idv.tw/uploads/image-20240117222455660.png)



## 1.3 問題解決步驟

### 1.3.1 HARBOR SSL連線失敗解決方案
1. 找到`registry`的這支API，點選鎖頭
![image-20240121150514153](https://markweb.idv.tw/uploads/image-20240121150514153.png)

2. 填上`Harbor`正確登入的`帳號`以及`密碼`
![image-20240121150606390](https://markweb.idv.tw/uploads/image-20240121150606390.png)

3. 開啟cmd，連線到遠端，輸入以下指令進行測試，出現`SSL憑證錯誤`的訊息

```bash
curl -X GET -H "Authorization: Bearer bWFya2hzdTpNYXJrODUwNDA5" https://markweb.idv.tw:29443/api/v2.0/registries
```
![image-20240121150707083](https://markweb.idv.tw/uploads/image-20240121150707083.png)

4. 編輯`harbor.yml`的設定檔，更改`crt`檔案
![image-20240121150853037](https://markweb.idv.tw/uploads/image-20240121150853037.png)

5. 存檔後重新執行`./install.sh`
![image-20240121151349789](https://markweb.idv.tw/uploads/image-20240121151349789.png)

6. 確認容器`全部啟動成功`即可
![image-20240121151431274](https://markweb.idv.tw/uploads/image-20240121151431274.png)

7. 成功畫面如下

![image-20240121152947893](https://markweb.idv.tw/uploads/image-20240121152947893.png)

![image-20240121153020311](https://markweb.idv.tw/uploads/image-20240121153020311.png)

![image-20240121153040298](https://markweb.idv.tw/uploads/image-20240121153040298.png)

---

### 1.3.2 找不到Gitlab內建存放庫

1. 在gitlab的`docker-compose.yml` 加入以下語法

```yaml
  registry:
    image: registry:2
    restart: always
    container_name: gitlab_registry
    ports:
      - 5300:5000
    volumes:
      - /media/markhsu/Data3/DockerProtainer/gitlab/registry/data:/var/lib/registry
```
![image-20240121153826093](https://markweb.idv.tw/uploads/image-20240121153826093.png)

2. 開啟`/etc/gitlab/gitlab.rb`，按照`紅框處`更新以下內容

![image-20240121154022411](https://markweb.idv.tw/uploads/image-20240121154022411.png)

![image-20240121154047071](https://markweb.idv.tw/uploads/image-20240121154047071.png)

3. 重新載入設定檔，輸入以下指令
```bash
gitlab-ctl reconfigure
```

4. 進入gitlab的容器映像庫，開始使用以下指令測試

![image-20240121155305652](https://markweb.idv.tw/uploads/image-20240121155305652.png)

5. 執行以下指令進行測試

```bash
# 登入
docker login markweb.idv.tw:5300
# 部署
docker build -t markweb.idv.tw:5300/gidlabprojectteam/20240117_gitlabsetup .
# 推送
docker push markweb.idv.tw:5300/gidlabprojectteam/20240117_gitlabsetup
```

![image-20240121155221568](https://markweb.idv.tw/uploads/image-20240121155221568.png)

![image-20240121155631310](https://markweb.idv.tw/uploads/image-20240121155631310.png)

![image-20240121155653791](https://markweb.idv.tw/uploads/image-20240121155653791.png)


6. 成功畫面如下

![image-20240121155423169](https://markweb.idv.tw/uploads/image-20240121155423169.png)

![image-20240121155515952](https://markweb.idv.tw/uploads/image-20240121155515952.png)

---

### 1.3.3 Gitlab Web編輯器無法正常登入

1. 編輯`/etc/apache2/sites-available/000-default.conf`，輸入以下指令，並重啟伺服器即可


```bash
ProxyPass / http://markweb.idv.tw:8082/ nocanon
```

![image-20240121161034932](https://markweb.idv.tw/uploads/image-20240121161034932.png)

### 1.3.4 參考資料如下
1. 解決Harbor無法信任根憑證之問題
>https://stackoverflow.com/questions/24611640/curl-60-ssl-certificate-problem-unable-to-get-local-issuer-certificate

2. 如何使用Gitlab-CI
>https://hackmd.io/@CloudyWing/B1Agss77s

3. Gitlab Container Registry使用
>https://blog.csdn.net/axibazZ/article/details/118733107

4. webIDE載入問題
>https://gitlab.com/gitlab-org/gitlab-foss/-/issues/45657