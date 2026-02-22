#!/usr/bin/env python3
"""
Mental Health Companion Backend Server
Handles AI features without Streamlit
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime
import sqlite3
import hashlib

# Import our custom modules
from text_mood_detector import TextMoodDetector
from image_mood_detector import ImageMoodDetector
from gemini_integration import GeminiIntegration
from database import DatabaseManager

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize components
text_detector = TextMoodDetector()
image_detector = ImageMoodDetector()
gemini = GeminiIntegration()
db = DatabaseManager()

# Serve static files
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

@app.route('/api/analyze-text', methods=['POST'])
def analyze_text():
    """Analyze text for mood and sentiment"""
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text.strip():
            return jsonify({'error': 'No text provided'}), 400
        
        # Analyze text
        analysis = text_detector.analyze_text_mood(text)
        
        # Generate response
        gemini_response = gemini.generate_response(
            analysis['detected_emotion'],
            text,
            analysis
        )
        
        return jsonify({
            'mood': analysis['detected_emotion'],
            'sentiment_score': analysis['sentiment_score'],
            'confidence_score': analysis['confidence_score'],
            'response': gemini_response['response'],
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-image', methods=['POST'])
def analyze_image():
    """Analyze image for emotion"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        image = request.files['image']
        
        # Validate image
        is_valid, message = image_detector.validate_image(image)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # Save temporary image
        temp_path = image_detector.save_uploaded_image(image)
        if not temp_path:
            return jsonify({'error': 'Failed to save image'}), 500
        
        # Analyze image
        analysis = image_detector.analyze_image_mood(temp_path)
        
        # Generate response
        gemini_response = gemini.generate_response(
            analysis['detected_emotion'],
            "Image-based emotion detection",
            analysis
        )
        
        # Clean up temp file
        image_detector.cleanup_temp_file(temp_path)
        
        return jsonify({
            'mood': analysis['detected_emotion'],
            'confidence_score': analysis['confidence_score'],
            'face_detected': analysis['face_detected'],
            'response': gemini_response['response'],
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat endpoint with AI responses"""
    try:
        data = request.json
        message = data.get('message', '')
        user_id = data.get('user_id', 1)
        
        if not message.strip():
            return jsonify({'error': 'No message provided'}), 400
        
        # Analyze message for mood
        analysis = text_detector.analyze_text_mood(message)
        
        # Generate AI response
        gemini_response = gemini.generate_response(
            analysis['detected_emotion'],
            message,
            analysis
        )
        
        # Save to database
        db.save_chat_message(user_id, message, gemini_response['response'], analysis['detected_emotion'])
        
        return jsonify({
            'response': gemini_response['response'],
            'detected_emotion': analysis['detected_emotion'],
            'confidence_score': analysis['confidence_score'],
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mood-history', methods=['GET'])
def mood_history():
    """Get mood history for user"""
    try:
        user_id = request.args.get('user_id', 1)
        
        # Get mood entries
        mood_entries = db.get_user_mood_history(user_id, limit=50)
        
        return jsonify({
            'mood_history': mood_entries,
            'total_entries': len(mood_entries)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/save-mood', methods=['POST'])
def save_mood():
    """Save mood entry"""
    try:
        data = request.json
        user_id = data.get('user_id', 1)
        mood = data.get('mood', '')
        text = data.get('text', '')
        
        if not mood:
            return jsonify({'error': 'No mood provided'}), 400
        
        # Save to database
        entry_id = db.save_mood_entry(
            user_id=user_id,
            text_input=text,
            detected_emotion=mood,
            sentiment_score=0.0,
            confidence_score=0.8,
            gemini_response=""
        )
        
        return jsonify({
            'success': True,
            'entry_id': entry_id,
            'message': 'Mood saved successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'features': {
            'text_analysis': True,
            'image_analysis': True,
            'gemini_api': gemini.is_api_available(),
            'database': True
        }
    })

if __name__ == '__main__':
    print("🧠 Mental Health Companion Backend Server")
    print("🚀 Starting server on http://localhost:5000")
    print("📝 Frontend available at http://localhost:8080")
    print("🔗 API endpoints available at http://localhost:5000")
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
