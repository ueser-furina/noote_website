<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { notesService } from '../services/notes'

const router = useRouter()
const route = useRoute()

const title = ref('')
const content = ref('')
const fileType = ref('md')
const isPublic = ref(true)
const loading = ref(false)
const error = ref('')

// 從 query 參數載入內容（用於 AI 整合結果）
onMounted(() => {
  if (route.query.title) {
    title.value = route.query.title as string
  }
  if (route.query.content) {
    content.value = route.query.content as string
    fileType.value = 'md' // AI 整合結果總是 Markdown
  }
})

async function handleSubmit() {
  if (!title.value || !content.value) {
    error.value = '請填寫標題和內容'
    return
  }

  loading.value = true
  error.value = ''

  try {
    await notesService.createNote({
      title: title.value,
      content: content.value,
      file_type: fileType.value,
      is_public: isPublic.value,
    })

    alert('筆記上傳成功！')
    router.push('/my-notes')
  } catch (err: any) {
    error.value = err.response?.data?.detail || '上傳失敗'
  } finally {
    loading.value = false
  }
}

function loadFromFile(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]

  if (!file) return

  const reader = new FileReader()
  reader.onload = (e) => {
    content.value = e.target?.result as string

    // 自動設定標題和檔案類型
    if (!title.value) {
      title.value = file.name.replace(/\.[^/.]+$/, '')
    }

    if (file.name.endsWith('.md')) {
      fileType.value = 'md'
    } else {
      fileType.value = 'txt'
    }
  }

  reader.readAsText(file)
}
</script>

<template>
  <div class="create-note-page">
    <!-- Background gradient overlay -->
    <div class="gradient-bg"></div>

    <!-- Floating elements -->
    <div class="floating-element" style="top: 8%; right: 12%">📄</div>
    <div class="floating-element" style="bottom: 12%; left: 10%">✏️</div>

    <div class="container">
      <div class="header">
        <h1 class="gradient-text">上傳筆記</h1>
        <router-link to="/my-notes" class="back-btn">
          <span class="btn-icon">←</span> 返回
        </router-link>
      </div>

      <form @submit.prevent="handleSubmit" class="note-form">
        <div class="form-group">
          <label for="title">筆記標題</label>
          <input
            id="title"
            v-model="title"
            type="text"
            placeholder="輸入筆記標題"
            required
          />
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="fileType">檔案類型</label>
            <select id="fileType" v-model="fileType">
              <option value="md">Markdown (.md)</option>
              <option value="txt">純文字 (.txt)</option>
            </select>
          </div>

          <div class="form-group">
            <label for="isPublic">可見性</label>
            <select id="isPublic" v-model="isPublic">
              <option :value="true">公開</option>
              <option :value="false">私密</option>
            </select>
          </div>
        </div>

        <div class="form-group">
          <label>從檔案載入</label>
          <div class="file-input-wrapper">
            <input type="file" accept=".md,.txt" @change="loadFromFile" id="file-input" />
            <label for="file-input" class="file-input-label">
              <span class="file-icon">📁</span>
              選擇檔案
            </label>
          </div>
          <small>支援 .md 和 .txt 檔案</small>
        </div>

        <div class="form-group">
          <label for="content">筆記內容</label>
          <textarea
            id="content"
            v-model="content"
            placeholder="輸入或貼上筆記內容，或使用上方的檔案載入功能"
            rows="20"
            required
          ></textarea>
        </div>

        <div v-if="error" class="error-message">
          <span class="error-icon">⚠️</span>
          {{ error }}
        </div>

        <div class="button-group">
          <button type="submit" class="submit-btn" :disabled="loading">
            <span v-if="!loading">
              <span class="btn-icon">💾</span> 上傳筆記
            </span>
            <span v-else class="loading-text">
              <span class="spinner"></span>
              上傳中...
            </span>
          </button>
          <button type="button" class="cancel-btn" @click="router.back()">取消</button>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.create-note-page {
  position: relative;
  min-height: 100vh;
  background: #000;
  padding: 2rem;
  overflow: hidden;
}

.gradient-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 25% 15%, rgba(102, 126, 234, 0.1) 0%, transparent 50%),
              radial-gradient(circle at 75% 85%, rgba(118, 75, 162, 0.1) 0%, transparent 50%);
  z-index: 0;
}

.floating-element {
  position: fixed;
  font-size: clamp(2rem, 4vw, 3rem);
  opacity: 0.2;
  animation: float 8s ease-in-out infinite;
  z-index: 0;
  pointer-events: none;
}

.floating-element:nth-child(2) {
  animation-delay: -4s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  25% {
    transform: translateY(-25px) rotate(5deg);
  }
  50% {
    transform: translateY(-15px) rotate(-5deg);
  }
  75% {
    transform: translateY(-20px) rotate(3deg);
  }
}

.container {
  position: relative;
  max-width: 900px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(30px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  padding: 2.5rem;
  border-radius: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  animation: fadeInUp 0.6s ease-out;
  z-index: 1;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.header h1 {
  font-size: clamp(1.8rem, 4vw, 2.3rem);
  font-weight: 700;
  margin: 0;
}

.gradient-text {
  background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
  background-size: 200% 200%;
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: gradientShift 3s ease infinite;
}

@keyframes gradientShift {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  background: rgba(102, 126, 234, 0.2);
  color: white;
  text-decoration: none;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  transition: all 0.3s;
  font-weight: 600;
}

.back-btn:hover {
  background: rgba(102, 126, 234, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.btn-icon {
  font-size: 1.2rem;
}

.note-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
  font-size: 0.9rem;
}

.form-group input[type='text'],
.form-group select,
.form-group textarea {
  padding: 0.9rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  font-size: 1rem;
  color: #fff;
  font-family: inherit;
  transition: all 0.3s;
}

.form-group textarea {
  resize: vertical;
  font-family: 'Courier New', monospace;
  line-height: 1.6;
}

.form-group input::placeholder,
.form-group textarea::placeholder {
  color: rgba(255, 255, 255, 0.3);
}

.form-group select {
  cursor: pointer;
}

.form-group select option {
  background: #1a1a1a;
  color: #fff;
}

.file-input-wrapper {
  position: relative;
}

.file-input-wrapper input[type='file'] {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.file-input-label {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.9rem 1.5rem;
  background: rgba(102, 126, 234, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.9);
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 500;
}

.file-input-label:hover {
  background: rgba(102, 126, 234, 0.3);
  transform: translateY(-2px);
}

.file-icon {
  font-size: 1.2rem;
}

.form-group small {
  margin-top: 0.5rem;
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.85rem;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.08);
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.error-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #fc8181;
  padding: 0.9rem;
  background: rgba(252, 129, 129, 0.1);
  border-radius: 12px;
  border: 1px solid rgba(252, 129, 129, 0.2);
  font-size: 0.9rem;
}

.error-icon {
  font-size: 1.2rem;
}

.button-group {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.submit-btn,
.cancel-btn {
  flex: 1;
  padding: 1rem 1.5rem;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.submit-btn {
  background: linear-gradient(135deg, #48bb78, #38a169);
  color: white;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(72, 187, 120, 0.4);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading-text {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.cancel-btn {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
}

.cancel-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .create-note-page {
    padding: 1rem;
  }

  .container {
    padding: 1.5rem;
  }

  .header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .button-group {
    flex-direction: column;
  }

  .floating-element {
    display: none;
  }
}
</style>
