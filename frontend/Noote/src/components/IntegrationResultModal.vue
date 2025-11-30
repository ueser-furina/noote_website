<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2>✨ 整合完成</h2>
        <button @click="$emit('close')" class="close-btn">✕</button>
      </div>

      <div class="result-info">
        <span>📊 整合了 {{ result.note_count }} 篇筆記</span>
        <span>🕐 {{ formatDate(result.created_at) }}</span>
      </div>

      <!-- 操作按鈕 -->
      <div class="action-buttons">
        <button @click="copyToClipboard" class="action-btn copy-btn">
          <span v-if="copied">✓ 已複製</span>
          <span v-else>📋 複製內容</span>
        </button>
        <button @click="saveAsNote" class="action-btn save-btn">
          💾 儲存為筆記
        </button>
        <button @click="downloadMarkdown" class="action-btn download-btn">
          ⬇️ 下載 Markdown
        </button>
      </div>

      <!-- Markdown 預覽 -->
      <div class="preview-section">
        <div class="preview-header">
          <h3>預覽</h3>
          <button @click="toggleView" class="toggle-btn">
            {{ showRaw ? '顯示渲染' : '顯示原始碼' }}
          </button>
        </div>
        <div v-if="showRaw" class="raw-content">
          <pre>{{ result.integrated_content }}</pre>
        </div>
        <div v-else class="rendered-content" v-html="renderedContent"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { marked } from 'marked'
import type { IntegrationResponse } from '../services/collections'

interface Props {
  result: IntegrationResponse
}

const props = defineProps<Props>()
const emit = defineEmits<{
  close: []
}>()

const router = useRouter()
const showRaw = ref(false)
const copied = ref(false)

const renderedContent = computed(() => {
  return marked(props.result.integrated_content)
})

function toggleView() {
  showRaw.value = !showRaw.value
}

