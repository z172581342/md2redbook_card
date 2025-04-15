# 使用官方Node.js镜像作为基础镜像
FROM node:18.19.1-alpine as build-stage

# 设置工作目录
WORKDIR /app

# 复制package.json和package-lock.json
COPY frontend/package*.json ./

# 安装依赖
RUN npm install

# 复制所有前端文件到工作目录
COPY frontend/src/ ./src/
COPY frontend/public/ ./public/
COPY frontend/index.html frontend/vite.config.js ./

# 构建应用
RUN npm run build

# 使用nginx来部署
FROM nginx:1.24.0-alpine as production-stage

# 从构建阶段复制构建好的文件到nginx目录
COPY --from=build-stage /app/dist /usr/share/nginx/html

# 复制nginx配置
COPY docker/frontend/nginx.conf /etc/nginx/conf.d/default.conf

# 暴露80端口
EXPOSE 80

# 启动nginx
CMD ["nginx", "-g", "daemon off;"]

# 添加 vite 相关配置文件
COPY frontend/.env* ./                  # 如果有环境变量文件
COPY frontend/tsconfig*.json ./         # 如果使用 TypeScript
COPY frontend/vite.config.* ./          # vite 配置文件 