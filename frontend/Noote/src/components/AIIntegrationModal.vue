<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal-content" @click.stop>
      <h2>🤖 AI 筆記整合</h2>
      <p class="description">
        使用 AI 將合集中的 {{ noteCount }} 篇筆記整合成一份完整的統整筆記
      </p>

      <form @submit.prevent="handleIntegrate">
        <!-- API Key 輸入 -->
        <div class="form-group">
          <label>
            Google Gemini API Key *
            <a href="https://makersuite.google.com/app/apikey" target="_blank" class="help-link">
              (取得 API Key)
            </a>
          </label>
          <input
            v-model="apiKey"
            type="password"
            placeholder="輸入你的 Gemini API Key"
            required
          />
          <div class="form-hint">
            API Key 僅用於此次請求，不會被儲存到伺服器
          </div>
        </div>

        <!-- 自訂提示詞 -->
        <div class="form-group">
          <label>
            自訂提示詞（選填）
          </label>
          <textarea
            v-model="customPrompt"
            rows="4"
            placeholder="例如：請將這些筆記整理成考試複習重點，著重在關鍵概念和公式"
          ></textarea>
          <div class="form-hint">
            留空將使用預設提示詞：建立完整、結構清晰、易於複習的統整筆記
          </div>
        </div>

        <!-- 快速提示詞按鈕 -->
        <div class="quick-prompts">
          <span class="quick-prompts-label">快速選擇：</span>
          <button
            type="button"
            @click="setPrompt('考試複習')"
            class="quick-prompt-btn"
          >
            📝 考試複習
          </button>
          <button
            type="button"
            @click="setPrompt('快速參考')"
            class="quick-prompt-btn"
          >
            ⚡ 快速參考
          </button>
          <button
            type="button"
            @click="setPrompt('概念地圖')"
            class="quick-prompt-btn"
          >
            🗺️ 概念地圖
          </button>
        </div>

        <!-- 操作按鈕 -->
        <div class="modal-actions">
          <button
            type="button"
            @click="$emit('close')"
            class="cancel-btn"
            :disabled="loading"
          >
            取消
          </button>
          <button
            type="submit"
            class="submit-btn"
            :disabled="loading || !apiKey"
          >
            <span v-if="loading">⏳ 整合中...</span>
            <span v-else>🚀 開始整合</span>
          </button>
        </div>
      </form>

      <!-- 錯誤訊息 -->
      <div v-if="error" class="error-message">
        ⚠️ {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Props {
  noteCount: number
}

defineProps<Props>()

const emit = defineEmits<{
  close: []
  integrate: [apiKey: string, customPrompt?: string]
}>()

const apiKey = ref('')
const customPrompt = ref('')
const loading = ref(false)
const error = ref('')

const promptTemplates = {
  '考試複習': '請將這些課堂筆記整理成考試複習重點，包含：1) 每個章節的關鍵概念，2) 重要公式和定義，3) 常見考題類型。使用清晰的條列式格式。',
  '快速參考': '請將這些筆記整合成快速參考手冊（Cheat Sheet），只保留最核心的概念、語法和範例程式碼，用簡潔的表格和程式碼區塊呈現。',
  '概念地圖': '請將這些筆記整合並建立概念之間的關聯性，用階層式結構呈現主題之間的關係，並在相關概念之間加上連結說明。'
}

function setPrompt(template: keyof typeof promptTemplates) {
  customPrompt.value = promptTemplates[template]
}

function handleIntegrate() {
  if (!apiKey.value.trim()) {
    error.value = '請輸入 API Key'
    return
  }

  error.value = ''
  loading.value = true

  emit('integrate', apiKey.value, customPrompt.value || undefined)
}

defineExpose({
  setLoading: (value: boolean) => {
    loading.value = value
  },
  setError: (msg: string) => {
    error.value = msg
    loading.value = false
  }
})
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

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-content {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(30px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  padding: 2.5rem;
  border-radius: 24px;
  width: 90%;
  max-width: 640px;
  max-height: 85vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
  animation: slideUp 0.4s ease-out;
  position: relative;
}

.modal-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
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

h2 {
  margin: 0 0 0.75rem 0;
  font-size: 1.75rem;
  color: rgba(255, 255, 255, 0.95);
  font-weight: 700;
}

.description {
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 2rem;
  font-size: 0.875rem;
  line-height: 1.6;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.625rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.875rem;
}

.help-link {
  color: #90cdf4;
  font-weight: normal;
  font-size: 0.8125rem;
  text-decoration: none;
  margin-left: 8px;
}

.help-link:hover {
  text-decoration: underline;
  color: #63b3ed;
}

.form-group input[type="password"],
.form-group textarea {
  width: 100%;
  padding: 0.875rem 1rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 12px;
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.95);
  transition: all 0.3s ease;
  font-family: inherit;
  box-sizing: border-box;
}

.form-group input::placeholder,
.form-group textarea::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.form-group input[type="password"]:focus,
.form-group textarea:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(102, 126, 234, 0.5);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-hint {
  margin-top: 0.5rem;
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.5);
  line-height: 1.5;
}

.quick-prompts {
  margin-bottom: 2rem;
  padding: 1.25rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  align-items: center;
}

.quick-prompts-label {
  font-size: 0.8125rem;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 600;
}

.quick-prompt-btn {
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.8125rem;
  color: rgba(255, 255, 255, 0.9);
  transition: all 0.3s ease;
  font-weight: 500;
}

.quick-prompt-btn:hover {
  background: rgba(255, 255, 255, 0.12);
  border-color: rgba(102, 126, 234, 0.5);
  color: #90cdf4;
  transform: translateY(-1px);
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

.cancel-btn,
.submit-btn {
  padding: 0.9rem 1.75rem;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.cancel-btn {
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.8);
}

.cancel-btn:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.12);
  transform: translateY(-2px);
}

.submit-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.cancel-btn:disabled,
.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.error-message {
  margin-top: 1rem;
  padding: 1rem 1.25rem;
  background: rgba(252, 129, 129, 0.15);
  color: #fc8181;
  border-radius: 12px;
  font-size: 0.875rem;
  border-left: 4px solid #fc8181;
  backdrop-filter: blur(10px);
}
</style>
