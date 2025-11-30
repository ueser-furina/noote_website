<template>
  <div class="modal-overlay" @click="$emit('close')">
    <div class="modal-content" @click.stop>
      <h2>添加到合集</h2>

      <div v-if="loading" class="loading">載入中...</div>
      <div v-else-if="collections.length === 0" class="empty">
        你還沒有合集，<router-link to="/my-collections">立即創建</router-link>
      </div>
      <div v-else class="collections-list">
        <label
          v-for="collection in collections"
          :key="collection.id"
          class="collection-item"
        >
          <input
            type="checkbox"
            :value="collection.id"
            v-model="selectedCollections"
            :disabled="collection.has_note"
          />
          <div class="collection-info">
            <span class="collection-name">{{ collection.name }}</span>
            <span v-if="collection.has_note" class="already-added">已添加</span>
          </div>
        </label>
      </div>

      <div class="modal-actions">
        <button @click="$emit('close')" class="cancel-btn">取消</button>
        <button
          @click="addToCollections"
          class="submit-btn"
          :disabled="selectedCollections.length === 0"
        >
          添加
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { collectionsService, type Collection } from '../services/collections'

interface Props {
  noteId: number
}

const props = defineProps<Props>()
const emit = defineEmits<{
  close: []
  added: []
}>()

interface CollectionWithStatus extends Collection {
  has_note?: boolean
}

const collections = ref<CollectionWithStatus[]>([])
const selectedCollections = ref<number[]>([])
const loading = ref(true)

onMounted(async () => {
  await loadCollections()
})

async function loadCollections() {
  try {
    loading.value = true
    const myCollections = await collectionsService.getMyCollections()

    // 檢查每個合集是否已包含該筆記
    for (const collection of myCollections) {
      const notes = await collectionsService.getCollectionNotes(collection.id!)
      collection.has_note = notes.some((note: any) => note.id === props.noteId)
    }

    collections.value = myCollections
  } catch (err) {
    console.error('載入合集失敗', err)
  } finally {
    loading.value = false
  }
}

async function addToCollections() {
  try {
    for (const collectionId of selectedCollections.value) {
      await collectionsService.addNoteToCollection(collectionId, props.noteId)
    }
    emit('added')
    emit('close')
  } catch (err: any) {
    alert(err.response?.data?.detail || '添加失敗')
  }
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
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(30px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  padding: 2.5rem;
  border-radius: 24px;
  width: 90%;
  max-width: 540px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
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
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-content h2 {
  margin: 0 0 1.5rem 0;
  color: rgba(255, 255, 255, 0.95);
  font-size: 1.75rem;
  font-weight: 700;
}

.loading,
.empty {
  text-align: center;
  padding: 2rem;
  color: rgba(255, 255, 255, 0.7);
}

.empty :deep(a) {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.empty :deep(a:hover) {
  text-decoration: underline;
}

.collections-list {
  max-height: 400px;
  overflow-y: auto;
  margin-bottom: 1.5rem;
}

.collection-item {
  display: flex;
  align-items: center;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  margin-bottom: 0.75rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.collection-item:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(102, 126, 234, 0.3);
}

.collection-item input[type="checkbox"] {
  margin-right: 1rem;
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.collection-item input[type="checkbox"]:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.collection-info {
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.collection-name {
  font-weight: 600;
  color: rgba(255, 255, 255, 0.9);
}

.already-added {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.5);
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

.cancel-btn:hover {
  background: rgba(255, 255, 255, 0.12);
  transform: translateY(-2px);
}

.submit-btn {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.submit-btn:disabled {
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.4);
  cursor: not-allowed;
  transform: none;
}
</style>
