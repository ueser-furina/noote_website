from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class CollectionBase(BaseModel):
    name: str
    description: str = ""
    is_public: bool = True

class CollectionCreate(CollectionBase):
    pass

class CollectionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    cover_image: Optional[str] = None
    is_public: Optional[bool] = None

class CollectionResponse(CollectionBase):
    id: int
    user_id: int
    cover_image: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    owner_username: Optional[str] = None
    note_count: Optional[int] = None  # 筆記數量

    class Config:
        from_attributes = True

class CollectionNoteAdd(BaseModel):
    note_id: int

class CollectionNoteReorder(BaseModel):
    note_ids: List[int]  # 按照新順序排列的筆記 ID 列表

class CollectionNoteResponse(BaseModel):
    id: int
    collection_id: int
    note_id: int
    position: int
    added_at: datetime

    class Config:
        from_attributes = True

class CollectionIntegrationRequest(BaseModel):
    custom_prompt: Optional[str] = None  # 自訂整合提示詞（選填）
    api_key: str  # Gemini API 金鑰（必填）

class CollectionIntegrationResponse(BaseModel):
    integrated_content: str  # 整合後的內容
    note_count: int  # 參與整合的筆記數量
    created_at: datetime  # 整合時間
