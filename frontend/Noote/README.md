# Roll Call AI - Frontend

Vue 3 + TypeScript 前端應用，提供筆記分享、搜尋和合集管理功能。

## 🚀 安裝與運行

### 1. 安裝依賴
```bash
cd frontend/Noote
npm install
```

### 2. 開發模式
```bash
npm run dev
```

前端將在 `http://localhost:5173` 啟動

### 3. 生產構建
```bash
npm run build
```

構建輸出在 `dist/` 目錄

### 4. 預覽生產構建
```bash
npm run preview
```

## 📁 項目結構

```
frontend/Noote/
├── src/
│   ├── views/                 # 頁面組件
│   │   ├── Home.vue              # 首頁
│   │   ├── Login.vue             # 登入頁
│   │   ├── Register.vue          # 註冊頁
│   │   ├── NoteList.vue          # 公開筆記列表（含搜尋）
│   │   ├── MyNotes.vue           # 我的筆記（含搜尋）
│   │   ├── NoteDetail.vue        # 筆記詳情
│   │   ├── CreateNote.vue        # 創建筆記
│   │   ├── PublicCollections.vue # 公開合集
│   │   ├── MyCollections.vue     # 我的合集
│   │   └── CollectionDetail.vue  # 合集詳情（含拖拽排序）
│   ├── components/            # 可重用組件
│   │   ├── SearchBar.vue         # 搜尋欄（防抖）
│   │   ├── NoteCard.vue          # 筆記卡片（關鍵字高亮）
│   │   ├── CollectionCard.vue    # 合集卡片
│   │   ├── AddToCollectionModal.vue # 加入合集彈窗
│   │   └── CoverImageUpload.vue  # 封面上傳組件
│   ├── services/              # API 服務
│   │   ├── api.ts                # Axios 實例
│   │   ├── auth.ts               # 認證 API
│   │   ├── notes.ts              # 筆記 API
│   │   └── collections.ts        # 合集 API
│   ├── stores/                # Pinia 狀態管理
│   │   └── user.ts               # 用戶狀態
│   ├── router/                # Vue Router
│   │   └── index.ts              # 路由配置
│   ├── utils/                 # 工具函數
│   │   └── markdown.ts           # Markdown 渲染
│   ├── App.vue                # 根組件
│   ├── main.ts                # 入口文件
│   └── style.css              # 全局樣式
├── public/                    # 靜態資源
├── index.html                 # HTML 模板
├── vite.config.ts             # Vite 配置
├── tsconfig.json              # TypeScript 配置
└── package.json               # 依賴配置
```

## 🎨 主要功能

### 🔐 認證系統
- **註冊/登入**: JWT Token 認證
- **自動登入**: 使用 localStorage 保存 Token
- **路由守衛**: 保護需要登入的頁面
- **自動登出**: Token 過期自動跳轉登入頁

### 📝 筆記管理
- **瀏覽公開筆記**: 卡片式展示
- **我的筆記**: 管理個人筆記
- **創建筆記**: 支援 Markdown 和純文本
- **編輯/刪除**: 擁有者專屬操作
- **Markdown 渲染**: 支援程式碼高亮

### 🔍 全文搜尋
- **實時搜尋**: 輸入後 300ms 執行（防抖）
- **關鍵字高亮**: 黃色背景標記搜尋關鍵字
- **智能摘要**: 優先顯示包含關鍵字的片段
- **多範圍搜尋**: 公開筆記、個人筆記、全部筆記
- **空狀態提示**: 沒有結果時的友善提示

### 📚 筆記合集
- **創建合集**: 自訂名稱、描述、封面
- **管理合集**: 編輯、刪除、公開/私密設定
- **添加筆記**: 從筆記詳情頁加入合集（支援多選）
- **拖拽排序**: 直觀調整筆記順序
- **封面上傳**: 支援圖片上傳（Base64）
- **權限控制**: 私密合集只對擁有者可見

## 🛠️ 技術棧

### 核心框架
- **Vue 3**: Composition API
- **TypeScript**: 類型安全
- **Vite**: 快速開發構建

### 路由與狀態
- **Vue Router**: SPA 路由管理
- **Pinia**: 狀態管理

### UI 與樣式
- **原生 CSS**: 無 UI 框架依賴
- **響應式設計**: 支援手機/平板/桌面

### HTTP 與數據
- **Axios**: HTTP 客戶端
- **Request/Response 攔截器**: 自動注入 Token

### Markdown 渲染
- **Marked**: Markdown 解析
- **Highlight.js**: 程式碼高亮

