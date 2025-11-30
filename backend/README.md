# Roll Call AI - Backend API

FastAPI 後端服務，提供 JWT 認證、筆記管理、搜尋和合集功能。

## 🚀 安裝與運行

### 1. 安裝依賴
```bash
cd backend
pip install -r requirements.txt
```

### 2. 運行開發服務器
```bash
python main.py
```

服務器將在 `http://localhost:8000` 啟動

### 3. API 文檔
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📁 項目結構

```
backend/
├── app/
│   ├── models/              # 資料庫模型
│   │   ├── user.py            # 用戶模型
│   │   ├── note.py            # 筆記模型
│   │   └── collection.py      # 合集模型
│   ├── routers/             # API 路由
│   │   ├── auth.py            # 認證端點
│   │   ├── notes.py           # 筆記端點（含搜尋）
│   │   └── collections.py     # 合集端點
│   ├── schemas/             # Pydantic Schema
│   │   ├── user.py            # 用戶 Schema
│   │   ├── note.py            # 筆記 Schema
│   │   └── collection.py      # 合集 Schema
│   ├── core/                # 核心功能
│   │   ├── config.py          # 配置管理
│   │   ├── security.py        # JWT、密碼加密
│   │   └── deps.py            # 依賴注入
│   ├── database.py          # 資料庫連接
│   └── main.py              # FastAPI 應用
├── main.py                  # 應用入口
└── requirements.txt         # Python 依賴
```

## 📝 API 端點

### 認證 (`/api/v1/auth`)
- `POST /register` - 註冊新用戶
  - Body: `{ "username": "...", "email": "...", "password": "..." }`
  - Response: 用戶資訊 + Token
- `POST /login` - 用戶登入
  - Body: `{ "username": "...", "password": "..." }`
  - Response: `{ "access_token": "...", "token_type": "bearer" }`
- `GET /me` - 獲取當前用戶信息
  - Headers: `Authorization: Bearer <token>`
  - Response: 用戶資訊

### 筆記 (`/api/v1/notes`)
- `POST /` - 創建新筆記 🔒
  - Body: `{ "title": "...", "content": "...", "file_type": "md", "is_public": true }`
- `GET /` - 獲取公開筆記列表
  - Query: `?skip=0&limit=20`
- `GET /my` - 獲取我的筆記 🔒
- `GET /search` - 搜尋筆記
  - Query: `?q=關鍵字&scope=public|my|all`
  - **scope 說明**:
    - `public`: 搜尋公開筆記（無需登入）
    - `my`: 搜尋我的筆記（需登入）
    - `all`: 搜尋我的 + 公開筆記（需登入）
- `GET /{id}` - 獲取單個筆記
- `PUT /{id}` - 更新筆記 🔒
- `DELETE /{id}` - 刪除筆記 🔒

### 筆記合集 (`/api/v1/collections`)
- `POST /` - 創建合集 🔒
  - Body: `{ "name": "...", "description": "...", "cover_image": "...", "is_public": true }`
- `GET /` - 獲取公開合集列表
  - Query: `?skip=0&limit=20`
- `GET /my` - 獲取我的合集 🔒
- `GET /{id}` - 獲取合集詳情
- `PUT /{id}` - 更新合集 🔒
- `DELETE /{id}` - 刪除合集 🔒
- `GET /{id}/notes` - 獲取合集內筆記
- `POST /{id}/notes` - 添加筆記到合集 🔒
  - Body: `{ "note_id": 123 }`
- `DELETE /{id}/notes/{note_id}` - 從合集移除筆記 🔒
- `PUT /{id}/notes/reorder` - 重排序合集內筆記 🔒
  - Body: `{ "note_ids": [1, 3, 2, 4] }`

🔒 = 需要 JWT 認證

## 🗃️ 資料庫模型

### User (用戶)
```python
id: int (PK)
username: str (unique, indexed)
email: str (unique, indexed)
hashed_password: str
created_at: datetime
```

### Note (筆記)
```python
id: int (PK)
title: str (indexed)
content: text
file_type: str (md/txt)
is_public: bool
user_id: int (FK -> User)
created_at: datetime
updated_at: datetime
```

### Collection (合集)
```python
id: int (PK)
name: str (indexed)
description: text
cover_image: str (nullable, Base64)
is_public: bool
user_id: int (FK -> User)
created_at: datetime
updated_at: datetime
```

### CollectionNote (合集-筆記關聯)
```python
id: int (PK)
collection_id: int (FK -> Collection)
note_id: int (FK -> Note)
position: int (排序)
added_at: datetime
```

## ⚙️ 配置

### 環境變數
在 `app/core/config.py` 中修改配置:

```python
class Settings(BaseSettings):
    PROJECT_NAME: str = "Roll Call AI - Note Sharing Platform"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"

    # JWT 配置
    SECRET_KEY: str = "your-secret-key-here"  # 生產環境必須修改
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 天

    # 資料庫配置
    DATABASE_URL: str = "sqlite:///./roll_call_ai.db"  # 或 PostgreSQL

    # CORS 配置
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # 其他前端
    ]
```

### 資料庫遷移

**使用 SQLite (開發)**:
- 自動創建: 啟動時自動建立資料庫

**使用 PostgreSQL (生產)**:
```bash
# 修改 DATABASE_URL
DATABASE_URL = "postgresql://user:password@localhost/roll_call_ai"

# 安裝 PostgreSQL driver
pip install psycopg2-binary
```

## 🔐 安全性

### JWT 認證
- 使用 HS256 算法
- Token 有效期 7 天
- 密碼使用 bcrypt 加密

### 權限控制
- **筆記**:
  - 公開筆記任何人可讀
  - 只有擁有者可以編輯/刪除
- **合集**:
  - 公開合集任何人可讀
  - 私密合集只有擁有者可見
  - 只有擁有者可以編輯/刪除/添加筆記

## 🔍 搜尋功能

### 搜尋實現
使用 SQLAlchemy 的 `ilike` (不區分大小寫):
```python
notes = db.query(Note).filter(
    or_(
        Note.title.ilike(f"%{query}%"),
        Note.content.ilike(f"%{query}%")
    )
)
```

### 搜尋優化建議
- SQLite: 適合小規模使用
- PostgreSQL: 可使用全文搜尋 (Full-Text Search)
- Elasticsearch: 大規模應用推薦

## 📦 依賴

主要依賴套件:
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
```

## 🚀 部署

### Docker (推薦)
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 傳統部署
```bash
# 使用 gunicorn + uvicorn worker
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🧪 測試

```bash
# 安裝測試依賴
pip install pytest pytest-asyncio httpx

# 運行測試
pytest
```

## 📊 API 使用範例

### 註冊用戶
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_user",
    "email": "test@example.com",
    "password": "password123"
  }'
```

### 登入
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_user",
    "password": "password123"
  }'
```

### 創建筆記
```bash
curl -X POST http://localhost:8000/api/v1/notes/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "測試筆記",
    "content": "# 標題\n這是內容",
    "file_type": "md",
    "is_public": true
  }'
```

### 搜尋筆記
```bash
curl "http://localhost:8000/api/v1/notes/search?q=測試&scope=public"
```

### 創建合集
```bash
curl -X POST http://localhost:8000/api/v1/collections/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "我的合集",
    "description": "這是一個測試合集",
    "is_public": true
  }'
```

## 🛠️ 開發

### 熱重載
```bash
uvicorn app.main:app --reload
```

### 查看日誌
```bash
# 使用 --log-level 控制日誌級別
uvicorn app.main:app --log-level debug
```

## 📄 授權

本專案為教育用途開發。
