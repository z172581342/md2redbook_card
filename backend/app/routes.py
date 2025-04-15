from flask import Blueprint, request, jsonify
import asyncio
from .services.converter import FrontendScreenshotService

main = Blueprint('main', __name__)
# 初始化服务，根据实际前端地址配置
frontend_service = FrontendScreenshotService(frontend_url="http://localhost:5173")

@main.route('/api/convert', methods=['POST'])
async def convert_markdown():
    try:
        # 获取请求数据
        data = request.json
        markdown_text = data.get('markdown', '')
        style_config = data.get('style', {})
        
        # 样式配置参数
        theme = style_config.get('theme', 'default')
        font_size = style_config.get('fontSize', 16)
        width = style_config.get('width', 440)
        height = style_config.get('height', 1000)        
        # 调用转换服务
        image_data = await frontend_service.capture_markdown_preview(
            markdown_text,
            theme=theme,
            font_size=font_size,
            width=width,
            height=height
        )
        
        # 返回图片数据
        return jsonify({
            'success': True,
            'image': image_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@main.route('/api/health', methods=['GET'])
async def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'API is running'
    })