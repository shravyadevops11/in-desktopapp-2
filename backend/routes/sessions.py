from fastapi import APIRouter, HTTPException
from models import Session, SessionCreate
from typing import List
from datetime import datetime
import logging
from database import SessionDB

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/sessions", response_model=Session)
async def create_session(session_input: SessionCreate):
    """Create a new interview session"""
    try:
        session = Session(**session_input.dict())
        await SessionDB.create(session.dict())
        logger.info(f"Created new session: {session.id}")
        return session
    except Exception as e:
        logger.error(f"Error creating session: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create session: {str(e)}")


@router.get("/sessions", response_model=List[Session])
async def get_sessions():
    """Get all sessions"""
    try:
        sessions = await SessionDB.get_all()
        return [Session(**session) for session in sessions]
    except Exception as e:
        logger.error(f"Error fetching sessions: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch sessions: {str(e)}")


@router.get("/sessions/{session_id}", response_model=Session)
async def get_session(session_id: str):
    """Get a specific session by ID"""
    try:
        session = await SessionDB.get_by_id(session_id)
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
        deleted = await SessionDB.delete(session_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Session not found")
        
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
        await SessionDB.update_stats(session_id, questions_asked, duration)
        return {"success": True}
    except Exception as e:
        logger.error(f"Error updating session stats: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to update session: {str(e)}")
