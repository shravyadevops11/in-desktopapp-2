from fastapi import APIRouter, HTTPException
from models import InputHistory, InputHistoryCreate
from typing import List
import logging
from database import InputHistoryDB

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/input-history")
async def save_input(input_data: InputHistoryCreate):
    """Save user input to history"""
    try:
        input_history = InputHistory(**input_data.dict())
        await InputHistoryDB.create(input_history.dict())
        logger.info(f"Saved input to history for session {input_data.sessionId}")
        return {"success": True}
    except Exception as e:
        logger.error(f"Error saving input history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to save input: {str(e)}")


@router.get("/input-history", response_model=List[str])
async def get_input_history():
    """Get all input history"""
    try:
        history = await InputHistoryDB.get_all()
        return history
    except Exception as e:
        logger.error(f"Error fetching input history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch history: {str(e)}")


@router.get("/input-history/{session_id}", response_model=List[InputHistory])
async def get_session_input_history(session_id: str):
    """Get input history for a specific session"""
    try:
        history = await InputHistoryDB.get_by_session(session_id)
        return [InputHistory(**item) for item in history]
    except Exception as e:
        logger.error(f"Error fetching session input history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch history: {str(e)}")
