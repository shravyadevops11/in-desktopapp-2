from fastapi import APIRouter, HTTPException
from models import InputHistory, InputHistoryCreate
from motor.motor_asyncio import AsyncIOMotorClient
import os
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Get database connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]


@router.post("/input-history")
async def save_input(input_data: InputHistoryCreate):
    """Save user input to history"""
    try:
        input_history = InputHistory(**input_data.dict())
        await db.input_history.insert_one(input_history.dict())
        logger.info(f"Saved input to history for session {input_data.sessionId}")
        return {"success": True}
    except Exception as e:
        logger.error(f"Error saving input history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to save input: {str(e)}")


@router.get("/input-history", response_model=List[str])
async def get_input_history():
    """Get all input history"""
    try:
        history = await db.input_history.find().sort("timestamp", -1).limit(100).to_list(100)
        return [item["input"] for item in history]
    except Exception as e:
        logger.error(f"Error fetching input history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch history: {str(e)}")


@router.get("/input-history/{session_id}", response_model=List[InputHistory])
async def get_session_input_history(session_id: str):
    """Get input history for a specific session"""
    try:
        history = await db.input_history.find({"sessionId": session_id}).sort("timestamp", 1).to_list(1000)
        return [InputHistory(**item) for item in history]
    except Exception as e:
        logger.error(f"Error fetching session input history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch history: {str(e)}")
