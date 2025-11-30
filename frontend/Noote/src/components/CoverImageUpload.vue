<template>
  <div class="cover-upload">
    <label class="upload-label">封面圖片（可選）</label>

    <div class="preview-area" :style="previewStyle">
      <div v-if="!imageUrl" class="placeholder">
        <span class="icon">🖼️</span>
        <p>點擊選擇封面圖片</p>
        <p class="hint">或拖曳圖片到此處</p>
      </div>
      <div v-else class="preview-overlay">
        <button type="button" @click="removeImage" class="remove-btn">✕ 移除</button>
      </div>
    </div>

    <input
      ref="fileInput"
      type="file"
      accept="image/*"
      @change="handleFileChange"
      class="file-input"
    />

    <button type="button" @click="triggerUpload" class="upload-btn">
      {{ imageUrl ? '更換圖片' : '選擇圖片' }}
    </button>

    <div v-if="uploading" class="uploading">上傳中...</div>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface Props {
  modelValue?: string
}

const props = defineProps<Props>()
const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const fileInput = ref<HTMLInputElement | null>(null)
const imageUrl = ref(props.modelValue || '')
const uploading = ref(false)
const error = ref('')

const previewStyle = computed(() => {
  if (imageUrl.value) {
    return {
      backgroundImage: `url(${imageUrl.value})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center'
    }
  }
  return {}
})

function triggerUpload() {
  fileInput.value?.click()
}

async function handleFileChange(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]

  if (!file) return

  // 驗證文件類型
  if (!file.type.startsWith('image/')) {
    error.value = '請選擇圖片文件'
    return
  }

  // 驗證文件大小（限制 5MB）
  if (file.size > 5 * 1024 * 1024) {
    error.value = '圖片大小不能超過 5MB'
    return
  }

  error.value = ''

  // 轉換為 Base64 或上傳到服務器
  try {
    uploading.value = true

    // 方案1: 轉換為 Base64（簡單，但會增加數據大小）
    const reader = new FileReader()
    reader.onload = (e) => {
      const result = e.target?.result as string
      imageUrl.value = result
      emit('update:modelValue', result)
      uploading.value = false
    }
    reader.onerror = () => {
      error.value = '讀取圖片失敗'
      uploading.value = false
    }
    reader.readAsDataURL(file)

    // 方案2: 上傳到服務器（需要後端支援）
    // const formData = new FormData()
    // formData.append('file', file)
    // const response = await api.post('/collections/upload-cover', formData, {
    //   headers: { 'Content-Type': 'multipart/form-data' }
    // })
    // imageUrl.value = response.data.url
    // emit('update:modelValue', response.data.url)

  } catch (err) {
    error.value = '上傳失敗'
    uploading.value = false
  }
}

function removeImage() {
  imageUrl.value = ''
  emit('update:modelValue', '')
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}
</script>

<style scoped>
.cover-upload {
  margin-bottom: 1.5rem;
}

.upload-label {
  display: block;
  margin-bottom: 0.625rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.875rem;
}

.preview-area {
  width: 100%;
  height: 220px;
  border: 2px dashed rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}

.preview-area:hover {
  border-color: rgba(102, 126, 234, 0.5);
  background: rgba(255, 255, 255, 0.05);
}

.placeholder {
  text-align: center;
  color: rgba(255, 255, 255, 0.6);
}

.placeholder .icon {
  font-size: 3.5rem;
  display: block;
  margin-bottom: 0.75rem;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
}

.placeholder p {
  margin: 0.375rem 0;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 500;
}

.hint {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.4);
}

.preview-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.preview-area:hover .preview-overlay {
  opacity: 1;
}

.remove-btn {
  padding: 0.625rem 1.25rem;
  background: rgba(252, 129, 129, 0.9);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 10px;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 600;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.remove-btn:hover {
  background: rgba(252, 129, 129, 1);
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(252, 129, 129, 0.4);
}

.file-input {
  display: none;
}

.upload-btn {
  padding: 0.625rem 1.25rem;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.8), rgba(118, 75, 162, 0.8));
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 10px;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 600;
  transition: all 0.3s ease;
  backdrop-filter: blur(10px);
}

.upload-btn:hover {
  background: linear-gradient(135deg, #667eea, #764ba2);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

.uploading,
.error {
  margin-top: 0.625rem;
  font-size: 0.875rem;
  font-weight: 500;
}

.uploading {
  color: #90cdf4;
}

.error {
  color: #fc8181;
}
</style>
