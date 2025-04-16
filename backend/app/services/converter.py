import asyncio
from playwright.async_api import async_playwright
import base64
import tempfile
import os
import urllib.parse

class FrontendScreenshotService:
    def __init__(self, frontend_url=None):
        """初始化服务
        
        Args:
            frontend_url: 前端应用的URL地址
        """
        # 优先使用传入的URL，否则使用环境变量，最后使用默认值
        self.frontend_url = frontend_url or os.getenv('FRONTEND_URL', 'http://localhost:2333')
        self.browser = None
        self.context = None
        
    async def initialize(self):
        """异步初始化浏览器"""
        if not self.browser:
            p = await async_playwright().start()
            # 尝试使用有中文字体支持的浏览器
            self.browser = await p.chromium.launch(headless=True)
            self.context = await self.browser.new_context(
                viewport={'width': 800, 'height': 600}
            )
            
            # 添加适用于所有页面的初始化脚本
            await self.context.add_init_script("""
                // 设置默认字体为中文优先
                if (document && document.documentElement) {
                    document.documentElement.style.fontFamily = 
                        "PingFang SC, Microsoft YaHei, Hiragino Sans GB, sans-serif";
                }
            """)
            
            # 添加markdown-it渲染配置修改脚本
            await self.context.add_init_script("""
                // 在全局window对象上添加一个标记，表示需要使用中文字体
                window.USE_CHINESE_FONT = true;
                
                // 监听可能的markdown-it实例创建
                const originalRender = window.markdownit;
                if (originalRender) {
                    window.markdownit = function(...args) {
                        const md = originalRender.apply(this, args);
                        // 修改渲染器的字体配置
                        if (md && md.renderer) {
                            const originalRenderToken = md.renderer.renderToken;
                            md.renderer.renderToken = function(...args) {
                                // 尝试添加中文字体
                                return originalRenderToken.apply(this, args);
                            };
                        }
                        return md;
                    };
                }
            """);

    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
            self.browser = None
            self.context = None

    async def capture_markdown_preview(self, markdown_text, theme='default', font_size=16, width=440, height=586):
        """访问前端页面并截取Markdown预览的图片
        
        Args:
            markdown_text: Markdown文本内容
            theme: 主题样式
            font_size: 字体大小
            width: 卡片宽度（像素）
            height: 卡片高度（像素）
        
        Returns:
            image_base64: Base64编码的图片数据
        """
        
        await self.initialize()
        
        try:
            # 创建新页面
            page = await self.context.new_page()
            
            try:
                # 访问前端应用的主页
                await page.goto(self.frontend_url)
                
                # 等待内容加载完成
                await page.wait_for_load_state('networkidle')
                
                # 等待编辑器和预览元素加载完成
                await page.wait_for_selector('.markdown-editor', state='visible')
                await page.wait_for_selector('.card-container', state='visible')
                
                # 1. 使用JavaScript设置Markdown内容，解决编码问题
                js_code = f"""
                   const editor = document.querySelector('.markdown-editor');
                   if (editor) {{
                       editor.value = {repr(markdown_text)};
                       // 触发input事件以确保内容更新
                       editor.dispatchEvent(new Event('input', {{ bubbles: true }}));
                   }}
                """
                
                await page.evaluate(js_code)
                
                # 2. 设置主题 - 这里需要根据前端ThemeManager组件的实际操作方式调整
                # 根据选择的主题设置对应的选项
                theme_map = {
                    'light': '浅色主题',
                    'dark': '深色主题', 
                    'pink': '粉色主题',
                    'blue': '蓝色主题',
                    'appleMemo': '苹果备忘录',
                    'artDeco': '艺术字装饰',
                    'popArt': '波普艺术',
                    'retroTypewriter': '复古打字机',
                    'japaneseMag': '日本杂志风'
                }
                
                if theme in theme_map:
                    # 使用正确的CSS选择器定位select元素
                    await page.select_option('.theme-selector select', theme)
                else:
                    # 默认使用浅色主题
                    await page.select_option('.theme-selector select', 'light')
                
                # 3. 设置字体大小
                # 假设前端有个字体大小调整滑块，可以通过设置输入值或选择预设选项
                await page.fill('input[type="range"]', str(font_size))
                
                # 4. 设置卡片尺寸
                # 根据传入的width和height参数设置
                try:
                    width_input = await page.query_selector('.size-input-group:first-child input[type="number"]')
                    height_input = await page.query_selector('.size-input-group:last-child input[type="number"]')
                    
                    if width_input:
                        width = max(200, min(1000, width))
                        await width_input.fill(str(width))
                        # 按下Tab键触发失焦事件
                        await width_input.press("Tab")
                    
                    if height_input:
                        height = max(200, min(1000, height))
                        await height_input.fill(str(height))
                        # 按下Enter键确认输入
                        await height_input.press("Enter")
                    
                    # 点击页面其他区域确保失焦事件触发
                    await page.click('.theme-manager')
                    
                    # 等待一小段时间确保尺寸更新已应用
                    await page.wait_for_timeout(1000)
                        
                except Exception as e:
                    print(f"设置卡片尺寸失败: {str(e)}")
                
                # 等待一段时间确保渲染完成
                await page.wait_for_timeout(5000)
                
                # 获取卡片容器并截图
                card_container = page.locator('.card-container')
                
                # 截图
                screenshot = await card_container.screenshot(
                    type='png',
                    scale='device'
                )
                
                # 转换为Base64
                image_base64 = base64.b64encode(screenshot).decode('utf-8')
                
                return image_base64
                
            finally:
                await page.close()
                
        except Exception as e:
            # 捕获并记录错误
            print(f"截图过程出错: {str(e)}")
            raise e