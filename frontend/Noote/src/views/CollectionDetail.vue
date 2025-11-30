<template>
  <div class="collection-detail-page">
    <!-- Background gradient overlay -->
    <div class="gradient-bg"></div>

    <!-- Floating elements -->
    <div class="floating-element" style="top: 5%; left: 8%">📚</div>
    <div class="floating-element" style="bottom: 10%; right: 12%">✨</div>

    <div v-if="loading" class="loading">
      <div class="spinner-large"></div>
      <p>載入中...</p>
    </div>
    <div v-else-if="error" class="error">
      <span class="error-icon">⚠️</span>
      {{ error }}
    </div>
    <div v-else>
      <!-- 合集資訊 -->
      <div class="collection-header">
        <div class="collection-cover" :style="coverStyle">
          <div v-if="!collection.cover_image" class="default-cover">📚</div>
        </div>
        <div class="collection-info">
          <h1 class="collection-title">{{ collection.name }}</h1>
          <p class="description">{{ collection.description }}</p>
          <div class="meta">
            <span class="meta-badge">👤 {{ collection.owner_username }}</span>
            <span class="meta-badge">📝 {{ notes.length }} 篇筆記</span>
            <span v-if="collection.is_public" class="badge public">🌐 公開</span>
            <span v-else class="badge private">🔒 私密</span>
          </div>
          <div class="actions">
            <router-link to="/collections/public" class="action-btn back-btn">
              <span class="btn-icon">←</span> 返回列表
            </router-link>
            <button
              v-if="notes.length > 0"
              @click="showIntegrationModal = true"
              class="action-btn integrate-btn"
            >
              <span class="btn-icon">🤖</span> AI 整合筆記
            </button>
            <button v-if="isOwner" @click="enableSorting = !enableSorting" class="action-btn sort-btn">
              <span class="btn-icon">{{ enableSorting ? '✅' : '🔄' }}</span>
              {{ enableSorting ? '完成排序' : '排序筆記' }}
            </button>
            <button v-if="isOwner" @click="openEditModal" class="action-btn edit-btn">
              <span class="btn-icon">✏️</span> 編輯
            </button>
            <button v-if="isOwner" @click="deleteCollection" class="action-btn delete-btn">
              <span class="btn-icon">🗑️</span> 刪除
            </button>
          </div>
        </div>
      </div>

      <!-- 筆記列表 -->
      <div class="notes-section">
        <h2 class="section-title">
          <span class="gradient-text">筆記列表</span>
        </h2>
        <div v-if="notes.length === 0" class="empty">
          <div class="empty-icon">📭</div>
          <p>此合集暫無筆記</p>
        </div>
        <div v-else class="notes-list" :class="{ sortable: enableSorting }">
          <div
            v-for="(note, index) in notes"
            :key="note.id"
            class="note-item"
            :draggable="enableSorting"
            @dragstart="handleDragStart(index)"
            @dragover.prevent
            @drop="handleDrop(index)"
          >
            <div class="drag-handle" v-if="enableSorting">⋮⋮</div>
            <NoteCard :note="note" @click="viewNote(note.id!)" />
            <button v-if="isOwner" @click="removeNote(note.id!)" class="remove-btn">
              <span class="btn-icon">✖</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 編輯合集彈窗 -->
    <div v-if="showEditModal" class="modal-overlay" @click="closeEditModal">
      <div class="modal-content" @click.stop>
        <h2 class="modal-title">編輯合集</h2>
        <form @submit.prevent="updateCollection">
          <CoverImageUpload v-model="editForm.cover_image" />

          <div class="form-group">
            <label>合集名稱 *</label>
            <input v-model="editForm.name" type="text" required />
          </div>
          <div class="form-group">
            <label>描述</label>
            <textarea v-model="editForm.description" rows="4"></textarea>
          </div>
          <div class="form-group checkbox-group">
            <label class="checkbox-label">
              <input v-model="editForm.is_public" type="checkbox" />
              <span>公開合集</span>
            </label>
          </div>
          <div class="modal-actions">
            <button type="button" @click="closeEditModal" class="cancel-btn">取消</button>
            <button type="submit" class="submit-btn">
              <span class="btn-icon">💾</span> 保存
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- AI 整合彈窗 -->
    <AIIntegrationModal
      v-if="showIntegrationModal"
      :note-count="notes.length"
      @close="showIntegrationModal = false"
      @integrate="handleIntegration"
      ref="integrationModalRef"
    />

    <!-- 整合結果彈窗 -->
    <IntegrationResultModal
      v-if="integrationResult"
      :result="integrationResult"
      @close="integrationResult = null"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import {
  collectionsService,
  type Collection,
  type IntegrationResponse
} from '../services/collections'
import type { Note } from '../services/notes'
import NoteCard from '../components/NoteCard.vue'
import CoverImageUpload from '../components/CoverImageUpload.vue'
import AIIntegrationModal from '../components/AIIntegrationModal.vue'
import IntegrationResultModal from '../components/IntegrationResultModal.vue'
import { useUserStore } from '../stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const collection = ref<Collection>({
  name: '',
  description: '',
  is_public: true
})
const notes = ref<Note[]>([])
const loading = ref(true)
const error = ref('')
const enableSorting = ref(false)
const showEditModal = ref(false)
const showIntegrationModal = ref(false)
const integrationResult = ref<IntegrationResponse | null>(null)
const integrationModalRef = ref<any>(null)
const editForm = ref<Collection>({
  name: '',
  description: '',
  is_public: true
})

