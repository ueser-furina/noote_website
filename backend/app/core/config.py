from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Union
import json

class Settings(BaseSettings):
    PROJECT_NAME: str = "Roll Call AI - Note Sharing"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # JWT設定
    SECRET_KEY: str = "your-secret-key-change-in-production"  # 生產環境需要更改
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天

    # 資料庫設定
    DATABASE_URL: str = "sqlite:///./notes.db"

    # CORS設定
    BACKEND_CORS_ORIGINS: Union[List[str], str] = '["http://localhost:5173", "http://localhost:3000"]'

    # Google Gemini API 設定
    GOOGLE_API_KEY: str = ""  # 從環境變數讀取或直接設定

    @field_validator('BACKEND_CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                # 如果不是 JSON，嘗試用逗號分割
                return [origin.strip() for origin in v.split(',') if origin.strip()]
        return v

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
