---
title: Log4sh教學
updated: 2024-07-23 13:30:52Z
created: 2023-08-04 08:26:29Z
tags:
  - Linux
  - Log4sh
---

# 1. Log4sh教學

## 1.1. 簡介
學習如何利用Linux設定log4sh.properties

## 1.2. 目錄

- [1. Log4sh教學](#1-log4sh教學)
  - [1.1. 簡介](#11-簡介)
  - [1.2. 目錄](#12-目錄)
  - [1.3. Log4sh教學](#13-log4sh教學)
    - [1.3.1. 輸入以下指令](#131-輸入以下指令)
    - [1.3.2. 輸入以下指令](#132-輸入以下指令)
    - [1.3.3. 輸入以下指令](#133-輸入以下指令)
    - [1.3.4. 輸入以下指令执行文件並給予最高權限](#134-輸入以下指令执行文件並給予最高權限)
    - [1.3.5. enjoy](#135-enjoy)
  - [1.4. 以下為參考連結](#14-以下為參考連結)


## 1.3. Log4sh教學

### 1.3.1. 輸入以下指令

```bash
git clone https://github.com/kward/log4sh.git
mkdir test && cd test && cp ../log4sh/log4sh .
```

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/w5q595da514-upload-804ee65a5e4dc6f45484486e465ab472.png)

<!--more-->

### 1.3.2. 輸入以下指令

```bash
vim helloworld.sh

# 2 ! /bin/bash

## 2.1 include log4jsh file
. ./log4sh

# 3 Say Hello to the world.
logger_info "Hello, world"

# 4 second way to Say hello
echo 'message to log' |logger_info
```

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/XWg59dcbeb3-upload-5ca84025e5296583abd3056d59d8e054.png)

### 1.3.3. 輸入以下指令

```bash
vim log4sh.properties

# 5 
# 6 log4sh example: Hello, world properties file
# 7 

# 8 Set root logger level to INFO and its only appender to A1.
log4sh.rootLogger=INFO, A1

# 9 A1 is set to be a ConsoleAppender.
log4sh.appender.A1=ConsoleAppender

# 10 A1 uses a PatternLayout.
log4sh.appender.A1.layout=PatternLayout
log4sh.appender.A1.layout.ConversionPattern=%-4r [%t] %-5p %c %x - %m%n
```

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/E0W74385e91-upload-d0830137f47246901dc26f26b4f95e38.png)

### 1.3.4. 輸入以下指令执行文件並給予最高權限

```bash
chmod 777 * 
./helloworld.sh 
```

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/a9ee94df-upload-4f748130770b32c25edfc1371f2467f1.png)

### 1.3.5. enjoy

![](https://mybookstack.zeabur.app/uploads/images/gallery/2025-08/371ba346-upload-7e6643c8c41b55352572f78f98daf313.png)

## 1.4. 以下為參考連結

* * *

https://dockerlin666.gitee.io/2020/08/24/shell-log4jsh/

https://github.com/kward/log4sh/blob/master/doc/log4sh.md