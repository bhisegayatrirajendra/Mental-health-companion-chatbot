import sqlite3
import hashlib
import json
from datetime import datetime
from typing import Optional, List, Dict, Any

class DatabaseManager:
    def __init__(self, db_url: str = "sqlite:///mental_health_companion.db"):
        self.db_path = db_url.replace("sqlite:///", "")
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE,
                    password_hash TEXT NOT NULL,
                    is_anonymous BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    profile_data TEXT
                )
            ''')
            
            # Mood entries table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS mood_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    text_input TEXT,
                    image_path TEXT,
                    detected_emotion TEXT,
                    sentiment_score REAL,
                    confidence_score REAL,
                    gemini_response TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Chat history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    message TEXT NOT NULL,
                    response TEXT NOT NULL,
                    emotion_detected TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            conn.commit()
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username: str, email: Optional[str] = None, 
                   password: Optional[str] = None, is_anonymous: bool = False) -> int:
        """Create a new user"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if is_anonymous:
                password_hash = self.hash_password(f"anonymous_{username}_{datetime.now()}")
            else:
                password_hash = self.hash_password(password) if password else None
            
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, is_anonymous)
                VALUES (?, ?, ?, ?)
            ''', (username, email, password_hash, is_anonymous))
            
            conn.commit()
            return cursor.lastrowid
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user credentials"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            password_hash = self.hash_password(password)
            
            cursor.execute('''
                SELECT id, username, email, is_anonymous, profile_data
                FROM users 
                WHERE username = ? AND password_hash = ? AND is_anonymous = FALSE
            ''', (username, password_hash))
            
            result = cursor.fetchone()
            if result:
                return {
                    'id': result[0],
                    'username': result[1],
                    'email': result[2],
                    'is_anonymous': bool(result[3]),
                    'profile_data': json.loads(result[4]) if result[4] else {}
                }
        return None
    
    def save_mood_entry(self, user_id: int, text_input: Optional[str] = None,
                       image_path: Optional[str] = None, detected_emotion: str = "",
                       sentiment_score: float = 0.0, confidence_score: float = 0.0,
                       gemini_response: str = "") -> int:
        """Save mood detection entry"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO mood_entries 
                (user_id, text_input, image_path, detected_emotion, 
                 sentiment_score, confidence_score, gemini_response)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, text_input, image_path, detected_emotion,
                  sentiment_score, confidence_score, gemini_response))
            
            conn.commit()
            return cursor.lastrowid
    
    def save_chat_message(self, user_id: int, message: str, response: str,
                         emotion_detected: Optional[str] = None) -> int:
        """Save chat message and response"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO chat_history (user_id, message, response, emotion_detected)
                VALUES (?, ?, ?, ?)
            ''', (user_id, message, response, emotion_detected))
            
            conn.commit()
            return cursor.lastrowid
    
    def get_user_mood_history(self, user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Get user's mood history"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT detected_emotion, sentiment_score, confidence_score, 
                       gemini_response, timestamp, text_input
                FROM mood_entries 
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (user_id, limit))
            
            results = cursor.fetchall()
            return [
                {
                    'emotion': row[0],
                    'sentiment_score': row[1],
                    'confidence_score': row[2],
                    'gemini_response': row[3],
                    'timestamp': row[4],
                    'text_input': row[5]
                }
                for row in results
            ]
    
    def get_chat_history(self, user_id: int, limit: int = 20) -> List[Dict[str, Any]]:
        """Get user's chat history"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT message, response, emotion_detected, timestamp
                FROM chat_history 
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (user_id, limit))
            
            results = cursor.fetchall()
            return [
                {
                    'message': row[0],
                    'response': row[1],
                    'emotion_detected': row[2],
                    'timestamp': row[3]
                }
                for row in results
            ]
