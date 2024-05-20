# 使用官方Python镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录到工作目录
COPY . /app

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 启动命令
CMD ["uwsgi", "--ini", "uwsgi.ini"]