"""
測試 AI 整合功能的簡單腳本
"""
import os
from app.services.ai_integration import AIIntegrationService

def test_ai_integration():
    """測試 AI 整合服務"""

    # 設定 API key（從環境變數讀取）
    api_key = os.getenv("GOOGLE_API_KEY", "")

    if not api_key:
        print("錯誤：請設定環境變數 GOOGLE_API_KEY")
        print("範例：export GOOGLE_API_KEY='your_api_key_here'")
        return

    # 建立服務實例
    service = AIIntegrationService(api_key=api_key)

    # 測試資料
    test_notes = [
        {
            "title": "Python 基礎語法",
            "content": """
# Python 基礎語法

## 變數宣告
在 Python 中，變數不需要宣告型別：
```python
x = 5
name = "Alice"
```

## 資料型別
- int: 整數
- float: 浮點數
- str: 字串
- bool: 布林值
"""
        },
        {
            "title": "Python 函式",
            "content": """
# Python 函式

## 定義函式
使用 def 關鍵字定義函式：
```python
def greet(name):
    return f"Hello, {name}!"
```

## 參數預設值
```python
def greet(name="World"):
    return f"Hello, {name}!"
```
"""
        },
        {
            "title": "Python 類別",
            "content": """
# Python 類別

## 定義類別
```python
class Person:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hi, I'm {self.name}"
```
"""
        }
    ]

    print("開始測試 AI 整合功能...")
    print(f"筆記數量：{len(test_notes)}")
    print("-" * 50)

    try:
        # 呼叫整合服務
        result = service.integrate_notes(test_notes)

        print("整合成功！")
        print("=" * 50)
        print(result)
        print("=" * 50)

    except Exception as e:
        print(f"整合失敗：{e}")

if __name__ == "__main__":
    test_ai_integration()