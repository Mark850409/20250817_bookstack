# Dockerfile
FROM lscr.io/linuxserver/bookstack:latest

# 安裝 Python & pip (Alpine 用 apk)
RUN apk add --no-cache python3 py3-pip py3-requests py3-markdown

# 設定時區（可選）
ENV TZ=Asia/Taipei

# 設定 BookStack 環境變數
# 注意：DB_HOST 需要填 Zeabur 提供的 Database Host，而不是容器名稱
ENV PUID=1000 \
    PGID=1000 \
    APP_URL=${APP_URL} \
    DB_HOST=${DB_HOST} \
    DB_PORT=${DB_PORT} \
    DB_USER=${DB_USER} \
    DB_PASS=${DB_PASS} \
    DB_DATABASE=${DB_DATABASE} \
    APP_KEY=${APP_KEY}

# 建立資料目錄（在 Zeabur 可掛載 Volume）
RUN mkdir -p /config /var/www/bookstack/public/uploads /scripts

COPY scripts/ /scripts/

# 指定工作目錄
WORKDIR /var/www/bookstack

# 將 uploads 與 scripts 掛載（Zeabur 可設定 Volume）
VOLUME ["/config", "/var/www/bookstack/public/uploads", "/scripts"]

# 對外開放 Port 80
EXPOSE 80