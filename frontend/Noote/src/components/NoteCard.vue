<template>
  <div class="note-card" @click="$emit('click')">
    <h3 class="note-title" v-html="highlightedTitle"></h3>
    <div class="note-meta">
      <span class="note-author">{{ note.owner_username }}</span>
      <span class="note-date">{{ formatDate(note.created_at) }}</span>
    </div>
    <div class="note-excerpt" v-html="highlightedExcerpt"></div>
    <div class="note-type">
      <span class="type-badge" :class="note.file_type">{{ note.file_type }}</span>
      <span v-if="note.is_public" class="visibility-badge public">公開</span>
      <span v-else class="visibility-badge private">私密</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Note } from '../services/notes'

interface Props {
  note: Note
  searchQuery?: string
}

const props = defineProps<Props>()
defineEmits<{
  click: []
}>()

// 格式化日期
const formatDate = (dateString?: string) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-TW', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 生成摘要（前200字）
const getExcerpt = (content: string, maxLength: number = 200) => {
  if (content.length <= maxLength) return content
  return content.substring(0, maxLength) + '...'
}

// 高亮關鍵字
const highlightText = (text: string, query: string) => {
  if (!query || !text) return text

  // 轉義正則特殊字符
  const escapeRegex = (str: string) => {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  }

  const regex = new RegExp(`(${escapeRegex(query)})`, 'gi')
  return text.replace(regex, '<mark class="highlight">$1</mark>')
}

// 高亮標題
const highlightedTitle = computed(() => {
  return highlightText(props.note.title, props.searchQuery || '')
})

// 高亮摘要（優先顯示包含關鍵字的部分）
const highlightedExcerpt = computed(() => {
  const content = props.note.content
  const query = props.searchQuery || ''

  if (!query) {
    return getExcerpt(content)
  }

  // 查找關鍵字位置
  const lowerContent = content.toLowerCase()
  const lowerQuery = query.toLowerCase()
  const index = lowerContent.indexOf(lowerQuery)

  if (index === -1) {
    // 關鍵字不在內容中，返回前200字
    return highlightText(getExcerpt(content), query)
  }

  // 提取包含關鍵字的片段（前後各100字）
  const start = Math.max(0, index - 100)
  const end = Math.min(content.length, index + query.length + 100)
  let excerpt = content.substring(start, end)

  if (start > 0) excerpt = '...' + excerpt
  if (end < content.length) excerpt = excerpt + '...'

  return highlightText(excerpt, query)
})
</script>

<style scoped>
.note-card {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(30px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.note-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
}

.note-card:hover {
  background: rgba(255, 255, 255, 0.12);
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(102, 126, 234, 0.3);
  border-color: rgba(102, 126, 234, 0.4);
}

.note-title {
  margin: 0 0 0.75rem 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.95);
}

.note-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.75rem;
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.6);
}

.note-author {
  font-weight: 500;
  color: rgba(255, 255, 255, 0.7);
}

.note-excerpt {
  color: rgba(255, 255, 255, 0.75);
  line-height: 1.6;
  margin-bottom: 1rem;
  font-size: 0.875rem;
}

.note-type {
  display: flex;
  gap: 0.625rem;
  align-items: center;
}

.type-badge {
  padding: 0.375rem 0.75rem;
  border-radius: 8px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  backdrop-filter: blur(10px);
}

.type-badge.md {
  background: rgba(66, 153, 225, 0.2);
  color: #90cdf4;
  border: 1px solid rgba(66, 153, 225, 0.3);
}

.type-badge.txt {
  background: rgba(159, 122, 234, 0.2);
  color: #d6bcfa;
  border: 1px solid rgba(159, 122, 234, 0.3);
}

.visibility-badge {
  padding: 0.375rem 0.75rem;
  border-radius: 8px;
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

:deep(.highlight) {
  background: linear-gradient(135deg, rgba(251, 191, 36, 0.3), rgba(245, 158, 11, 0.3));
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 600;
  color: #fbbf24;
  border: 1px solid rgba(251, 191, 36, 0.4);
}
</style>