let draggedIndex = -1

const collectionId = computed(() => parseInt(route.params.id as string))

const isOwner = computed(() => {
  return userStore.user && collection.value.user_id === userStore.user.id
})

const coverStyle = computed(() => {
  if (collection.value.cover_image) {
    return {
      backgroundImage: `url(${collection.value.cover_image})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center'
    }
  }
  return {}
})

onMounted(async () => {
  await loadCollection()
  await loadNotes()
})

async function loadCollection() {
  try {
    collection.value = await collectionsService.getCollection(collectionId.value)
  } catch (err: any) {
    error.value = err.response?.data?.detail || '載入合集失敗'
  } finally {
    loading.value = false
  }
}

async function loadNotes() {
  try {
    notes.value = await collectionsService.getCollectionNotes(collectionId.value)
  } catch (err) {
    console.error('載入筆記失敗', err)
  }
}

function viewNote(id: number) {
  router.push(`/notes/${id}`)
}

async function removeNote(noteId: number) {
  if (!confirm('確定要從合集中移除這篇筆記嗎？')) return

  try {
    await collectionsService.removeNoteFromCollection(collectionId.value, noteId)
    await loadNotes()
  } catch (err) {
    alert('移除筆記失敗')
  }
}

async function deleteCollection() {
  if (!confirm('確定要刪除此合集嗎？此操作無法撤銷。')) return

  try {
    await collectionsService.deleteCollection(collectionId.value)
    router.push('/my-collections')
  } catch (err) {
    alert('刪除合集失敗')
  }
}

function closeEditModal() {
  showEditModal.value = false
}

async function updateCollection() {
  try {
    await collectionsService.updateCollection(collectionId.value, editForm.value)
    closeEditModal()
    await loadCollection()
  } catch (err) {
    alert('更新合集失敗')
  }
}

// 拖拽排序
function handleDragStart(index: number) {
  draggedIndex = index
}

async function handleDrop(dropIndex: number) {
  if (draggedIndex === -1 || draggedIndex === dropIndex) return

  const newNotes = [...notes.value]
  const [draggedNote] = newNotes.splice(draggedIndex, 1)
  if (draggedNote) {
    newNotes.splice(dropIndex, 0, draggedNote)
  }

  notes.value = newNotes

  // 更新排序到後端
  try {
    const noteIds = newNotes.map(note => note.id!)
    await collectionsService.reorderCollectionNotes(collectionId.value, noteIds)
  } catch (err) {
    alert('更新排序失敗')
    await loadNotes() // 重新載入
  }

  draggedIndex = -1
}

// 當編輯彈窗打開時，填充表單
function openEditModal() {
  editForm.value = {
    name: collection.value.name,
    description: collection.value.description || '',
    cover_image: collection.value.cover_image || '',
    is_public: collection.value.is_public
  }
  showEditModal.value = true
}

// AI 整合處理
async function handleIntegration(apiKey: string, customPrompt?: string) {
  try {
    const result = await collectionsService.integrateCollectionNotes(
      collectionId.value,
      {
        api_key: apiKey,
        custom_prompt: customPrompt
      }
    )

    // 關閉整合彈窗，顯示結果
    showIntegrationModal.value = false
    integrationResult.value = result
  } catch (err: any) {
    console.error('整合失敗', err)
    if (integrationModalRef.value) {
      const errorMsg = err.response?.data?.detail || '整合失敗，請檢查 API Key 是否正確'
      integrationModalRef.value.setError(errorMsg)
    }
  }
}
</script>

<style scoped>
.collection-detail-page {
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
  background: radial-gradient(circle at 15% 15%, rgba(102, 126, 234, 0.1) 0%, transparent 50%),
              radial-gradient(circle at 85% 85%, rgba(118, 75, 162, 0.1) 0%, transparent 50%);
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

.collection-header {
  position: relative;
  max-width: 1200px;
  margin: 0 auto 3rem;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  overflow: hidden;
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

.collection-cover {
  width: 100%;
  height: 250px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.default-cover {
  font-size: 80px;
}

.collection-info {
  padding: 2.5rem;
}

.collection-title {
  margin: 0 0 1rem 0;
  font-size: clamp(1.8rem, 4vw, 2.5rem);
  font-weight: 700;
  color: rgba(255, 255, 255, 0.95);
}

.description {
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.meta {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  align-items: center;
  margin-bottom: 1.5rem;
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

.badge {
  padding: 0.5rem 1rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
  backdrop-filter: blur(10px);
}

.badge.public {
  background: rgba(72, 187, 120, 0.2);
  border: 1px solid rgba(72, 187, 120, 0.3);
  color: #48bb78;
}

.badge.private {
  background: rgba(255, 163, 38, 0.2);
  border: 1px solid rgba(255, 163, 38, 0.3);
  color: #ffa326;
}

.actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.3s;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.back-btn {
  background: rgba(102, 126, 234, 0.2);
  color: white;
}

.back-btn:hover {
  background: rgba(102, 126, 234, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.integrate-btn {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.8), rgba(118, 75, 162, 0.8));
  color: white;
}

.integrate-btn:hover {
  background: linear-gradient(135deg, #667eea, #764ba2);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.sort-btn {
  background: rgba(255, 163, 38, 0.2);
  color: #ffa326;
}

.sort-btn:hover {
  background: rgba(255, 163, 38, 0.3);
  transform: translateY(-2px);
}

.edit-btn {
  background: rgba(72, 187, 120, 0.2);
  color: #48bb78;
}

.edit-btn:hover {
  background: rgba(72, 187, 120, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(72, 187, 120, 0.3);
}

.delete-btn {
  background: rgba(252, 129, 129, 0.2);
  color: #fc8181;
}

.delete-btn:hover {
  background: rgba(252, 129, 129, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(252, 129, 129, 0.3);
}

.btn-icon {
  font-size: 1.1rem;
}

.notes-section {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
  z-index: 1;
}

.section-title {
  margin-bottom: 2rem;
  font-size: clamp(1.5rem, 4vw, 2rem);
  font-weight: 700;
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

.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 4rem 2rem;
  color: rgba(255, 255, 255, 0.8);
}

.empty-icon {
  font-size: 4rem;
  opacity: 0.5;
}

.empty p {
  font-size: 1.2rem;
  margin: 0;
}

.notes-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.note-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  transition: transform 0.3s;
}

.note-item.sortable {
  cursor: move;
}

.drag-handle {
  font-size: 24px;
  color: rgba(255, 255, 255, 0.3);
  cursor: grab;
  user-select: none;
  padding: 0.5rem;
}

.drag-handle:active {
  cursor: grabbing;
}

.note-item > :nth-child(2) {
  flex: 1;
}

.remove-btn {
  padding: 0.5rem 0.75rem;
  background: rgba(252, 129, 129, 0.9);
  backdrop-filter: blur(10px);
  color: white;
  border: 1px solid rgba(252, 129, 129, 0.3);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
  font-weight: 600;
}

.remove-btn:hover {
  background: #f56565;
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(252, 129, 129, 0.4);
}

/* 彈窗樣式 */
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
  z-index: 1000;
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
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 2.5rem;
  border-radius: 24px;
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
  animation: slideUp 0.4s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-title {
  margin: 0 0 1.5rem 0;
  color: rgba(255, 255, 255, 0.95);
  font-size: 1.8rem;
  font-weight: 700;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
}

.form-group input[type="text"],
.form-group textarea {
  width: 100%;
  padding: 0.9rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  font-size: 1rem;
  color: #fff;
  box-sizing: border-box;
  transition: all 0.3s;
}

.form-group input::placeholder,
.form-group textarea::placeholder {
  color: rgba(255, 255, 255, 0.3);
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.08);
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group textarea {
  resize: vertical;
  font-family: inherit;
  line-height: 1.6;
}

.checkbox-group {
  margin-top: 1rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  transition: all 0.3s;
}

.checkbox-label:hover {
  background: rgba(255, 255, 255, 0.05);
}

.checkbox-label input[type="checkbox"] {
  width: 20px;
  height: 20px;
  cursor: pointer;
}

.checkbox-label span {
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

.cancel-btn,
.submit-btn {
  padding: 0.9rem 1.5rem;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
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

.submit-btn {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

@media (max-width: 768px) {
  .collection-detail-page {
    padding: 1rem;
  }

  .collection-info {
    padding: 1.5rem;
  }

  .actions {
    flex-direction: column;
  }

  .action-btn {
    width: 100%;
    justify-content: center;
  }

  .note-item {
    flex-direction: column;
  }

  .floating-element {
    display: none;
  }

  .modal-content {
    padding: 1.5rem;
  }
}
</style>
