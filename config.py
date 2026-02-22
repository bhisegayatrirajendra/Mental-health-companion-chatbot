import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Gemini API Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "your_gemini_api_key_here")
    
    # Database Configuration
    DATABASE_URL = "sqlite:///mental_health_companion.db"
    
    # Emotion Detection Models
    EMOTION_LABELS = ["Happy", "Sad", "Angry", "Stressed", "Anxious", "Neutral", "Surprised", "Fear"]
    
    # Sentiment Thresholds
    POSITIVE_THRESHOLD = 0.1
    NEGATIVE_THRESHOLD = -0.1
    
    # File Upload Configuration
    ALLOWED_IMAGE_TYPES = ["jpg", "jpeg", "png", "webp"]
    MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
    
    # UI Configuration
    APP_TITLE = "🧠 Mental Health Companion"
    APP_DESCRIPTION = "AI-Based Mood Detection + Gemini API Powered Suggestion Engine"
    
    # Disclaimer
    DISCLAIMER = "⚠️ **Disclaimer**: This chatbot is not a replacement for professional medical help. If you're experiencing severe mental health issues, please consult a qualified healthcare professional."
