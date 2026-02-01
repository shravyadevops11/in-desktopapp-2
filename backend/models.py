from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime
import uuid


class Session(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    date: datetime = Field(default_factory=datetime.utcnow)
    duration: str = "0 mins"
    questionsAsked: int = 0
    model: str = "GPT-5.2"
    createdAt: datetime = Field(default_factory=datetime.utcnow)
    updatedAt: datetime = Field(default_factory=datetime.utcnow)


class SessionCreate(BaseModel):
    title: str
    model: str = "GPT-5.2"


class Message(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sessionId: str
    type: Literal["user", "assistant"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    messageType: Optional[str] = "text"  # text, audio, image
    audioUrl: Optional[str] = None
    imageUrl: Optional[str] = None


class MessageCreate(BaseModel):
    sessionId: str
    message: str
    model: str = "GPT-5.2"
    messageType: Optional[str] = "text"
    imageData: Optional[str] = None  # base64 encoded image
    audioData: Optional[str] = None  # base64 encoded audio


class InputHistory(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sessionId: str
    input: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class InputHistoryCreate(BaseModel):
    sessionId: str
    input: str
