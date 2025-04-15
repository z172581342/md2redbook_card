<template>
  <div class="theme-manager">
    <div class="theme-selector">
      <label>主题样式</label>
      <select v-model="selectedTheme" @change="changeTheme">
        <option value="light">浅色主题</option>
        <option value="dark">深色主题</option>
        <option value="pink">粉色主题</option>
        <option value="blue">蓝色主题</option>
        <option value="appleMemo">苹果备忘录</option>
        <option value="artDeco">艺术字装饰</option>
        <option value="popArt">波普艺术</option>
        <option value="retroTypewriter">复古打字机</option>
        <option value="japaneseMag">日本杂志风</option>
      </select>
    </div>
    
    <div class="font-size-control">
      <h3>文字大小</h3>
      <div class="font-size-slider">
        <label>基础文字大小</label>
        <input 
          type="range" 
          v-model.number="fontSize" 
          min="12" 
          max="24" 
          step="1"
          @input="updateFontSize"
        />
        <span class="font-size-value">{{ fontSize }}px</span>
      </div>
      <div class="preset-sizes">
        <button @click="setFontSize(14)" :class="{ active: fontSize === 14 }">小</button>
        <button @click="setFontSize(16)" :class="{ active: fontSize === 16 }">中</button>
        <button @click="setFontSize(18)" :class="{ active: fontSize === 18 }">大</button>
        <button @click="setFontSize(20)" :class="{ active: fontSize === 20 }">特大</button>
      </div>
    </div>
    
    <div class="size-manager">
      <h3>卡片尺寸</h3>
      <div class="size-inputs">
        <div class="size-input-group">
          <label>宽度 (px)</label>
          <input 
            type="number" 
            v-model.number="rawCardWidth" 
            @blur="updateCardSize"
          />
          <span class="size-hint" v-if="rawCardWidth < 200 || rawCardWidth > 1000">
            有效范围: 200-1000px
          </span>
        </div>
        <div class="size-input-group">
          <label>高度 (px)</label>
          <input 
            type="number" 
            v-model.number="rawCardHeight" 
            @blur="updateCardSize"
          />
          <span class="size-hint" v-if="rawCardHeight < 200 || rawCardHeight > 1000">
            有效范围: 200-1000px
          </span>
        </div>
      </div>
      <button class="reset-size-btn" @click="resetCardSize">重置尺寸</button>
    </div>
    
    <!--<div class="style-customizer">
      <h3>自定义颜色</h3>
      <div class="color-picker">
        <label>背景颜色</label>
        <chrome-picker v-model="customStyle.backgroundColor" @input="updateCustomStyle" />
      </div>
      <div class="color-picker">
        <label>文字颜色</label>
        <chrome-picker v-model="customStyle.textColor" @input="updateCustomStyle" />
      </div>
      <div class="color-picker">
        <label>边框颜色</label>
        <chrome-picker v-model="customStyle.borderColor" @input="updateCustomStyle" />
      </div>
    </div>-->
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { Chrome } from 'vue-color'

const emit = defineEmits(['themeChange', 'styleChange', 'sizeChange', 'fontSizeChange'])

const selectedTheme = ref('light')
const customStyle = reactive({
  backgroundColor: '#ffffff',
  textColor: '#333333',
  borderColor: '#f0f0f0',
  fontSize: 16
})

// 默认字体大小
const DEFAULT_FONT_SIZE = 16
const fontSize = ref(DEFAULT_FONT_SIZE)

// 默认卡片尺寸
const DEFAULT_WIDTH = 440
const DEFAULT_HEIGHT = 586

// 原始输入值 - 可以是任何数字
const rawCardWidth = ref(DEFAULT_WIDTH)
const rawCardHeight = ref(DEFAULT_HEIGHT)

// 限制在有效范围内的计算属性
const effectiveWidth = computed(() => {
  if (isNaN(rawCardWidth.value)) return DEFAULT_WIDTH
  return Math.min(Math.max(Number(rawCardWidth.value), 200), 1000)
})

const effectiveHeight = computed(() => {
  if (isNaN(rawCardHeight.value)) return DEFAULT_HEIGHT
  return Math.min(Math.max(Number(rawCardHeight.value), 200), 1000)
})

