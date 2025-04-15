<template>
  <div class="markdown-card" :style="cardStyle" :class="[getThemeClass()]">
    <div class="card-header">
      <div class="avatar">
        <img src="https://picsum.photos/48/48" alt="avatar" />
      </div>
      <div class="user-info">
        <span class="username">用户名</span>
        <span class="time">刚刚</span>
      </div>
    </div>
    <div class="card-content" v-html="renderedContent"></div>
    <div class="card-footer">
      <div class="actions">
        <span class="like">❤️ 点赞</span>
        <span class="comment">💬 评论</span>
        <span class="share">🔄 分享</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'
import emoji from 'markdown-it-emoji'
import sub from 'markdown-it-sub'
import sup from 'markdown-it-sup'
import mark from 'markdown-it-mark'
import taskLists from 'markdown-it-task-lists'
import container from 'markdown-it-container'
import footnote from 'markdown-it-footnote'
import abbr from 'markdown-it-abbr'
import ins from 'markdown-it-ins'
import katex from '@iktakahiro/markdown-it-katex'
import 'katex/dist/katex.min.css'

const props = defineProps({
  content: {
    type: String,
    required: true
  },
  theme: {
    type: Object,
    default: () => ({
      backgroundColor: '#ffffff',
      textColor: '#333333',
      borderColor: '#f0f0f0',
      fontFamily: 'sans-serif',
      fontSize: 16
    })
  },
  cardSize: {
    type: Object,
    default: () => ({
      width: 440,
      height: 586
    })
  }
})

const getThemeClass = () => {
  // 通过背景颜色判断主题
  if (props.theme.backgroundColor === '#fffbeb') return 'apple-memo-theme'
  if (props.theme.backgroundColor === '#f9f4ef') return 'art-deco-theme'
  if (props.theme.backgroundColor === '#ff6b6b') return 'pop-art-theme'
  if (props.theme.backgroundColor === '#f8f5e6') return 'retro-typewriter-theme'
  if (props.theme.backgroundColor === '#f7f7f7' && props.theme.borderColor === '#e83015') return 'japanese-mag-theme'
  return ''
}

const md = new MarkdownIt({
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(str, { language: lang }).value
      } catch (__) {}
    }
    return ''
  }
})
  .use(emoji)
  .use(sub)
  .use(sup)
  .use(mark)
  .use(taskLists)
  .use(container, 'warning')
  .use(footnote)
  .use(abbr)
  .use(ins)
  .use(katex)

const renderedContent = ref('')

const cardStyle = computed(() => ({
  backgroundColor: props.theme.backgroundColor,
  color: props.theme.textColor,
  borderColor: props.theme.borderColor,
  fontFamily: props.theme.fontFamily || 'sans-serif',
  fontSize: `${props.theme.fontSize}px`,
  width: '100%',
  height: '100%'
}))

watch(() => props.content, (newContent) => {
  renderedContent.value = md.render(newContent)
}, { immediate: true })
</script>

