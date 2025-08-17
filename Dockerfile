# Dockerfile
FROM lscr.io/linuxserver/bookstack:latest

# 安裝 Python & pip (Alpine 用 apk)
RUN apk add --no-cache python3 py3-pip py3-requests py3-markdown

# 複製我們的匯入腳本 (例如 import_md.py)
#COPY import_md.py /usr/local/bin/import_md.py
#RUN chmod +x /usr/local/bin/import_md.py
