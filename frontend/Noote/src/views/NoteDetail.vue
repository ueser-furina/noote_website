<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { notesService, type Note } from '../services/notes'
import { renderMarkdown } from '../utils/markdown'
import AddToCollectionModal from '../components/AddToCollectionModal.vue'
import { useUserStore } from '../stores/user'
import 'highlight.js/styles/github-dark.css'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const note = ref<Note | null>(null)
const loading = ref(true)
const error = ref('')
const showAddToCollectionModal = ref(false)

const renderedContent = computed(() => {
  if (!note.value) return ''
  if (note.value.file_type === 'md') {
    return renderMarkdown(note.value.content)
  }
  return `<pre>${note.value.content}</pre>`
})

onMounted(async () => {
  try {
    const noteId = parseInt(route.params.id as string)
    note.value = await notesService.getNote(noteId)
  } catch (err) {
    error.value = '載入筆記失敗'
  } finally {
    loading.value = false
  }
})

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleString('zh-TW')
}

function goBack() {
  router.back()
}

function openAddToCollectionModal() {
  if (!userStore.isLoggedIn) {
    alert('請先登入')
    router.push('/login')
    return
  }
  showAddToCollectionModal.value = true
}

function closeAddToCollectionModal() {
  showAddToCollectionModal.value = false
}

function onAddedToCollection() {
  alert('已添加到合集')
}
</script>

<template>
  <div class="note-detail-page">
    <!-- Background gradient overlay -->
    <div class="gradient-bg"></div>

    <!-- Floating elements -->
    <div class="floating-element" style="top: 10%; right: 5%">📖</div>
    <div class="floating-element" style="bottom: 15%; left: 8%">✍️</div>

    <div v-if="loading" class="loading">
      <div class="spinner-large"></div>
      <p>載入中...</p>
    </div>
    <div v-else-if="error" class="error">
      <span class="error-icon">⚠️</span>
      {{ error }}
    </div>
    <div v-else-if="note" class="note-container">
      <div class="note-header">
        <div class="header-actions">
          <button class="back-btn" @click="goBack">
            <span class="btn-icon">←</span> 返回
          </button>
          <button class="add-collection-btn" @click="openAddToCollectionModal">
            <span class="btn-icon">📚</span> 加入合集
          </button>
        </div>
        <div class="note-meta">
          <h1 class="note-title">{{ note.title }}</h1>
          <div class="meta-info">
            <span class="meta-badge">📝 {{ note.file_type.toUpperCase() }}</span>
            <span class="meta-badge">👤 {{ note.owner_username }}</span>
            <span class="meta-badge">📅 {{ formatDate(note.created_at!) }}</span>
          </div>
        </div>
      </div>

      <div class="note-content" v-html="renderedContent"></div>
    </div>

    <!-- 添加到合集彈窗 -->
    <AddToCollectionModal
      v-if="showAddToCollectionModal && note"
      :note-id="note.id!"
      @close="closeAddToCollectionModal"
      @added="onAddedToCollection"
    />
  </div>
</template>

<style scoped>
.note-detail-page {
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
  background: radial-gradient(circle at 15% 25%, rgba(102, 126, 234, 0.1) 0%, transparent 50%),
              radial-gradient(circle at 85% 75%, rgba(118, 75, 162, 0.1) 0%, transparent 50%);
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

.loading,
.error {
  position: relative;
  text-align: center;
  padding: 4rem 2rem;
  color: rgba(255, 255, 255, 0.8);
  z-index: 1;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.spinner-large {
  width: 48px;
  height: 48px;
  border: 4px solid rgba(255, 255, 255, 0.1);
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  color: #fc8181;
}

.error-icon {
  font-size: 2rem;
}

.note-container {
  position: relative;
  max-width: 900px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
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

.note-header {
  margin-bottom: 2.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.header-actions {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.back-btn,
.add-collection-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 600;
  backdrop-filter: blur(10px);
}

.back-btn {
  background: rgba(102, 126, 234, 0.2);
}

.back-btn:hover {
  background: rgba(102, 126, 234, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.add-collection-btn {
  background: linear-gradient(135deg, rgba(72, 187, 120, 0.8), rgba(56, 161, 105, 0.8));
}

.add-collection-btn:hover {
  background: linear-gradient(135deg, #48bb78, #38a169);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(72, 187, 120, 0.4);
}

.btn-icon {
  font-size: 1.2rem;
}

.note-meta {
  animation: fadeInDown 0.6s ease-out 0.2s backwards;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.note-title {
  margin-bottom: 1rem;
  color: rgba(255, 255, 255, 0.95);
  font-size: clamp(1.8rem, 4vw, 2.5rem);
  font-weight: 700;
}

.meta-info {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.meta-badge {
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.85rem;
  backdrop-filter: blur(10px);
}

.note-content {
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.85);
  animation: fadeInUp 0.6s ease-out 0.3s backwards;
  text-align: left !important;
}

.note-content * {
  text-align: left !important;
}

.note-content :deep(h1),
.note-content :deep(h2),
.note-content :deep(h3) {
  margin-top: 2rem;
  margin-bottom: 1rem;
  color: rgba(255, 255, 255, 0.95);
  font-weight: 600;
}

.note-content :deep(h1) {
  font-size: 2rem;
}

.note-content :deep(h2) {
  font-size: 1.6rem;
}

.note-content :deep(h3) {
  font-size: 1.3rem;
}

.note-content :deep(p) {
  margin-bottom: 1rem;
}

.note-content :deep(code) {
  background: rgba(102, 126, 234, 0.15);
  color: #a5b4fc;
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
  font-family: 'Courier New', monospace;
  font-size: 0.9em;
}

.note-content :deep(pre) {
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 1.25rem;
  border-radius: 12px;
  overflow-x: auto;
  margin: 1.5rem 0;
}

.note-content :deep(pre code) {
  background: none;
  color: #abb2bf;
  padding: 0;
}

.note-content :deep(ul),
.note-content :deep(ol) {
  margin-left: 2rem;
  margin-bottom: 1rem;
}

.note-content :deep(li) {
  margin-bottom: 0.5rem;
}

.note-content :deep(blockquote) {
  border-left: 4px solid #667eea;
  padding-left: 1.25rem;
  margin: 1.5rem 0;
  color: rgba(255, 255, 255, 0.7);
  font-style: italic;
  background: rgba(102, 126, 234, 0.05);
  padding: 1rem 1.25rem;
  border-radius: 0 8px 8px 0;
}

.note-content :deep(a) {
  color: #667eea;
  text-decoration: none;
  border-bottom: 1px solid rgba(102, 126, 234, 0.3);
  transition: all 0.3s;
}

.note-content :deep(a:hover) {
  color: #764ba2;
  border-bottom-color: #764ba2;
}

.note-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5rem 0;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 12px;
  overflow: hidden;
}

.note-content :deep(th),
.note-content :deep(td) {
  padding: 0.75rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.note-content :deep(th) {
  background: rgba(102, 126, 234, 0.2);
  color: rgba(255, 255, 255, 0.95);
  font-weight: 600;
}

@media (max-width: 768px) {
  .note-detail-page {
    padding: 1rem;
  }

  .note-container {
    padding: 1.5rem;
  }

  .header-actions {
    flex-direction: column;
  }

  .meta-info {
    flex-direction: column;
  }

  .floating-element {
    display: none;
  }
}
</style>
