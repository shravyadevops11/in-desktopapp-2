# Quick Start Without AI (For Testing)

If you want to test the app without setting up the AI key first, follow these steps:

## Option 1: Run Without AI (Fastest)

Create a file `backend/ai_service_mock.py`:

```python
import logging

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        logger.info("Using MOCK AI Service (no real AI)")
    
    async def get_response(self, session_id: str, user_message: str, model: str = "GPT-5.2", 
                          image_data: str = None, audio_data: str = None) -> str:
        return f"[MOCK RESPONSE] This is a test response to: '{user_message}'. Real AI is not configured yet. Add EMERGENT_LLM_KEY to .env to enable GPT-5.2."

ai_service = AIService()
```

Then in `backend/routes/chat.py`, change line 5 from:
```python
from ai_service import ai_service
```
to:
```python
from ai_service_mock import ai_service
```

Now run:
```powershell
python -m uvicorn server:app --host localhost --port 8001
```

This will let you test the app without AI first!

---

## Option 2: Add the LLM Key

Check if your `.env` file exists and has the key:

```powershell
cd backend
type .env
```

It should show:
```
EMERGENT_LLM_KEY=sk-emergent-14f8cAd188e61AaA00
```

If the file is missing or incomplete, create/update it:

```powershell
echo EMERGENT_LLM_KEY=sk-emergent-14f8cAd188e61AaA00 > .env
```

---

## Option 3: Python Version Issue

You're using **Python 3.14** which is very new and has compatibility issues. Consider using **Python 3.11** instead:

1. Download Python 3.11 from https://www.python.org/downloads/
2. Install it
3. Create virtual environment:
```powershell
py -3.11 -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
pip install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
python -m uvicorn server:app --host localhost --port 8001
```

---

## Recommended: Try Mock Version First

The easiest way forward:

1. **Pull latest code** (I've updated ai_service.py to not crash)
2. **Test backend**:
```powershell
cd backend
python -m uvicorn server:app --host localhost --port 8001
```

If it still fails, use the mock version above to at least get the app running and test the UI!