<style scoped>
.markdown-card {
  width: 100%;
  height: 100%;
  margin: 0;
  border-radius: 0;
  box-shadow: none;
  overflow: hidden;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid v-bind('theme.borderColor');
  background-color: v-bind('theme.backgroundColor');
  font-family: v-bind('theme.fontFamily || "sans-serif"');
  flex-shrink: 0;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 12px;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.username {
  font-weight: bold;
  font-size: 14px;
}

.time {
  font-size: 12px;
  color: #999;
}

.card-content {
  padding: 16px;
  line-height: 1.6;
  overflow-y: auto;
  background-color: v-bind('theme.backgroundColor');
  font-family: v-bind('theme.fontFamily || "sans-serif"');
  font-size: v-bind('theme.fontSize + "px"');
  flex: 1;
  text-align: left;
}

.card-footer {
  padding: 12px 16px;
  border-top: 1px solid v-bind('theme.borderColor');
  background-color: v-bind('theme.backgroundColor');
  font-family: v-bind('theme.fontFamily || "sans-serif"');
  flex-shrink: 0;
}

.actions {
  display: flex;
  gap: 20px;
}

.actions span {
  cursor: pointer;
  font-size: 14px;
}

:deep(pre) {
  background: #f6f8fa;
  padding: 16px;
  border-radius: 6px;
  overflow-x: auto;
  font-family: 'Courier New', Courier, monospace !important;
}

:deep(code) {
  font-family: 'Courier New', Courier, monospace !important;
}

:deep(img) {
  max-width: 100%;
  border-radius: 8px;
}

:deep(p) {
  margin: 0.5em 0;
  text-align: left;
  font-size: v-bind('theme.fontSize + "px"');
}

:deep(h1), :deep(h2), :deep(h3), :deep(h4), :deep(h5), :deep(h6) {
  margin-top: 1em;
  margin-bottom: 0.5em;
  font-weight: bold;
  font-family: v-bind('theme.fontFamily || "sans-serif"');
  text-align: left;
}

:deep(h1) { font-size: v-bind('theme.fontSize * 1.8 + "px"'); }
:deep(h2) { font-size: v-bind('theme.fontSize * 1.5 + "px"'); }
:deep(h3) { font-size: v-bind('theme.fontSize * 1.3 + "px"'); }
:deep(h4) { font-size: v-bind('theme.fontSize * 1.1 + "px"'); }
:deep(h5) { font-size: v-bind('theme.fontSize + "px"'); }
:deep(h6) { font-size: v-bind('theme.fontSize + "px"'); }

:deep(ul), :deep(ol) {
  padding-left: 2em;
  margin: 0.5em 0;
  text-align: left;
  font-size: v-bind('theme.fontSize + "px"');
}

:deep(li) {
  text-align: left;
  margin-bottom: 0.3em;
  font-size: v-bind('theme.fontSize + "px"');
}

:deep(blockquote) {
  margin: 0.5em 0;
  padding-left: 1em;
  border-left: 4px solid v-bind('theme.borderColor');
  color: #666;
  text-align: left;
  font-size: v-bind('theme.fontSize + "px"');
}

:deep(.task-list-item) {
  list-style-type: none;
}

:deep(.task-list-item-checkbox) {
  margin-right: 0.5em;
}

:deep(.emoji) {
  height: 1em;
  width: 1em;
  margin: 0 0.05em 0 0.1em;
  vertical-align: -0.1em;
}

:deep(.katex-display) {
  overflow-x: auto;
  overflow-y: hidden;
  padding: 1em 0;
}

/* 苹果备忘录主题 */
.apple-memo-theme {
  border-radius: 0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.apple-memo-theme :deep(p), 
.apple-memo-theme :deep(li) {
  line-height: 1.5;
  text-align: left;
}

.apple-memo-theme :deep(blockquote) {
  background-color: rgba(255, 224, 102, 0.2);
  border-left: 3px solid #ffe066;
  padding: 0.5em 1em;
  text-align: left;
}

/* 艺术字装饰主题 */
.art-deco-theme {
  border: 1px solid v-bind('theme.borderColor');
}

.art-deco-theme :deep(h1), 
.art-deco-theme :deep(h2) {
  text-transform: uppercase;
  letter-spacing: 2px;
  font-weight: bold;
  border-bottom: 2px solid v-bind('theme.borderColor');
  padding-bottom: 0.3em;
  text-align: left;
}

.art-deco-theme :deep(blockquote) {
  border-left: 3px solid #a48111;
  font-style: italic;
  text-align: left;
}

/* 波普艺术主题 */
.pop-art-theme {
  border-radius: 10px;
  overflow: hidden;
}

.pop-art-theme :deep(h1), 
.pop-art-theme :deep(h2),
.pop-art-theme :deep(h3) {
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #1d3557;
  text-shadow: 2px 2px 0px #ffd166;
  text-align: left;
}

.pop-art-theme :deep(strong) {
  background-color: #ffd166;
  padding: 0 5px;
}

.pop-art-theme :deep(img) {
  border: 5px solid #ffd166;
}

.pop-art-theme :deep(li) {
  text-align: left;
}

/* 复古打字机主题 */
.retro-typewriter-theme {
  border: none;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  background-image: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAQAAAAECAYAAACp8Z5+AAAAEklEQVQImWNgYGD4z0AswK4SAFXuAf8EPy+xAAAAAElFTkSuQmCC');
}

.retro-typewriter-theme :deep(*) {
  font-family: 'Courier New', Courier, monospace !important;
}

.retro-typewriter-theme :deep(p),
.retro-typewriter-theme :deep(li) {
  letter-spacing: -0.5px;
  line-height: 1.8;
  text-align: left;
}

.retro-typewriter-theme :deep(h1),
.retro-typewriter-theme :deep(h2),
.retro-typewriter-theme :deep(h3) {
  text-decoration: underline;
  text-align: left;
}

/* 日本杂志风格主题 */
.japanese-mag-theme {
  border: 1px solid transparent;
  padding: 0;
  overflow: hidden;
  position: relative;
  box-sizing: border-box;
  max-width: 100%;
}

.japanese-mag-theme .card-header {
  padding: 10px 12px;
  box-sizing: border-box;
  width: 100%;
  border-bottom: 1px solid #e0e0e0;
}

.japanese-mag-theme .card-footer {
  padding: 10px 12px;
  box-sizing: border-box;
  width: 100%;
  border-top: 1px solid #e0e0e0;
}

.japanese-mag-theme::before {
  content: 'STYLE';
  position: absolute;
  top: 8px;
  right: 8px;
  background-color: #000;
  color: #fff;
  padding: 1px 8px;
  font-size: 9px;
  font-weight: bold;
  letter-spacing: 1px;
  z-index: 10;
}

/* 减小代码块的内边距 */
.japanese-mag-theme :deep(pre) {
  padding: 12px;
  margin: 0.5em 0;
  max-width: 100%;
  overflow-x: auto;
  box-sizing: border-box;
}

/* 调整引用块的间距 */
.japanese-mag-theme :deep(blockquote) {
  border-left: none;
  position: relative;
  font-style: italic;
  padding: 8px 8px 8px 32px;
  background-color: #f9f9f9;
  color: #333;
  margin: 16px 0;
  text-align: left;
  box-sizing: border-box;
  width: 100%;
}

.japanese-mag-theme :deep(blockquote)::before {
  content: '"';
  font-family: Georgia, serif;
  position: absolute;
  left: 8px;
  top: 0;
  font-size: 50px;
  color: #000000;
  line-height: 1;
}

.japanese-mag-theme :deep(h1),
.japanese-mag-theme :deep(h2),
.japanese-mag-theme :deep(h3) {
  position: relative;
  padding-left: 10px;
  border-bottom: none;
  text-align: left;
  margin-top: 0.8em;
  margin-bottom: 0.8em;
  font-weight: 900;
  box-sizing: border-box;
  width: 100%;
}

.japanese-mag-theme :deep(h1)::before,
.japanese-mag-theme :deep(h2)::before,
.japanese-mag-theme :deep(h3)::before {
  content: '';
  position: absolute;
  left: 0;
  top: 5%;
  height: 90%;
  width: 4px;
  background-color: #000000;
}

/* 确保标题文本不会溢出 */
.japanese-mag-theme :deep(h1), 
.japanese-mag-theme :deep(h2), 
.japanese-mag-theme :deep(h3) {
  max-width: 100%;
  word-break: break-word;
  overflow-wrap: break-word;
}

.japanese-mag-theme :deep(strong) {
  color: v-bind('theme.borderColor');
  font-weight: 900;
  background-color: transparent;
  padding: 0;
}

.japanese-mag-theme :deep(p) {
  line-height: 1.6;
  margin: 0.4em 0;
  text-align: left;
  box-sizing: border-box;
  width: 100%;
}

.japanese-mag-theme :deep(ul) {
  list-style-type: none;
  padding-left: 1.8em;
  margin-top: 1em;
  box-sizing: border-box;
  width: 100%;
}

.japanese-mag-theme :deep(ul li) {
  position: relative;
  margin-bottom: 0.7em;
  text-align: left;
  padding-left: 0.3em;
  box-sizing: border-box;
}

.japanese-mag-theme :deep(ul li)::before {
  content: '';
  position: absolute;
  left: -0.8em;
  top: 0.7em;
  width: 5px;
  height: 5px;
  background-color: #000000;
}

.japanese-mag-theme :deep(ol) {
  counter-reset: custom-counter;
  list-style-type: none;
  padding-left: 2.2em;
  margin-top: 1em;
  position: relative;
  box-sizing: border-box;
  width: 100%;
}

.japanese-mag-theme :deep(ol)::after {
  content: '';
  position: absolute;
  left: 0.8em;
  top: 0;
  bottom: 0;
  width: 2px;
  background-color: v-bind('theme.borderColor');
}

.japanese-mag-theme :deep(ol li) {
  position: relative;
  counter-increment: custom-counter;
  margin-bottom: 0.7em;
  text-align: left;
  padding-left: 0.3em;
  box-sizing: border-box;
}

.japanese-mag-theme :deep(ol li)::before {
  content: counter(custom-counter);
  color: white;
  background-color: black;
  border-radius: 0;
  font-weight: bold;
  position: absolute;
  left: -1.8em;
  top: 0.15em;
  width: 20px;
  height: 20px;
  line-height: 20px;
  text-align: center;
  font-size: 11px;
}

/* 为列表项添加红色边框 */
.japanese-mag-theme :deep(ol) {
  position: relative;
}

.japanese-mag-theme :deep(ol)::after {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 2px;
  background-color: v-bind('theme.borderColor');
}

/* 为有序列表文本添加特殊样式 */
.japanese-mag-theme :deep(ol li) strong {
  font-size: 1.05em;
}

/* 为日本杂志风格主题的图片添加特殊边框 */
.japanese-mag-theme :deep(img) {
  max-width: 100%;
  border: 1px solid #e0e0e0;
  box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.1);
  margin: 10px auto;
  display: block;
  box-sizing: border-box;
}

.japanese-mag-theme .card-content {
  padding: 14px 12px;
  box-sizing: border-box;
  width: 100%;
  overflow-x: hidden;
}
</style> 