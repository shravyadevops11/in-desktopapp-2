from fastapi import APIRouter, HTTPException
from models import Message, MessageCreate
from typing import List
import logging
from ai_service import ai_service
from datetime import datetime
from database import MessageDB

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/chat", response_model=Message)
async def send_message(message_input: MessageCreate):
    """Send a message to AI and get response"""
    try:
        # Save user message
        user_message = Message(
            sessionId=message_input.sessionId,
            type="user",
            content=message_input.message,
            messageType=message_input.messageType or "text",
            imageUrl=message_input.imageData if message_input.imageData else None
        )
        await MessageDB.create(user_message.dict())
        logger.info(f"Saved user message for session {message_input.sessionId}")
        
        # Get AI response
        ai_response_text = await ai_service.get_response(
            session_id=message_input.sessionId,
            user_message=message_input.message,
            model=message_input.model,
            image_data=message_input.imageData,
            audio_data=message_input.audioData
        )
        
        # Save AI response
        ai_message = Message(
            sessionId=message_input.sessionId,
            type="assistant",
            content=ai_response_text,
            messageType="text"
        )
        await MessageDB.create(ai_message.dict())
        logger.info(f"Saved AI response for session {message_input.sessionId}")
        
        # Update session question count
        await MessageDB.increment_question_count(message_input.sessionId)
        
        return ai_message
        
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process message: {str(e)}")


@router.get("/chat/{session_id}", response_model=List[Message])
async def get_messages(session_id: str):
    """Get all messages for a session"""
    try:
        messages = await MessageDB.get_by_session(session_id)
        return [Message(**msg) for msg in messages]
    except Exception as e:
        logger.error(f"Error fetching messages: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch messages: {str(e)}")


@router.delete("/chat/{session_id}")
async def delete_messages(session_id: str):
    """Delete all messages for a session"""
    try:
        deleted_count = await MessageDB.delete_by_session(session_id)
        logger.info(f"Deleted {deleted_count} messages for session {session_id}")
        return {"success": True, "deleted_count": deleted_count}
    except Exception as e:
        logger.error(f"Error deleting messages: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete messages: {str(e)}")
