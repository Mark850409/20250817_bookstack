---
title: SVNWEBSERVER建置
updated: 2024-07-23 13:30:49Z
created: 2023-08-04 08:26:29Z
tags:
  - Linux
  - SVN
  - Server
---

# 1 SVN WEBSERVER建置


## 1.1 簡介
學習如何安裝SVN WEBSERVER

## 1.2 目錄

- [1 SVN WEBSERVER建置](#1-svn-webserver建置)
  - [1.1 簡介](#11-簡介)
  - [1.2 目錄](#12-目錄)
    - [1.2.1 安装java运行环境和Subversion](#121-安装java运行环境和subversion)
    - [1.2.2 下载最新版发行包jar](#122-下载最新版发行包jar)
    - [1.2.3 啟動webServer](#123-啟動webserver)
    - [1.2.4 成功畫面](#124-成功畫面)

### 1.2.1 安装java运行环境和Subversion

```bash
apt update
apt install openjdk-11-jdk
apt install subversion
```

<!--more-->

### 1.2.2 下载最新版发行包jar

```bash
mkdir /home/svnWebUI/
```

```bash
wget -O /home/svnWebUI/svnWebUI.jar http://file.nginxwebui.cn/svnWebUI-1.7.7.jar
```

### 1.2.3 啟動webServer

```bash
nohup java -jar -Dfile.encoding=UTF-8 /home/svnWebUI/svnWebUI.jar --server.port=6060 > /dev/null &
```


> [!note] 小提示 
>  参数说明(都是非必填)
>1.  --server.port 占用端口, 默认以6060端口启动
>2.  --project.home 项目配置文件目录，存放仓库文件, 数据库文件等, 默认为/home/svnWebUI/
>3.  --database.type=mysql 使用其他数据库，不填为使用本地h2数据库
>4.  --database.url=jdbc:mysql://ip:port/dbname 数据库url
>5.  --database.username=root 数据库用户
>6.  --database.password=pass 数据库密码
> 注意命令最后加 个&号, 表示项目后台运行
### 1.2.4 成功畫面

![](https://markweb.idv.tw/uploads/upload_0b00e9f7ecbfb630f5e4b01b360304d4.png)