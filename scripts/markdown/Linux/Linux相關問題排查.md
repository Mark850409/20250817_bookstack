---
title: Linux相關問題排查
updated: 2024-08-04 11:47:09Z
created: 2024-08-02 02:39:46Z
latitude: 25.0329694
longitude: 121.5654177
altitude: 0
tags:
  - Linux
  - problem
---

# 1. Linux 相關問題排查

## 1.1. 簡介

紀錄`安裝過程`遇到的問題紀錄

## 1.2. 目錄

- [1. Linux 相關問題排查](#1-linux-相關問題排查)
  - [1.1. 簡介](#11-簡介)
  - [1.2. 目錄](#12-目錄)
  - [1.3. 問題與處理步驟](#13-問題與處理步驟)


## 1.3. 問題與處理步驟

> [!note] 小提示 
>Q1：Linux主機開機如何自啟動

解決步驟

- 查看時區

```bash
timedatectl
```

![](https://markweb.idv.tw/uploads/202408022345829.png)

- 強制使用`RTC`，而非`UTC`時間

```bash
timedatectl set-local-rtc 1
```

- 讀取目前`BIOS主機板`時間 

```bash
 hwclock -r
```

![](https://markweb.idv.tw/uploads/202408022347332.png)

- 寫入目前時間到`BIOS`

```bash
hwclock -w
```

![](https://markweb.idv.tw/uploads/202408022348505.png)

<!--more-->

> [!note] 小提示 
>  Q2：SonarQube登入失敗

錯誤訊息

```bash
[org.sonar.scanner.bootstrap.GlobalServerSettings]: Factory method 'provide' threw exception; nested exception is Not authorized. Please check the properties sonar.login and sonar.password.
```

解決步驟

<div class="note info">
	<p>sonarqube如果重新部署，不能沿用舊的token，請在建立 個新的token</p>
</div>


> [!note] 小提示 
>  Q3：Jenkins出現Failed to connect to repository

錯誤訊息

```bash
Failed to connect to repository : Command "git ls-remote -h -- ssh://git@markweb.idv.tw:2222/dockercomposeteam/flaskcrudvue_localhost.git HEAD" returned status code 128:
stdout:
stderr: Bad owner or permissions on /root/.ssh/config
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```

解決步驟

- 檢查 /root/.ssh/config 文件的權限：

確保該文件的權限設置為 600，這樣只有擁有者（通常是 root）可以讀取和寫入該文件，其他人無法存取。你可以使用以下命令來設定權限

```bash
chmod 600 /root/.ssh/config
```

- 檢查 /root/.ssh 目錄的權限：

確保該目錄的權限設置為 700，這樣只有擁有者可以進入和操作該目錄：

```bash
chmod 700 /root/.ssh
```


- 檢查文件擁有者

確保 /root/.ssh/config 文件的擁有者是 root。如果 Jenkins 是以 root 用戶執行的，則擁有者應該是 root。你可以使用以下命令來確認擁有者：

```bash
ls -l /root/.ssh/config 
```


- 如果需要更改擁有者，可以使用 chown 命令：

```bash
chown root:root /root/.ssh/config
```



- 測試 SSH 連接：

確保 SSH 配置文件中的設定是正確的，並且能夠連接到 Git 存儲庫。你可以手動測試 SSH 連接： 

```bash
ssh -T git@markweb.idv.tw -p 2222   
```

如果這個命令能夠成功執行並顯示歡迎消息，則 SSH 配置應該是正確的。 



> [!note] 小提示 
>  Q4：docker-portainer管理工具加入中文出現輸入正確密碼無法登入問題

錯誤訊息

```bash
出現0.510 error: externally-managed-environment
0.510                                                                                                                   0.510 × This environment is externally managed
0.510 ╰─> To install Python packages system-wide, try apt install
0.510     python3-xyz, where xyz is the package you are trying to
0.510     install.
0.510
0.510     If you wish to install a non-Debian-packaged Python package,
0.510     create a virtual environment using python3 -m venv path/to/venv.
0.510     Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
0.510     sure you have python3-full installed.
0.510
0.510     If you wish to install a non-Debian packaged Python application,
0.510     it may be easiest to use pipx install xyz, which will manage a
0.510     virtual environment for you. Make sure you have pipx installed.
0.510
0.510     See /usr/share/doc/python3.11/README.venv for more information.
0.510
0.510 note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
0.510 hint: See PEP 668 for the detailed specification.
```

解決步驟

請參考：https://www.cnblogs.com/A1999/p/15993682.html


> [!note] 小提示 
>  Q5：jenkins dockerfile包版出現rror: externally-managed-environment

解決步驟

- 這個錯誤信息顯示你的環境是 個「外部管理環境」，這意味著你不能直接使用 pip 安裝系統範圍內的 Python 包。這是 種防止系統 Python 環境被修改的安全措施。
- 要解決這個問題，你可以按照以下步驟操作：

使用虛擬環境 

建議使用 Python 虛擬環境來安裝 Python 包。這樣可以避免對系統 Python 環境造成影響。

撰寫Dockerfile 

- 安裝了 python3-venv，用於創建虛擬環境。
- 創建了 個虛擬環境 /opt/venv 並將其添加到 PATH 中。
- 使用虛擬環境中的 pip 安裝 Python 包。

```docker
FROM jenkins/jenkins:2.470-jdk17
USER root

# 1 安裝基礎工具
RUN apt-get update && apt-get install -y \
       apt-transport-https \
       ca-certificates \
       curl \
       gnupg2 \
       software-properties-common \
       python3 \
       python3-venv \
       python3-pip \
       vim

# 2 添加 Docker 的 GPG 密鑰
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# 3 添加 Docker 仓库
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# 4 更新 APT 索引並安裝 Docker CLI
RUN apt-get update && apt-get install -y docker-ce-cli

# 5 安裝 docker-compose
RUN curl -L "https://github.com/docker/compose/releases/download/1.25.3/docker-compose-$(uname -s)-$(uname -m)" \
  -o /usr/local/bin/docker-compose \
  && chmod +x /usr/local/bin/docker-compose

# 6 創建並激活虛擬環境
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 7 安裝 Python 包
RUN pip install --upgrade pip
RUN pip install art pytest allure-pytest

# 8 清理 APT cache
RUN apt-get clean && rm -rf /var/lib/apt/lists/*
```

> [!note] 小提示 
>  Q6：harbor如何備份registry?  

解決步驟

- 執行rsync指令先進行備份(要整個目錄包含資料庫，不是只有registry)

```bash
rsync -avrz data/* data2/
```

![](https://markweb.idv.tw/uploads/202408031540782.png)

- 編輯`harbor.yml`

```bash
vim harbor.yml
```

- 修改data_volume的部份

![](https://markweb.idv.tw/uploads/202408031542951.png)

- 執行安裝程式

```bash
./install.sh 
```

![](https://markweb.idv.tw/uploads/202408031543690.png)


> [!note] 小提示 
>  Q7: 如何在Linux掛載硬碟?

- 列出所有磁碟 UUID

```bash
sudo blkid
```

![](https://markweb.idv.tw/uploads/202408022343819.png)

- 修改 `/etc/fstab`

```bash
sudo vim /etc/fstab
```

- 增加此行

```bash
UUID="5E38D75638D72C31" /media/markhsu/Data ntfs defaults 0 2
```

![](https://markweb.idv.tw/uploads/202408022341453.png)


> [!note] 小提示 
> Q8: Jenkins出現 stderr: fatal: not in a git directory


錯誤訊息

```
Started by user markhsu
hudson.plugins.git.GitException: Command "git config remote.origin.url ssh://git@markweb.idv.tw:2222/dockercomposeteam/flaskcrudvue_localhost.git" returned status code 128:
stdout: 
stderr: fatal: not in a git directory

    at PluginClassLoader for git-client//org.jenkinsci.plugins.gitclient.CliGitAPIImpl.launchCommandIn(CliGitAPIImpl.java:2846)
    at PluginClassLoader for git-client//org.jenkinsci.plugins.gitclient.CliGitAPIImpl.launchCommandIn(CliGitAPIImpl.java:2766)
    at PluginClassLoader for git-client//org.jenkinsci.plugins.gitclient.CliGitAPIImpl.launchCommandIn(CliGitAPIImpl.java:2761)
    at PluginClassLoader for git-client//org.jenkinsci.plugins.gitclient.CliGitAPIImpl.launchCommand(CliGitAPIImpl.java:2051)
    at PluginClassLoader for git-client//org.jenkinsci.plugins.gitclient.CliGitAPIImpl.launchCommand(CliGitAPIImpl.java:2063)
    at PluginClassLoader for git-client//org.jenkinsci.plugins.gitclient.CliGitAPIImpl.setRemoteUrl(CliGitAPIImpl.java:1662)
    at PluginClassLoader for git-client//hudson.plugins.git.GitAPI.setRemoteUrl(GitAPI.java:180)
    at PluginClassLoader for git//jenkins.plugins.git.GitSCMFileSystem$BuilderImpl.build(GitSCMFileSystem.java:393)
    at PluginClassLoader for scm-api//jenkins.scm.api.SCMFileSystem.of(SCMFileSystem.java:219)
    at PluginClassLoader for workflow-cps//org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition.create(CpsScmFlowDefinition.java:126)
    at PluginClassLoader for workflow-cps//org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition.create(CpsScmFlowDefinition.java:73)
    at PluginClassLoader for workflow-job//org.jenkinsci.plugins.workflow.job.WorkflowRun.run(WorkflowRun.java:311)
    at hudson.model.ResourceController.execute(ResourceController.java:101)
    at hudson.model.Executor.run(Executor.java:446)
[Gitea] do not publish assets due to build being non-Successfully
Finished: FAILURE
```


解決步驟

- 這問題會出現在移轉jenkins時，解法如下：
```bash
cd /var/jenkins_home
git config --global --add safe.directory '*'
```

進入jenkins，輸入這兩行指令即可，完成後記得重啟生效


> [!note] 小提示 
> Q9: 如何在tortorisegit新增SSH key

解決步驟

請參考
- https://blog.csdn.net/Jeffxu_lib/article/details/112259246?ydreferer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8%3D

-  https://floatfrog.blogspot.com/2015/06/tortoisegitssh-keygitlab.html


> [!note] 小提示 
> Q10: 如何在jenkins新增css

解決步驟

- 先撰寫以下css

```css
/* 設定表格、表單、輸入框、單元格、標題欄、段落、文本區域、下拉選單的字型 */
table, form, input, td, th, p, textarea, select {
    font-family: Arial, sans-serif; /* 字型設定為 Arial，備選為 sans-serif */
    font-size: 14px; /* 字體大小為 14px */
}

/* 設定描述區域的底部邊距 */
# 9 description {
    margin-bottom: 20px !important; /* 底部邊距為 20px，使用 !important 強制覆蓋 */
}

a:hover {
    text-decoration: none !important; /* 懸停時取消下劃線，使用 !important 強制覆蓋 */
}

/* 設定標頭的高度 */
# 10 header {
    height: 60px !important; /* 高度為 60px，使用 !important 強制覆蓋 */
}

/* 設定搜尋框的高度 */
# 11 search-box.main-search__input {
    height: 35px !important; /* 高度為 35px，使用 !important 強制覆蓋 */
}

/* 設定控制台輸出的圓角 */
.console-output {
    border-radius: 30px !important; /* 圓角為 30px，使用 !important 強制覆蓋 */
}

/* 設定在程式碼區域中的連結顏色 */
body>pre a, body>pre a:visited, #main-panel pre a, #main-panel pre a:visited {
    color: #2196F3 !important; /* 連結顏色為 #2196F3，使用 !important 強制覆蓋 */
}

/* 設定面包屑導航的懸停效果 */
# 12 breadcrumbs li:hover {
    color: transparent !important; /* 懸停時顏色為透明，使用 !important 強制覆蓋 */
}

/* 設定 Jenkins 表格的樣式 */
.jenkins-table {
    border: none !important; /* 無邊框，使用 !important 強制覆蓋 */
    background: transparent !important; /* 背景為透明，使用 !important 強制覆蓋 */
}

/* 設定自定義標頭的背景色和高度 */
.custom-header__page {
    background: teal; /* 背景顏色為青色 */
    height: 3.5rem; /* 高度為 3.5rem */
}

/* 隱藏頁腳中的 Jenkins 按鈕 */
.page-footer .jenkins-button {
    display: none !important; /* 隱藏按鈕，使用 !important 強制覆蓋 */
}

/* 設定應用程式登入和註冊頁面的標題樣式 */
.app-sign-in-register__content-inner h3 {
    font-family: "Noto Sans TC", sans-serif; /* 字型設定為 Noto Sans TC，備選為 sans-serif */
    font-optical-sizing: auto; /* 自動調整字體光學大小 */
    font-weight: 400; /* 字體粗細為 400 */
    font-style: normal; /* 字體樣式為正常 */
}

/* 設定全站文字的字型和樣式 */
body, form, input, p, select, table, td, textarea, th {
    font-family: "Noto Sans TC", "Roboto", sans-serif !important; /* 字型設定為 Noto Sans TC，備選為 Roboto 和 sans-serif，使用 !important 強制覆蓋 */
    font-optical-sizing: auto !important; /* 自動調整字體光學大小，使用 !important 強制覆蓋 */
    font-weight: 500 !important; /* 字體粗細為 500，使用 !important 強制覆蓋 */
    font-style: normal !important; /* 字體樣式為正常，使用 !important 強制覆蓋 */
}

/* Material Design風格的控制台輸出樣式 */
.console-output {
    background-color: #333; /* 較深的黑色背景 */
    border: 1px solid #004c8c; /* 邊框顏色與背景色協調 */
    border-radius: 4px; /* 圓角 */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2); /* 更明顯的陰影 */
    padding: 16px; /* 內邊距 */
    font-family: 'Roboto', sans-serif; /* 字型設定為 Roboto，備選為 sans-serif */
    color: #ffffff; /* 白色文字 */
    line-height: 1.5; /* 行高 */
    overflow-x: auto; /* 橫向滾動 */
}

/* 控制台輸出中的關鍵字或標籤 */
.console-output .keyword {
    color: #00aaff; /* 明亮的藍色 */
    font-weight: bold; /* 加粗 */
}

/* 控制台輸出中的警告或錯誤 */
.console-output .warning, .console-output .error {
    color: #ff3d00; /* 明亮的橙色 */
    font-weight: bold; /* 加粗 */
}

/* 控制台輸出中的資訊 */
.console-output .info {
    color: #00e676; /* 亮綠色 */
    font-weight: bold; /* 加粗 */
}

/* 控制台輸出中的連結樣式 */
.console-output a {
    color: #00aaff; /* 與關鍵字顏色 致 */
    text-decoration: underline; /* 連結下劃線 */
}

.console-output a:hover {
    color: #007bb5; /* 連結懸停顏色，稍微深 點 */
    text-decoration: none; /* 懸停時移除下劃線 */
}

side-panel .pane-frame {
    background: transparent im !important; 
    border: none !important;
}
```


- 將css透過sftp上傳至`/home/markhsu/jenkins/data/war/css/`

- 記下css url路徑
![](https://markweb.idv.tw/uploads/202408022333313.png)

- 增加 個css url，將剛剛的路徑貼上
![](https://markweb.idv.tw/uploads/202408022334748.png)

- 想要找相關的jenkins logo，可以從這個網址
https://www.jenkins.io/zh/artwork/


> [!note] 小提示 
> Q11: 新版harbor出現錯誤

![](https://markweb.idv.tw/uploads/202408031751305.png)


解決步驟

- 開啟harbor.yml，加入以下語法

```
jobservice:
  # Maximum number of job workers in job service
  max_job_workers: 10
  # The jobLoggers backend name, only support "STD_OUTPUT", "FILE" and/or "DB"
  job_loggers:
    - STD_OUTPUT
    - FILE
    # - DB
  # The jobLogger sweeper duration (ignored if `jobLogger` is `stdout`)
  logger_sweeper_duration: 1 #days
```

- 重新執行腳本

```bash
./install.sh
```

![](https://markweb.idv.tw/uploads/202408031753439.png)

