# Backend Integration Contracts - "In" AI Interview Assistant

## API Contracts

### 1. Sessions API

**POST /api/sessions**
- Create a new session
- Request: `{ title: string, model: string }`
- Response: `{ id: string, title: string, date: string, duration: string, questionsAsked: number, model: string }`

**GET /api/sessions**
- Retrieve all sessions for history
- Response: `[Session]`

**GET /api/sessions/:id**
- Get specific session details
- Response: `Session`

**DELETE /api/sessions/:id**
- Delete a session
- Response: `{ success: boolean }`

### 2. Chat API

**POST /api/chat**
- Send a message to AI and get response
- Request: `{ sessionId: string, message: string, model: string }`
- Response: `{ id: string, type: 'assistant', content: string, timestamp: string }`

**GET /api/chat/:sessionId**
- Get all messages for a session
- Response: `[Message]`

### 3. Input History API

**POST /api/input-history**
- Save user input to history
- Request: `{ input: string, sessionId: string }`
- Response: `{ success: boolean }`

**GET /api/input-history**
- Get all input history
- Response: `[string]`

## Database Models

### Session Model
```python
{
  id: str (UUID)
  title: str
  date: datetime
  duration: str
  questionsAsked: int
  model: str (default: "GPT-5.2")
  createdAt: datetime
  updatedAt: datetime
}
```

### Message Model
```python
{
  id: str (UUID)
  sessionId: str
  type: str ('user' | 'assistant')
  content: str
  timestamp: datetime
}
```

### InputHistory Model
```python
{
  id: str (UUID)
  sessionId: str
  input: str
  timestamp: datetime
}
```

## Mock Data Replacement

### Frontend Changes Required
1. Replace mockSessions in `mockData.js` with API call to `/api/sessions`
2. Replace mockChatHistory with API call to `/api/chat/:sessionId`
3. Replace mockInputHistory with API call to `/api/input-history`
4. Update DesktopApp.jsx to call `/api/chat` for AI responses
5. Update App.js to create session via API when starting new session

## Backend Implementation Plan

1. **Install Dependencies**
   - emergentintegrations (for GPT-5.2 integration)
   - Add EMERGENT_LLM_KEY to .env

2. **Create Models**
   - Session model
   - Message model
   - InputHistory model

3. **Create Routes**
   - Sessions routes (CRUD)
   - Chat routes (send message, get history)
   - Input history routes

4. **GPT-5.2 Integration**
   - Use emergentintegrations.llm.chat.LlmChat
   - Initialize with EMERGENT_LLM_KEY
   - Configure with model "openai", "gpt-5.2"
   - Store all messages in MongoDB for history

5. **Frontend Integration**
   - Create axios service for API calls
   - Replace mock data with real API calls
   - Add loading states
   - Add error handling

## Integration Flow

1. User clicks "Start New Session" → POST /api/sessions → Creates session in DB
2. User sends message → POST /api/chat → Stores user message → Calls GPT-5.2 → Stores AI response → Returns to frontend
3. User opens History → GET /api/sessions → Shows all sessions
4. User clicks session → GET /api/chat/:sessionId → Loads conversation
5. All inputs stored via POST /api/input-history for future reference
