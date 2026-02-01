import sqlite3
import json
from datetime import datetime
from typing import List, Optional
import uuid
import os
from pathlib import Path

# Database file location
DB_PATH = Path(__file__).parent / "in_app.db"

def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            duration TEXT DEFAULT '0 mins',
            questionsAsked INTEGER DEFAULT 0,
            model TEXT DEFAULT 'GPT-5.2',
            createdAt TEXT NOT NULL,
            updatedAt TEXT NOT NULL
        )
    """)
    
    # Messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            sessionId TEXT NOT NULL,
            type TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            messageType TEXT DEFAULT 'text',
            audioUrl TEXT,
            imageUrl TEXT,
            FOREIGN KEY (sessionId) REFERENCES sessions (id)
        )
    """)
    
    # Input history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS input_history (
            id TEXT PRIMARY KEY,
            sessionId TEXT NOT NULL,
            input TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (sessionId) REFERENCES sessions (id)
        )
    """)
    
    conn.commit()
    conn.close()

# Initialize database on import
init_db()

class SessionDB:
    @staticmethod
    async def create(session_data: dict) -> dict:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sessions (id, title, date, duration, questionsAsked, model, createdAt, updatedAt)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session_data['id'],
            session_data['title'],
            session_data['date'].isoformat() if isinstance(session_data['date'], datetime) else session_data['date'],
            session_data.get('duration', '0 mins'),
            session_data.get('questionsAsked', 0),
            session_data.get('model', 'GPT-5.2'),
            session_data['createdAt'].isoformat() if isinstance(session_data['createdAt'], datetime) else session_data['createdAt'],
            session_data['updatedAt'].isoformat() if isinstance(session_data['updatedAt'], datetime) else session_data['updatedAt']
        ))
        conn.commit()
        conn.close()
        return session_data
    
    @staticmethod
    async def get_all() -> List[dict]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sessions ORDER BY createdAt DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    @staticmethod
    async def get_by_id(session_id: str) -> Optional[dict]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None
    
    @staticmethod
    async def delete(session_id: str) -> bool:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
        cursor.execute("DELETE FROM messages WHERE sessionId = ?", (session_id,))
        cursor.execute("DELETE FROM input_history WHERE sessionId = ?", (session_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()
        return deleted
    
    @staticmethod
    async def update_stats(session_id: str, questions_asked: int, duration: str):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE sessions 
            SET questionsAsked = ?, duration = ?, updatedAt = ?
            WHERE id = ?
        """, (questions_asked, duration, datetime.utcnow().isoformat(), session_id))
        conn.commit()
        conn.close()

class MessageDB:
    @staticmethod
    async def create(message_data: dict) -> dict:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO messages (id, sessionId, type, content, timestamp, messageType, audioUrl, imageUrl)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            message_data['id'],
            message_data['sessionId'],
            message_data['type'],
            message_data['content'],
            message_data['timestamp'].isoformat() if isinstance(message_data['timestamp'], datetime) else message_data['timestamp'],
            message_data.get('messageType', 'text'),
            message_data.get('audioUrl'),
            message_data.get('imageUrl')
        ))
        conn.commit()
        conn.close()
        return message_data
    
    @staticmethod
    async def get_by_session(session_id: str) -> List[dict]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM messages WHERE sessionId = ? ORDER BY timestamp ASC", (session_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    @staticmethod
    async def delete_by_session(session_id: str) -> int:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM messages WHERE sessionId = ?", (session_id,))
        conn.commit()
        deleted = cursor.rowcount
        conn.close()
        return deleted
    
    @staticmethod
    async def increment_question_count(session_id: str):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE sessions 
            SET questionsAsked = questionsAsked + 1, updatedAt = ?
            WHERE id = ?
        """, (datetime.utcnow().isoformat(), session_id))
        conn.commit()
        conn.close()

class InputHistoryDB:
    @staticmethod
    async def create(input_data: dict) -> dict:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO input_history (id, sessionId, input, timestamp)
            VALUES (?, ?, ?, ?)
        """, (
            input_data['id'],
            input_data['sessionId'],
            input_data['input'],
            input_data['timestamp'].isoformat() if isinstance(input_data['timestamp'], datetime) else input_data['timestamp']
        ))
        conn.commit()
        conn.close()
        return input_data
    
    @staticmethod
    async def get_all() -> List[str]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT input FROM input_history ORDER BY timestamp DESC LIMIT 100")
        rows = cursor.fetchall()
        conn.close()
        return [row['input'] for row in rows]
    
    @staticmethod
    async def get_by_session(session_id: str) -> List[dict]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM input_history WHERE sessionId = ? ORDER BY timestamp ASC", (session_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
