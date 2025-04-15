<script setup>
import { ref, onMounted, computed } from 'vue'
import MarkdownCard from './components/MarkdownCard.vue'
import ThemeManager from './components/ThemeManager.vue'
import html2canvas from 'html2canvas'

const defaultMarkdown = `# MD2Card

> MD2Card 是一个 markdown 转知识卡片工具，可以让你用 Markdown 制作优雅的图文海报。 🌟

![](https://picsum.photos/600/300)

## 它的主要功能：

1. 将 Markdown 转化为**图文海报**
2. 多种主题风格任你选择
3. 长文自动拆分，或者根据 markdown \`---\` 横线拆分
4. 可以复制图片到\`剪贴板\`，或者下载为\`PNG\`、\`SVG\`图片
5. 所见即所得`

const markdownContent = ref('')
const fileInput = ref(null)
const imageInput = ref(null)
const cardRef = ref(null)
const currentTheme = ref({
  backgroundColor: '#ffffff',
  textColor: '#333333',
  borderColor: '#f0f0f0',
  fontSize: 16
})

// 原始卡片尺寸
const rawCardSize = ref({
  width: 440,
  height: 586
})

// 有效的卡片尺寸（用于应用样式）
const effectiveCardSize = computed(() => {
  return {
    width: rawCardSize.value.width,
    height: rawCardSize.value.height
  }
})

// 在组件挂载时设置默认 Markdown 内容
onMounted(() => {
  markdownContent.value = defaultMarkdown
})

const triggerFileUpload = () => {
  fileInput.value.click()
}

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      markdownContent.value = e.target.result
    }
    reader.readAsText(file)
  }
}

const triggerImageUpload = () => {
  imageInput.value.click()
}

const handleImageUpload = (event) => {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      const imageUrl = e.target.result
      const imageMarkdown = `![${file.name}](${imageUrl})`
      const cursorPos = markdownContent.value.length
      markdownContent.value = markdownContent.value.slice(0, cursorPos) + '\n' + imageMarkdown + '\n'
    }
    reader.readAsDataURL(file)
  }
}

const exportAsImage = async () => {
  if (cardRef.value) {
    // 等待所有图片加载完成
    const images = cardRef.value.$el.getElementsByTagName('img')
    const imageLoadPromises = Array.from(images).map(img => {
      if (img.complete) return Promise.resolve()
      return new Promise(resolve => {
        img.onload = resolve
        img.onerror = resolve
      })
    })
    
    await Promise.all(imageLoadPromises)
    
    const canvas = await html2canvas(cardRef.value.$el, {
      useCORS: true,
      allowTaint: true,
      backgroundColor: null
    })
    const link = document.createElement('a')
    link.download = '小红书卡片.png'
    link.href = canvas.toDataURL()
    link.click()
  }
}

const handleThemeChange = (theme) => {
  currentTheme.value = theme
}

const handleStyleChange = (style) => {
  currentTheme.value = style
}

const handleSizeChange = (size) => {
  rawCardSize.value = size
}

const handleFontSizeChange = (fontSize) => {
  currentTheme.value.fontSize = fontSize
}
</script>

<template>
  <div class="app">
    <h1>Markdown 转小红书卡片</h1>
    <div class="toolbar">
      <div class="file-upload">
        <input
          type="file"
          accept=".md,.markdown"
          @change="handleFileUpload"
          ref="fileInput"
          style="display: none"
        />
        <button @click="triggerFileUpload" class="upload-btn">上传 Markdown 文件</button>
      </div>
      <div class="image-upload">
        <input
          type="file"
          accept="image/*"
          @change="handleImageUpload"
          ref="imageInput"
          style="display: none"
        />
        <button @click="triggerImageUpload" class="upload-btn">上传图片</button>
      </div>
      <button @click="exportAsImage" class="export-btn">导出为图片</button>
    </div>
    <div class="main-container">
      <div class="content-area">
        <div class="editor-section">
          <div class="section-header">Markdown 编辑</div>
          <textarea
            v-model="markdownContent"
            placeholder="在这里输入 Markdown 内容..."
            class="markdown-editor"
          ></textarea>
        </div>
        <div class="preview-section">
          <div class="section-header">小红书卡片预览</div>
          <div class="card-container" :style="{ width: effectiveCardSize.width + 'px', height: effectiveCardSize.height + 'px' }">
            <MarkdownCard 
              :content="markdownContent" 
              :theme="currentTheme" 
              :cardSize="effectiveCardSize" 
              ref="cardRef"
            />
          </div>
        </div>
      </div>
      <div class="settings-panel">
        <div class="settings-header">卡片设置</div>
        <ThemeManager 
          @themeChange="handleThemeChange" 
          @styleChange="handleStyleChange"
          @sizeChange="handleSizeChange"
          @fontSizeChange="handleFontSizeChange"
        />
      </div>
    </div>
  </div>
</template>

<style>
.app {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
}

.toolbar {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 20px;
}

.upload-btn, .export-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  background-color: #409eff;
  color: white;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.upload-btn:hover, .export-btn:hover {
  background-color: #66b1ff;
}

.main-container {
  display: flex;
  gap: 20px;
}

.content-area {
  flex: 3;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  align-items: flex-start;
}

.settings-panel {
  flex: 1;
  min-width: 300px;
  border: 1px solid var(--border-color, #ddd);
  border-radius: 8px;
  background-color: var(--panel-bg-color, #f9f9f9);
  overflow: hidden;
}

.settings-header {
  background-color: var(--header-bg-color, #f0f0f0);
  padding: 10px 15px;
  font-weight: bold;
  border-bottom: 1px solid var(--border-color, #ddd);
}

.editor-section, .preview-section {
  border: 1px solid var(--border-color, #ddd);
  border-radius: 8px;
  background-color: var(--panel-bg-color, #f9f9f9);
  overflow: hidden;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.section-header {
  background-color: var(--header-bg-color, #f0f0f0);
  padding: 10px 15px;
  font-weight: bold;
  border-bottom: 1px solid var(--border-color, #ddd);
  flex-shrink: 0;
}

.markdown-editor {
  width: 100%;
  height: 100%;
  min-height: 500px;
  padding: 15px;
  border: none;
  font-family: monospace;
  resize: none;
  font-size: 14px;
  line-height: 1.6;
  background-color: var(--input-bg-color, #fff);
  color: var(--text-color, #333);
  flex: 1;
}

.markdown-editor:focus {
  outline: none;
}

.card-container {
  margin: 20px auto;
  overflow: auto;
  background-color: var(--card-bg-color, #fff);
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  max-width: 100%;
}

.preview-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}

:root {
  --border-color: #ddd;
  --panel-bg-color: #f9f9f9;
  --header-bg-color: #f0f0f0;
  --input-bg-color: #fff;
  --card-bg-color: #fff;
  --text-color: #333;
}

@media (prefers-color-scheme: dark) {
  :root {
    --border-color: #444;
    --panel-bg-color: #333;
    --header-bg-color: #2a2a2a;
    --input-bg-color: #222;
    --card-bg-color: #2a2a2a;
    --text-color: #eee;
  }
}

@media (max-width: 1200px) {
  .main-container {
    flex-direction: column;
  }
  
  .settings-panel {
    min-width: 100%;
  }
}

@media (max-width: 768px) {
  .content-area {
    grid-template-columns: 1fr;
  }
}
</style>
