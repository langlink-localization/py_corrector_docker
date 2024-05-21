# 使用官方Python镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录到工作目录
COPY . /app

# 安装依赖
RUN pip3 install torch --index-url https://download.pytorch.org/whl/cpu --no-cache-dir
RUN pip install --no-cache-dir -r requirements.txt

# 设置 Flask 应用的环境变量
ENV FLASK_APP=app.py

# 设置适当的文件权限以确保日志可以写入
RUN touch /app/app.log && chmod 666 /app/app.log

# 启动命令
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
