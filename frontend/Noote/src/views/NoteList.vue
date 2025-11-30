<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { notesService, type Note } from '../services/notes'
import SearchBar from '../components/SearchBar.vue'
import NoteCard from '../components/NoteCard.vue'

const router = useRouter()
const notes = ref<Note[]>([])
const loading = ref(true)
const error = ref('')
const searchQuery = ref('')
const isSearching = ref(false)

onMounted(async () => {
  await loadNotes()
})

async function loadNotes() {
  try {
    loading.value = true
    notes.value = await notesService.getPublicNotes()
  } catch (err) {
    error.value = '載入筆記失敗'
  } finally {
    loading.value = false
  }
}

async function handleSearch(query: string) {
  searchQuery.value = query

  if (!query) {
    // 清空搜尋，載入所有公開筆記
    isSearching.value = false
    await loadNotes()
    return
  }

  try {
    loading.value = true
    isSearching.value = true
    notes.value = await notesService.searchNotes(query, 'public')
  } catch (err) {
    error.value = '搜尋失敗'
  } finally {
    loading.value = false
  }
}

function viewNote(id: number) {
  router.push(`/notes/${id}`)
}
</script>

<template>
  <div class="note-list-page">
    <!-- Background gradient overlay -->
    <div class="gradient-bg"></div>

    <!-- Floating elements -->
    <div class="floating-element" style="top: 8%; left: 10%">📝</div>
    <div class="floating-element" style="top: 50%; right: 8%">🌐</div>
    <div class="floating-element" style="bottom: 15%; left: 12%">✨</div>

    <div class="header">
      <h1 class="gradient-text">公開筆記</h1>
      <router-link to="/" class="back-btn">
        <span class="btn-icon">←</span> 返回首頁
      </router-link>
    </div>

    <div class="search-container">
      <SearchBar @search="handleSearch" placeholder="搜尋公開筆記..." />
      <div v-if="isSearching" class="search-info">
        搜尋結果：{{ notes.length }} 篇筆記
      </div>
    </div>

    <div v-if="loading" class="loading">
      <div class="spinner-large"></div>
      <p>載入中...</p>
    </div>
    <div v-else-if="error" class="error">
      <span class="error-icon">⚠️</span>
      {{ error }}
    </div>
    <div v-else-if="notes.length === 0" class="empty">
      <div class="empty-icon">📭</div>
      <p>{{ isSearching ? '沒有找到符合的筆記' : '目前沒有公開筆記' }}</p>
    </div>
    <div v-else class="note-list">
      <div v-for="note in notes" :key="note.id" class="note-card-wrapper">
        <NoteCard
          :note="note"
          :search-query="searchQuery"
          @click="viewNote(note.id!)"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.note-list-page {
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
  background: radial-gradient(circle at 20% 20%, rgba(102, 126, 234, 0.1) 0%, transparent 50%),
              radial-gradient(circle at 80% 80%, rgba(118, 75, 162, 0.1) 0%, transparent 50%);
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
  animation-delay: -3s;
}

.floating-element:nth-child(3) {
  animation-delay: -6s;
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

.header {
  position: relative;
  max-width: 1200px;
  margin: 0 auto 2.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  animation: fadeInDown 0.6s ease-out;
  z-index: 1;
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

.header h1 {
  font-size: clamp(2rem, 5vw, 2.5rem);
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
  transition: all 0.3s;
  font-weight: 600;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.back-btn:hover {
  background: rgba(102, 126, 234, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.btn-icon {
  font-size: 1.2rem;
}

.search-container {
  position: relative;
  max-width: 1200px;
  margin: 0 auto 2rem;
  animation: fadeInUp 0.6s ease-out 0.1s backwards;
  z-index: 1;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.search-info {
  margin-top: 10px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 14px;
  text-align: center;
}

.loading,
.error,
.empty {
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

.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.empty-icon {
  font-size: 4rem;
  opacity: 0.5;
}

.empty p {
  font-size: 1.2rem;
  margin: 0;
}

.note-list {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
  z-index: 1;
}

.note-card-wrapper {
  position: relative;
  margin-bottom: 1.5rem;
  animation: fadeInUp 0.5s ease-out backwards;
}

.note-card-wrapper:nth-child(1) {
  animation-delay: 0.1s;
}
.note-card-wrapper:nth-child(2) {
  animation-delay: 0.15s;
}
.note-card-wrapper:nth-child(3) {
  animation-delay: 0.2s;
}
.note-card-wrapper:nth-child(4) {
  animation-delay: 0.25s;
}
.note-card-wrapper:nth-child(5) {
  animation-delay: 0.3s;
}

@media (max-width: 768px) {
  .note-list-page {
    padding: 1rem;
  }

  .header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .floating-element {
    display: none;
  }
}
</style>
