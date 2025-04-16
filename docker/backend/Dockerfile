# 使用官方Python镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright \
    PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple \
    DEBIAN_FRONTEND=noninteractive

# 复制依赖文件
COPY backend/requirements.txt .

# 配置apt源
RUN echo "deb http://mirrors.aliyun.com/debian/ bullseye main non-free contrib" > /etc/apt/sources.list \
    && echo "deb http://mirrors.aliyun.com/debian-security/ bullseye-security main" >> /etc/apt/sources.list \
    && echo "deb http://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib" >> /etc/apt/sources.list

# 更新apt缓存
RUN apt-get clean && apt-get update

# 安装X11相关依赖
RUN apt-get install -y --no-install-recommends \
    libx11-6 \
    libxext6 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    && rm -rf /var/lib/apt/lists/*

# 安装GTK相关依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxcb1 \
    libxkbcommon0 \
    && rm -rf /var/lib/apt/lists/*

# 安装其他必要依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatspi2.0-0 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# 安装中文字体支持
RUN apt-get update && apt-get install -y --no-install-recommends \
    fonts-wqy-microhei \
    fonts-wqy-zenhei \
    fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/* \
    && fc-cache -fv

# 安装Python依赖
RUN pip install --no-cache-dir werkzeug==2.0.3 flask==2.0.1
RUN pip install --no-cache-dir -r requirements.txt

# 安装playwright
RUN playwright install chromium

# 复制应用代码
COPY backend/app ./app
COPY backend/run.py .

# 暴露端口
EXPOSE 5556

# 启动应用
CMD ["python", "run.py"]