async function copyToClipboard() {
  try {
    await navigator.clipboard.writeText(props.result.integrated_content)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (err) {
    alert('複製失敗，請手動複製')
  }
}

function downloadMarkdown() {
  const blob = new Blob([props.result.integrated_content], {
    type: 'text/markdown'
  })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `integrated_note_${Date.now()}.md`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

function saveAsNote() {
  // 關閉當前彈窗並導航到建立筆記頁面，帶上整合內容
  emit('close')
  router.push({
    name: 'create-note',
    query: {
      content: props.result.integrated_content,
      title: `整合筆記 - ${new Date().toLocaleDateString()}`
    }
  })
}

function formatDate(dateString: string) {
  const date = new Date(dateString)
  return date.toLocaleString('zh-TW', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  animation: fadeIn 0.3s ease-out;
}

.modal-content {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(30px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 24px;
  width: 95%;
  max-width: 1200px;
  height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  animation: slideUp 0.4s ease-out;
  position: relative;
  overflow: hidden;
}

.modal-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  z-index: 1;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    transform: translateY(30px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(255, 255, 255, 0.03);
}

.modal-header h2 {
  margin: 0;
  font-size: 1.75rem;
  color: rgba(255, 255, 255, 0.95);
  font-weight: 700;
}

.close-btn {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  font-size: 20px;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  padding: 0;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.95);
  transform: scale(1.1);
}

.result-info {
  padding: 1rem 2rem;
  background: rgba(255, 255, 255, 0.03);
  display: flex;
  gap: 2rem;
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.7);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.action-buttons {
  padding: 1rem 2rem;
  display: flex;
  gap: 0.75rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  flex-wrap: wrap;
  background: rgba(255, 255, 255, 0.02);
}

.action-btn {
  padding: 0.625rem 1.25rem;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 10px;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 600;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  backdrop-filter: blur(10px);
}

.copy-btn {
  background: rgba(66, 153, 225, 0.15);
  color: #90cdf4;
}

.copy-btn:hover {
  background: rgba(66, 153, 225, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(66, 153, 225, 0.3);
}

.save-btn {
  background: rgba(72, 187, 120, 0.15);
  color: #9ae6b4;
}

.save-btn:hover {
  background: rgba(72, 187, 120, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(72, 187, 120, 0.3);
}

.download-btn {
  background: rgba(237, 137, 54, 0.15);
  color: #fbd38d;
}

.download-btn:hover {
  background: rgba(237, 137, 54, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(237, 137, 54, 0.3);
}

.preview-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.preview-header {
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.03);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.preview-header h3 {
  margin: 0;
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 600;
}

.toggle-btn {
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.8125rem;
  color: rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
  font-weight: 500;
}

.toggle-btn:hover {
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(102, 126, 234, 0.5);
  color: #90cdf4;
}

.raw-content,
.rendered-content {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
  text-align: left;
  background: rgba(0, 0, 0, 0.2);
}

.raw-content pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
  font-size: 0.8125rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.9);
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1.5rem;
  border-radius: 12px;
}

.rendered-content {
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.9);
  max-width: 900px;
}

.rendered-content * {
  text-align: left !important;
}

.rendered-content :deep(h1) {
  font-size: 1.75rem;
  margin-top: 2rem;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid rgba(255, 255, 255, 0.15);
  text-align: left;
  color: rgba(255, 255, 255, 0.95);
  font-weight: 700;
}

.rendered-content :deep(h2) {
  font-size: 1.5rem;
  margin-top: 1.75rem;
  margin-bottom: 0.875rem;
  color: rgba(255, 255, 255, 0.9);
  text-align: left;
  font-weight: 700;
}

.rendered-content :deep(h3) {
  font-size: 1.25rem;
  margin-top: 1.5rem;
  margin-bottom: 0.625rem;
  color: rgba(255, 255, 255, 0.85);
  text-align: left;
  font-weight: 600;
}

.rendered-content :deep(p) {
  margin-bottom: 1rem;
  text-align: left;
  color: rgba(255, 255, 255, 0.8);
}

.rendered-content :deep(ul),
.rendered-content :deep(ol) {
  margin-bottom: 1rem;
  padding-left: 2rem;
  text-align: left;
  color: rgba(255, 255, 255, 0.8);
}

.rendered-content :deep(li) {
  margin-bottom: 0.5rem;
  text-align: left;
}

.rendered-content :deep(code) {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.15);
  padding: 3px 8px;
  border-radius: 6px;
  font-family: 'Monaco', 'Menlo', 'Consolas', monospace;
  font-size: 0.875em;
  color: #fbbf24;
}

.rendered-content :deep(pre) {
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #f8f8f2;
  padding: 1.5rem;
  border-radius: 12px;
  overflow-x: auto;
  margin-bottom: 1.5rem;
}

.rendered-content :deep(pre code) {
  background: none;
  border: none;
  padding: 0;
  color: inherit;
}

.rendered-content :deep(blockquote) {
  border-left: 4px solid rgba(102, 126, 234, 0.6);
  padding-left: 1.25rem;
  color: rgba(255, 255, 255, 0.7);
  margin: 1.5rem 0;
  text-align: left;
  background: rgba(255, 255, 255, 0.03);
  padding: 1rem 1.25rem;
  border-radius: 0 8px 8px 0;
}

.rendered-content :deep(table) {
  border-collapse: collapse;
  width: 100%;
  margin-bottom: 1.5rem;
  text-align: left;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 8px;
  overflow: hidden;
}

.rendered-content :deep(th),
.rendered-content :deep(td) {
  border: 1px solid rgba(255, 255, 255, 0.15);
  padding: 0.875rem;
  text-align: left;
}

.rendered-content :deep(th) {
  background: rgba(255, 255, 255, 0.08);
  font-weight: 700;
  color: rgba(255, 255, 255, 0.95);
}

.rendered-content :deep(td) {
  color: rgba(255, 255, 255, 0.8);
}

.rendered-content :deep(a) {
  color: #90cdf4;
  text-decoration: none;
  border-bottom: 1px solid rgba(144, 205, 244, 0.3);
  transition: all 0.3s ease;
}

.rendered-content :deep(a:hover) {
  color: #63b3ed;
  border-bottom-color: rgba(99, 179, 237, 0.6);
}
</style>
