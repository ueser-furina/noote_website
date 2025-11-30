<template>
  <div class="my-collections-page">
    <!-- Background gradient overlay -->
    <div class="gradient-bg"></div>

    <!-- Floating elements -->
    <div class="floating-element" style="top: 8%; right: 12%">📚</div>
    <div class="floating-element" style="bottom: 12%; left: 10%">⭐</div>

    <div class="header">
      <h1 class="gradient-text">我的合集</h1>
      <div class="actions">
        <button @click="showCreateModal = true" class="create-btn">
          <span class="btn-icon">+</span> 新增合集
        </button>
        <router-link to="/" class="back-btn">
          <span class="btn-icon">←</span> 返回首頁
        </router-link>
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
    <div v-else-if="collections.length === 0" class="empty">
      <div class="empty-icon">📦</div>
      <p>還沒有任何合集</p>
      <a href="#" @click.prevent="showCreateModal = true" class="empty-action">立即新增</a>
    </div>
    <div v-else class="collections-grid">
      <CollectionCard
        v-for="collection in collections"
        :key="collection.id"
        :collection="collection"
        @click="viewCollection(collection.id!)"
      />
    </div>

    <!-- 創建合集彈窗 -->
    <div v-if="showCreateModal" class="modal-overlay" @click="closeCreateModal">
      <div class="modal-content" @click.stop>
        <h2 class="modal-title">創建新合集</h2>
        <form @submit.prevent="createCollection">
          <CoverImageUpload v-model="newCollection.cover_image" />

          <div class="form-group">
            <label>合集名稱 *</label>
            <input v-model="newCollection.name" type="text" placeholder="輸入合集名稱" required />
          </div>
          <div class="form-group">
            <label>描述</label>
            <textarea v-model="newCollection.description" rows="4" placeholder="輸入合集描述（可選）"></textarea>
          </div>
          <div class="form-group checkbox-group">
            <label class="checkbox-label">
              <input v-model="newCollection.is_public" type="checkbox" />
              <span>公開合集</span>
            </label>
          </div>
          <div class="modal-actions">
            <button type="button" @click="closeCreateModal" class="cancel-btn">取消</button>
            <button type="submit" class="submit-btn">
              <span class="btn-icon">✨</span> 創建
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { collectionsService, type Collection } from '../services/collections'
import CollectionCard from '../components/CollectionCard.vue'
import CoverImageUpload from '../components/CoverImageUpload.vue'

const router = useRouter()
const collections = ref<Collection[]>([])
const loading = ref(true)
const error = ref('')
const showCreateModal = ref(false)
const newCollection = ref<Collection>({
  name: '',
  description: '',
  cover_image: '',
  is_public: true
})

onMounted(async () => {
  await loadCollections()
})

async function loadCollections() {
  try {
    loading.value = true
    collections.value = await collectionsService.getMyCollections()
  } catch (err) {
    error.value = '載入合集失敗'
  } finally {
    loading.value = false
  }
}

function viewCollection(id: number) {
  router.push(`/collections/${id}`)
}

function closeCreateModal() {
  showCreateModal.value = false
  newCollection.value = {
    name: '',
    description: '',
    cover_image: '',
    is_public: true
  }
}

async function createCollection() {
  try {
    await collectionsService.createCollection(newCollection.value)
    closeCreateModal()
    await loadCollections()
  } catch (err) {
    alert('創建合集失敗')
  }
}
</script>

<style scoped>
.my-collections-page {
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

.actions {
  display: flex;
  gap: 0.75rem;
}

.create-btn,
.back-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  color: white;
  text-decoration: none;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  font-weight: 600;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.create-btn {
  background: linear-gradient(135deg, rgba(72, 187, 120, 0.8), rgba(56, 161, 105, 0.8));
}

.create-btn:hover {
  background: linear-gradient(135deg, #48bb78, #38a169);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(72, 187, 120, 0.4);
}

.back-btn {
  background: rgba(102, 126, 234, 0.2);
}

.back-btn:hover {
  background: rgba(102, 126, 234, 0.3);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.btn-icon {
  font-size: 1.2rem;
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

.empty-action {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  text-decoration: none;
  border-radius: 12px;
  font-weight: 600;
  transition: all 0.3s;
}

.empty-action:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.collections-grid {
  position: relative;
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  z-index: 1;
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
  .my-collections-page {
    padding: 1rem;
  }

  .header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }

  .actions {
    width: 100%;
    justify-content: center;
  }

  .collections-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .floating-element {
    display: none;
  }

  .modal-content {
    padding: 1.5rem;
  }
}
</style>
