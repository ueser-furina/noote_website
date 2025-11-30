from pydantic_settings import BaseSettings

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
    BACKEND_CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]

    # Google Gemini API 設定
    GOOGLE_API_KEY: str = ""  # 從環境變數讀取或直接設定

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
