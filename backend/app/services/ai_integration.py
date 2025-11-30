"""
AI 整合服務 - 用於將多個筆記合併整合
"""
import os
import json
from typing import List, Dict
import google.generativeai as genai

class AIIntegrationService:
    """AI 整合服務類別"""

    def __init__(self, api_key: str = None):
        """初始化 AI 服務

        Args:
            api_key: Google Gemini API 金鑰，若未提供則從環境變數讀取
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY", "")
        if self.api_key:
            genai.configure(api_key=self.api_key)
        else:
            print("警告：未設定 GOOGLE_API_KEY，AI 整合功能將無法使用")

    def integrate_notes(self, notes_data: List[Dict[str, str]], integration_prompt: str = None) -> str:
        """整合多個筆記內容

        Args:
            notes_data: 筆記資料列表，每個項目包含 title 和 content
            integration_prompt: 自訂整合提示詞，若未提供則使用預設

        Returns:
            整合後的筆記內容（Markdown 格式）

        Raises:
            RuntimeError: 當 API 金鑰未設定或 API 呼叫失敗
        """
        if not self.api_key:
            raise RuntimeError("未設定 GOOGLE_API_KEY，無法使用 AI 整合功能")

        if not notes_data:
            raise ValueError("筆記資料不能為空")

        # 建構提示詞
        notes_content = self._format_notes_for_prompt(notes_data)

        if integration_prompt is None:
            integration_prompt = self._get_default_integration_prompt()

        full_prompt = f"{integration_prompt}\n\n{notes_content}"

        try:
            # 使用 Gemini 2.0 Flash 進行整合
            model = genai.GenerativeModel("gemini-2.0-flash-lite")
            response = model.generate_content(full_prompt)

            if not response or not response.text:
                raise RuntimeError("AI 回應為空")

            integrated_content = response.text.strip()
            return integrated_content

        except Exception as e:
            error_msg = f"呼叫 Gemini API 時發生錯誤: {str(e)}"
            print(error_msg)
            raise RuntimeError(error_msg)

    def _format_notes_for_prompt(self, notes_data: List[Dict[str, str]]) -> str:
        """將筆記資料格式化為提示詞格式"""
        formatted_notes = []

        for i, note in enumerate(notes_data, 1):
            title = note.get("title", f"筆記 {i}")
            content = note.get("content", "")

            formatted_note = f"""
## 筆記 {i}: {title}

{content}

---
"""
            formatted_notes.append(formatted_note)

        return "\n".join(formatted_notes)

    def _get_default_integration_prompt(self) -> str:
        """取得預設的整合提示詞"""
        return """你是一位專業的學習助理，擅長整理和統整課堂筆記。

現在有多份課堂筆記需要你整合。請仔細閱讀所有筆記，然後：

1. **統整重複內容**：將相同主題的內容合併，避免重複
2. **建立清晰結構**：使用階層式標題組織內容，建立邏輯清晰的大綱
3. **保留重要細節**：確保不遺漏任何重要的概念、定義、公式或範例
4. **補充關聯性**：在不同主題之間建立連結，幫助理解整體脈絡
5. **使用 Markdown 格式**：適當使用標題、列表、粗體、斜體、程式碼區塊等格式
6. **新增摘要**：在開頭加上簡短的整體摘要

請生成一份完整、結構清晰、易於複習的整合筆記。

以下是需要整合的筆記："""


# 延遲初始化，從設定讀取 API key
def get_ai_service():
    """取得 AI 服務實例（從設定檔讀取 API key）"""
    from ..core.config import settings
    return AIIntegrationService(api_key=settings.GOOGLE_API_KEY)

# 建立全域實例（從環境變數或設定檔讀取）
ai_service = get_ai_service()