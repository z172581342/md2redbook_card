# Markdown转小红书卡片

一个将Markdown文本转换为小红书风格卡片的工具，支持深色/浅色模式，可自定义主题、字体大小和卡片尺寸。

## 功能特点

- 实时Markdown预览与编辑
- 多种主题风格选择
- 支持深色/浅色模式自动切换
- 自定义卡片尺寸和字体大小
- 图片导出功能
- API接口服务

## 前端安装与运行

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 开发模式运行
npm run dev

# 构建生产版本
npm run build
```

## 后端API安装与运行

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\\Scripts\\activate

# 安装依赖
pip install -r requirements.txt

# 安装Playwright浏览器驱动 (如果需要后端进行截图)
# 请根据 backend/app/services/converter.py 中的配置确认是否需要以及需要哪个浏览器
# playwright install chromium  # 示例：安装 chromium
playwright install

# 启动服务
python run.py
```

## API使用说明

### 转换Markdown为图片

**端点:** `POST /convert` (请根据 `backend/app/routes.py` 确认)

**请求体:**
```json
{
  "markdown": "# 标题\n这是内容",
  "style": {
    "theme": "light",
    "fontSize": 16,
    "width": 440,
    "height": 586
  }
}
```

**响应:** 成功时返回包含图片URL或图片数据的JSON。失败时返回错误信息。

## 配置说明

### 前端配置 (`frontend/`)
- 默认运行在 `http://localhost:5173` (由 `vite.config.js` 或 `package.json` 配置)
- 支持的主题: light, dark, pink, blue, appleMemo, artDeco, popArt, retroTypewriter, japaneseMag (请在前端代码中确认最新列表)
- 图片尺寸范围: 宽度和高度均在200-1000像素之间 (可能在前端组件中限制)
- API请求地址: 可能在前端代码中配置 (例如: `.env` 文件或直接在代码中)

### 后端配置 (`backend/`)
- 默认运行在 `http://localhost:5556` (由 `run.py` 或 Flask/FastAPI 配置决定)
- CORS设置: 可在 `backend/app/__init__.py` (如果是Flask) 或类似 FastAPI 的主应用文件中配置
- 截图服务依赖的前端URL: 如果后端需要调用前端进行截图，相关URL配置可能在 `backend/app/services/converter.py` 中。

## 演示
![小红书卡片演示](https://raw.githubusercontent.com/xlwt2113/md2redbook_card/refs/heads/main/public/pic.png)
*(请确保此图片链接仍然有效或替换为新的演示图)*

## 项目结构

```
md2redbook_card/
├── frontend/                 # 前端代码 (Vue/React/etc.)
│   ├── public/
│   ├── src/
│   ├── index.html
│   ├── package.json
│   └── vite.config.js        # (或其他构建工具配置)
│
├── backend/                  # 后端代码 (Python/Node.js/etc.)
│   ├── app/                  # 应用核心代码
│   ├── venv/                 # Python虚拟环境 (通常不提交到git)
│   ├── run.py                # 启动脚本
│   └── requirements.txt      # Python依赖
│
├── scripts/                  # 辅助脚本
│   └── test_api.sh           # API测试脚本示例
│
├── temp/                     # 临时文件目录 (例如: 生成的图片)
│
├── docker/                   # Docker配置文件
│   ├── frontend/
│   │   ├── Dockerfile
│   │   └── nginx.conf        # (如果使用Nginx)
│   └── backend/
│       └── Dockerfile
│
├── docker-compose.yml        # Docker Compose配置
├── .gitignore                # Git忽略配置
└── README.md                 # 项目说明文档
```

## Docker部署说明

### 使用Docker Compose部署

1.  **构建和启动容器**
    ```bash
    docker-compose up -d --build
    ```
    `--build` 参数确保每次都重新构建镜像，以包含最新的代码更改。`-d` 表示在后台运行。

2.  **访问应用**
    - 前端界面: `http://localhost:8080` (根据 `docker-compose.yml` 中的 `ports` 配置)
    - 后端API: `http://localhost:5556` (根据 `docker-compose.yml` 中的 `ports` 配置)

3.  **停止容器**
    ```bash
    docker-compose down
    ```
    这个命令会停止并移除由 `docker-compose up` 创建的容器、网络等。

4.  **查看日志**
    ```bash
    # 查看所有服务的实时日志
    docker-compose logs -f

    # 查看特定服务的日志 (例如 frontend)
    docker-compose logs -f frontend

    # 查看后端服务的日志
    docker-compose logs -f backend
    ```

### Docker 配置说明

- **前端容器 (`frontend` service in `docker-compose.yml`)**: 通常基于 Node.js 镜像构建应用，然后可能使用 Nginx 或其他Web服务器来提供静态文件服务。
- **后端容器 (`backend` service in `docker-compose.yml`)**: 通常基于 Python 镜像，安装 `requirements.txt` 中的依赖，并运行API服务 (`run.py`)。
- **数据卷 (`volumes` in `docker-compose.yml`)**:
    - 代码同步: 将本地的 `frontend` 和 `backend` 目录挂载到容器内，方便开发时代码修改实时生效。
    - 共享目录: 可能将 `temp` 目录挂载到前端和后端容器，用于文件交换 (例如后端生成图片，前端需要访问)。
- **端口映射 (`ports` in `docker-compose.yml`)**: 将宿主机的端口映射到容器内部运行服务的端口。
- **依赖关系 (`depends_on` in `docker-compose.yml`)**: 可以定义服务启动的依赖顺序 (例如前端可能依赖后端API)。

如需修改配置 (例如端口号)，请编辑 `docker-compose.yml` 文件以及各个服务对应的 `Dockerfile` (`docker/frontend/Dockerfile`, `docker/backend/Dockerfile`)。