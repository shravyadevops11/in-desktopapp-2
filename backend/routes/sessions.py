from fastapi import APIRouter, HTTPException
from models import Session, SessionCreate
from motor.motor_asyncio import AsyncIOMotorClient
import os
from typing import List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Get database connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]


@router.post("/sessions", response_model=Session)
async def create_session(session_input: SessionCreate):
    """Create a new interview session"""
    try:
        session = Session(**session_input.dict())
        await db.sessions.insert_one(session.dict())
        logger.info(f"Created new session: {session.id}")
        return session
    except Exception as e:
        logger.error(f"Error creating session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")


@router.get("/sessions", response_model=List[Session])
async def get_sessions():
    """Get all sessions"""
    try:
        sessions = await db.sessions.find().sort("createdAt", -1).to_list(1000)
        return [Session(**session) for session in sessions]
    except Exception as e:
        logger.error(f"Error fetching sessions: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch sessions: {str(e)}")


@router.get("/sessions/{session_id}", response_model=Session)
async def get_session(session_id: str):
    """Get a specific session by ID"""
    try:
        session = await db.sessions.find_one({"id": session_id})
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return Session(**session)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch session: {str(e)}")


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a session"""
    try:
        result = await db.sessions.delete_one({"id": session_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Also delete all messages for this session
        await db.messages.delete_many({"sessionId": session_id})
        await db.input_history.delete_many({"sessionId": session_id})
        
        logger.info(f"Deleted session: {session_id}")
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete session: {str(e)}")


@router.patch("/sessions/{session_id}/update-stats")
async def update_session_stats(session_id: str, questions_asked: int, duration: str):
    """Update session statistics"""
    try:
        await db.sessions.update_one(
            {"id": session_id},
            {
                "$set": {
                    "questionsAsked": questions_asked,
                    "duration": duration,
                    "updatedAt": datetime.utcnow()
                }
            }
        )
        return {"success": True}
    except Exception as e:
        logger.error(f"Error updating session stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update session: {str(e)}")
