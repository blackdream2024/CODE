# 命理星河 API 网关服务 Dockerfile

FROM python:3.11-slim

WORKDIR /app

# 复制依赖文件
COPY requirements.txt ./

# 安装依赖
RUN pip install -r requirements.txt --no-cache-dir

# 复制应用代码
COPY . .

# 设置环境变量
ENV PORT=3000
ENV PYTHONUNBUFFERED=1

# 暴露端口
EXPOSE 3000

# 启动应用
CMD ["python", "main.py"]