## 📦 主要依賴

```json
{
  "dependencies": {
    "vue": "^3.3.4",
    "vue-router": "^4.2.5",
    "pinia": "^2.1.7",
    "axios": "^1.6.2",
    "marked": "^11.0.0",
    "highlight.js": "^11.9.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.4.0",
    "typescript": "^5.2.2",
    "vite": "^5.0.0",
    "vue-tsc": "^1.8.22"
  }
}
```

## 🔌 API 集成

### API 基礎配置
```typescript
// src/services/api.ts
const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

// 自動注入 Token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

### 認證服務
```typescript
// src/services/auth.ts
export const authService = {
  async register(username: string, email: string, password: string)
  async login(username: string, password: string)
  async getCurrentUser()
  isAuthenticated()
  logout()
}
```

### 筆記服務
```typescript
// src/services/notes.ts
export const notesService = {
  async createNote(note: Note)
  async getPublicNotes(skip, limit)
  async getMyNotes()
  async getNote(id)
  async updateNote(id, note)
  async deleteNote(id)
  async searchNotes(query, scope)
}
```

### 合集服務
```typescript
// src/services/collections.ts
export const collectionsService = {
  async createCollection(collection)
  async getPublicCollections(skip, limit)
  async getMyCollections()
  async getCollection(id)
  async updateCollection(id, collection)
  async deleteCollection(id)
  async getCollectionNotes(id)
  async addNoteToCollection(collectionId, noteId)
  async removeNoteFromCollection(collectionId, noteId)
  async reorderCollectionNotes(collectionId, noteIds)
}
```

## 🎯 路由配置

```typescript
const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/register', component: Register },
  { path: '/notes', component: NoteList },
  { path: '/notes/:id', component: NoteDetail },
  { path: '/my-notes', component: MyNotes, meta: { requiresAuth: true } },
  { path: '/create-note', component: CreateNote, meta: { requiresAuth: true } },
  { path: '/collections/public', component: PublicCollections },
  { path: '/my-collections', component: MyCollections, meta: { requiresAuth: true } },
  { path: '/collections/:id', component: CollectionDetail },
]
```

## 🎨 組件說明

### SearchBar.vue
- **功能**: 搜尋輸入框，帶防抖機制
- **Props**: `placeholder`, `debounceMs` (預設 300ms)
- **Events**: `@search` - 發出搜尋關鍵字

### NoteCard.vue
- **功能**: 筆記卡片，顯示標題、摘要、作者
- **Props**: `note`, `searchQuery` (高亮用)
- **Features**:
  - 關鍵字高亮（黃色背景）
  - 智能摘要（優先顯示包含關鍵字的部分）
  - 點擊跳轉詳情頁

### CollectionCard.vue
- **功能**: 合集卡片，顯示封面、名稱、筆記數量
- **Props**: `collection`
- **Features**:
  - 封面圖片顯示（支援自訂或預設）
  - 公開/私密標籤
  - Hover 動畫效果

### AddToCollectionModal.vue
- **功能**: 添加筆記到合集的彈窗
- **Props**: `noteId`
- **Events**: `@close`, `@added`
- **Features**:
  - 多選合集
  - 顯示已添加狀態
  - 自動檢測筆記是否已在合集中

### CoverImageUpload.vue
- **功能**: 封面圖片上傳組件
- **Props**: `modelValue` (v-model)
- **Features**:
  - 圖片預覽
  - 拖曳上傳支援（UI 預留）
  - 文件驗證（類型、大小 5MB）
  - Base64 編碼

## 🔧 配置

### 環境變數
創建 `.env` 文件：
```env
VITE_API_URL=http://localhost:8000/api/v1
```

使用：
```typescript
const API_URL = import.meta.env.VITE_API_URL
```

### TypeScript 配置
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "module": "ESNext",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "preserve",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

## 🎭 開發技巧

### 熱模組替換 (HMR)
Vite 自動支援，修改代碼立即生效

### Vue Devtools
安裝 Vue Devtools 瀏覽器擴展進行調試

### API Mock
開發時可使用 Mock Service Worker (MSW)

## 🚀 部署

### 靜態網站託管
```bash
npm run build
# 將 dist/ 目錄上傳到:
# - Vercel
# - Netlify
# - GitHub Pages
# - Cloudflare Pages
```

### Docker
```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Nginx 配置
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:8000;
    }
}
```

## 🐛 開發與調試

### 查看構建產物
```bash
npm run build -- --debug
```

### 分析構建大小
```bash
npm run build -- --report
```

## 📄 授權

本專案為教育用途開發。
