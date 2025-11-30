<template>
  <div class="collection-card" @click="$emit('click')">
    <div class="collection-cover" :style="coverStyle">
      <div v-if="!collection.cover_image" class="default-cover">
        📚
      </div>
    </div>
    <div class="collection-info">
      <h3 class="collection-name">{{ collection.name }}</h3>
      <p class="collection-description">{{ truncatedDescription }}</p>
      <div class="collection-meta">
        <span class="collection-author">👤 {{ collection.owner_username }}</span>
        <span class="collection-count">📝 {{ collection.note_count || 0 }} 篇</span>
      </div>
      <div class="collection-visibility">
        <span v-if="collection.is_public" class="visibility-badge public">公開</span>
        <span v-else class="visibility-badge private">私密</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Collection } from '../services/collections'

interface Props {
  collection: Collection
}

const props = defineProps<Props>()
defineEmits<{
  click: []
}>()

const coverStyle = computed(() => {
  if (props.collection.cover_image) {
    return {
      backgroundImage: `url(${props.collection.cover_image})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center'
    }
  }
  return {}
})

const truncatedDescription = computed(() => {
  const maxLength = 80
  if (props.collection.description.length <= maxLength) {
    return props.collection.description
  }
  return props.collection.description.substring(0, maxLength) + '...'
})
</script>

<style scoped>
.collection-card {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(30px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 20px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.collection-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  z-index: 1;
}

.collection-card:hover {
  background: rgba(255, 255, 255, 0.12);
  transform: translateY(-6px);
  box-shadow: 0 16px 40px rgba(102, 126, 234, 0.4);
  border-color: rgba(102, 126, 234, 0.5);
}

.collection-cover {
  width: 100%;
  height: 200px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.6) 0%, rgba(118, 75, 162, 0.6) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.collection-cover::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100%;
  background: linear-gradient(180deg, transparent 0%, rgba(0, 0, 0, 0.2) 100%);
}

.default-cover {
  font-size: 4rem;
  z-index: 1;
  filter: drop-shadow(0 4px 12px rgba(0, 0, 0, 0.3));
}

.collection-info {
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.03);
}

.collection-name {
  margin: 0 0 0.75rem 0;
  font-size: 1.25rem;
  color: rgba(255, 255, 255, 0.95);
  font-weight: 700;
}

.collection-description {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.875rem;
  line-height: 1.6;
  margin-bottom: 1rem;
  min-height: 44px;
}

.collection-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.75rem;
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.6);
}

.collection-visibility {
  margin-top: 0.75rem;
}

.visibility-badge {
  padding: 0.375rem 0.875rem;
  border-radius: 10px;
  font-size: 0.75rem;
  font-weight: 600;
  backdrop-filter: blur(10px);
}

.visibility-badge.public {
  background: rgba(72, 187, 120, 0.2);
  color: #9ae6b4;
  border: 1px solid rgba(72, 187, 120, 0.3);
}

.visibility-badge.private {
  background: rgba(237, 137, 54, 0.2);
  color: #fbd38d;
  border: 1px solid rgba(237, 137, 54, 0.3);
}
</style>
