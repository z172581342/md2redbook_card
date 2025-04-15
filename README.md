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
cd md2redbook_api

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 安装Playwright浏览器
playwright install chromium

# 启动服务
python run.py
```

## API使用说明

### 转换Markdown为图片

请求体:
```json
{
  "markdown": "# 标题\n内容",
  "style": {
    "theme": "light",
    "fontSize": 16,
    "width": 440,
    "height": 586
  }
}
```

## 配置说明

### 前端配置
- 默认运行在 `http://localhost:5173`
- 支持的主题: light, dark, pink, blue, appleMemo, artDeco, popArt, retroTypewriter, japaneseMag
- 图片尺寸范围: 宽度和高度均在200-1000像素之间

### 后端配置
- 默认运行在 `http://localhost:5556`
- 在`md2redbook_api/app/__init__.py`中可配置CORS设置
- 在`md2redbook_api/app/services/converter.py`中设置截图服务的前端URL

## 演示
![小红书卡片演示](https://raw.githubusercontent.com/xlwt2113/md2redbook_card/refs/heads/main/public/pic.png)

## 项目结构

```
md2redbook_card/
├── frontend/                 # 前端代码
│   ├── public/               # 静态资源
│   │   └── pic.png           # 示例图片
│   ├── src/                  # 源代码
│   │   ├── assets/           # 资源文件
│   │   ├── components/       # 组件
│   │   ├── App.vue           # 主组件
│   │   ├── main.js           # 入口文件
│   │   └── style.css         # 样式文件
│   ├── index.html            # HTML模板
│   ├── package.json          # 前端依赖
│   └── vite.config.js        # Vite配置
│
├── backend/                  # 后端代码
│   ├── app/                  # 应用代码
│   ├── run.py                # 启动脚本
│   └── requirements.txt      # 后端依赖
│
├── scripts/                  # 脚本文件
│   └── test_api.sh           # API测试脚本
│
├── temp/                     # 临时文件目录
│
├── docker/                   # Docker配置
│   ├── frontend/             # 前端Docker配置
│   │   ├── Dockerfile        # 前端Dockerfile
│   │   └── nginx.conf        # Nginx配置文件
│   └── backend/              # 后端Docker配置
│       └── Dockerfile        # 后端Dockerfile
│
├── docker-compose.yml        # Docker Compose配置
├── .gitignore                # Git忽略文件
└── README.md                 # 项目说明
```

## Docker部署说明

### 使用Docker Compose部署

1. **构建和启动容器**
   ```bash
   docker-compose up -d
   ```
   这个命令会构建前端和后端的Docker镜像并在后台启动容器。

2. **访问应用**
   - 前端界面: http://localhost:8080
   - 后端API: http://localhost:5556

3. **停止容器**
   ```bash
   docker-compose down
   ```

4. **查看日志**
   ```bash
   # 查看所有容器日志
   docker-compose logs -f
   
   # 查看前端容器日志
   docker-compose logs -f frontend
   
   # 查看后端容器日志
   docker-compose logs -f backend
   ```

### 配置说明

1. **前端容器**: 基于Node.js构建Vue应用，并使用Nginx提供静态文件服务
2. **后端容器**: 基于Python运行API服务，包含所有必要的依赖
3. **数据共享**: 前端和后端容器共享`temp`目录，用于临时文件交换
4. **端口映射**: 前端映射到8080端口，后端映射到5556端口

如需修改配置，请编辑`docker-compose.yml`文件和相应的Dockerfile。