const themes = {
  light: {
    backgroundColor: '#ffffff',
    textColor: '#333333',
    borderColor: '#f0f0f0',
    fontSize: 16
  },
  dark: {
    backgroundColor: '#1a1a1a',
    textColor: '#ffffff',
    borderColor: '#333333',
    fontSize: 16
  },
  pink: {
    backgroundColor: '#fff0f5',
    textColor: '#ff1493',
    borderColor: '#ffb6c1',
    fontSize: 16
  },
  blue: {
    backgroundColor: '#f0f8ff',
    textColor: '#000080',
    borderColor: '#87ceeb',
    fontSize: 16
  },
  appleMemo: {
    backgroundColor: '#fffbeb',
    textColor: '#333333',
    borderColor: '#ffe066',
    fontFamily: 'SF Pro, -apple-system, BlinkMacSystemFont, sans-serif',
    fontSize: 16
  },
  artDeco: {
    backgroundColor: '#f9f4ef',
    textColor: '#2d2a32',
    borderColor: '#a48111',
    fontFamily: 'Georgia, serif',
    fontSize: 16
  },
  popArt: {
    backgroundColor: '#ff6b6b',
    textColor: '#1d3557',
    borderColor: '#ffd166',
    fontFamily: 'Impact, Charcoal, sans-serif',
    fontSize: 16
  },
  retroTypewriter: {
    backgroundColor: '#f8f5e6',
    textColor: '#3b3a30',
    borderColor: '#c3bfb6',
    fontFamily: 'Courier New, Courier, monospace',
    fontSize: 16
  },
  japaneseMag: {
    backgroundColor: '#f7f7f7',
    textColor: '#121212',
    borderColor: '#e83015',
    fontFamily: '"Hiragino Kaku Gothic Pro", "Meiryo", sans-serif',
    fontSize: 16
  }
}

const changeTheme = () => {
  const theme = themes[selectedTheme.value]
  Object.assign(customStyle, theme)
  fontSize.value = theme.fontSize
  emit('themeChange', theme)
}

const updateCustomStyle = () => {
  emit('styleChange', { ...customStyle })
}

const updateCardSize = () => {
  // 仅应用有效范围内的值，但不改变用户输入
  emit('sizeChange', { 
    width: effectiveWidth.value, 
    height: effectiveHeight.value 
  })
}

const resetCardSize = () => {
  rawCardWidth.value = DEFAULT_WIDTH
  rawCardHeight.value = DEFAULT_HEIGHT
  updateCardSize()
}

const updateFontSize = () => {
  customStyle.fontSize = fontSize.value
  emit('fontSizeChange', fontSize.value)
  emit('styleChange', { ...customStyle })
}

const setFontSize = (size) => {
  fontSize.value = size
  updateFontSize()
}
</script>

<style scoped>
.theme-manager {
  padding: 15px;
  background: transparent;
  border-radius: 0;
  margin-bottom: 0;
}

.theme-selector {
  margin-bottom: 15px;
}

.theme-selector label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
}

.theme-selector select {
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ddd;
  width: 100%;
}

.font-size-control {
  margin-bottom: 15px;
  padding-top: 15px;
  border-top: 1px solid #ddd;
}

.font-size-slider {
  margin-bottom: 10px;
}

.font-size-slider label {
  display: block;
  margin-bottom: 8px;
}

.font-size-slider input {
  width: 90%;
}

.font-size-value {
  display: inline-block;
  margin-top: 5px;
  font-weight: bold;
}

.preset-sizes {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
}

.preset-sizes button {
  flex: 1;
  padding: 6px;
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
  min-width: 40px;
}

.preset-sizes button.active {
  background-color: #e0e0e0;
  font-weight: bold;
}

.size-manager {
  margin-bottom: 15px;
  padding-top: 15px;
  border-top: 1px solid #ddd;
}

.size-inputs {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 10px;
}

.size-input-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.size-input-group label {
  font-weight: normal;
}

.size-input-group input {
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ddd;
  width: 100%;
}

.size-hint {
  font-size: 12px;
  color: #ff4d4f;
}

.reset-size-btn {
  padding: 6px 12px;
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  width: 100%;
}

.reset-size-btn:hover {
  background-color: #e0e0e0;
}

.style-customizer {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #ddd;
}

.color-picker {
  margin-bottom: 15px;
}

.color-picker label {
  display: block;
  margin-bottom: 8px;
}

.color-picker :deep(.vc-chrome) {
  width: 100% !important;
  box-shadow: none !important;
  border: 1px solid #ddd !important;
}

h3 {
  margin-bottom: 12px;
  color: #333;
  font-size: 15px;
}
</style> 