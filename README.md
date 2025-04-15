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