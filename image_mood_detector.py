import cv2
import numpy as np
from deepface import DeepFace
from PIL import Image
import tempfile
import os
from typing import Dict, List, Tuple, Optional

class ImageMoodDetector:
    def __init__(self):
        """Initialize image-based emotion detection"""
        self.emotion_labels = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]
        
        # Map deepface emotions to our emotion categories
        self.emotion_mapping = {
            "angry": "Angry",
            "disgust": "Angry",  # Map disgust to angry
            "fear": "Anxious",
            "happy": "Happy",
            "sad": "Sad",
            "surprise": "Surprised",
            "neutral": "Neutral"
        }
    
    def preprocess_image(self, image_path: str) -> Optional[np.ndarray]:
        """Preprocess image for emotion detection"""
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                return None
            
            # Convert to RGB (DeepFace expects RGB)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            return image_rgb
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return None
    
    def detect_faces(self, image_path: str) -> List[Dict]:
        """Detect faces in the image"""
        try:
            # Use OpenCV's Haar Cascade for face detection
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
            image = cv2.imread(image_path)
            if image is None:
                return []
            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            face_info = []
            for (x, y, w, h) in faces:
                face_info.append({
                    'x': x,
                    'y': y,
                    'width': w,
                    'height': h,
                    'confidence': 1.0  # Haar Cascade doesn't provide confidence
                })
            
            return face_info
            
        except Exception as e:
            print(f"Error detecting faces: {e}")
            return []
    
    def analyze_emotion_deepface(self, image_path: str) -> Dict[str, any]:
        """Analyze emotion using DeepFace"""
        try:
            # Analyze emotion with DeepFace
            analysis = DeepFace.analyze(
                img_path=image_path,
                actions=['emotion'],
                enforce_detection=False,  # Don't fail if no face is detected
                detector_backend='opencv'
            )
            
            if isinstance(analysis, list):
                analysis = analysis[0]  # Take first face if multiple
            
            emotions = analysis.get('emotion', {})
            dominant_emotion = analysis.get('dominant_emotion', 'neutral')
            region = analysis.get('region', {})
            
            # Map to our emotion categories
            mapped_emotions = {}
            for emotion, score in emotions.items():
                mapped_emotion = self.emotion_mapping.get(emotion.lower(), emotion)
                mapped_emotions[mapped_emotion] = mapped_emotions.get(mapped_emotion, 0) + score
            
            # Get dominant emotion
            if mapped_emotions:
                detected_emotion = max(mapped_emotions, key=mapped_emotions.get)
                confidence_score = mapped_emotions[detected_emotion]
            else:
                detected_emotion = "Neutral"
                confidence_score = 0.5
            
            return {
                "detected_emotion": detected_emotion,
                "confidence_score": confidence_score,
                "face_detected": bool(region),
                "face_region": region,
                "all_emotions": mapped_emotions,
                "raw_emotions": emotions,
                "dominant_deepface_emotion": dominant_emotion
            }
            
        except Exception as e:
            print(f"Error in DeepFace analysis: {e}")
            return {
                "detected_emotion": "Neutral",
                "confidence_score": 0.0,
                "face_detected": False,
                "face_region": {},
                "all_emotions": {},
                "raw_emotions": {},
                "error": str(e)
            }
    
    def analyze_image_mood(self, image_path: str) -> Dict[str, any]:
        """Comprehensive image mood analysis"""
        if not os.path.exists(image_path):
            return {
                "detected_emotion": "Neutral",
                "confidence_score": 0.0,
                "face_detected": False,
                "error": "Image file not found"
            }
        
        # Preprocess image
        processed_image = self.preprocess_image(image_path)
        if processed_image is None:
            return {
                "detected_emotion": "Neutral",
                "confidence_score": 0.0,
                "face_detected": False,
                "error": "Could not process image"
            }
        
        # Detect faces
        faces = self.detect_faces(image_path)
        
        # Analyze emotion with DeepFace
        emotion_analysis = self.analyze_emotion_deepface(image_path)
        
        # Add face detection info
        emotion_analysis["num_faces"] = len(faces)
        emotion_analysis["face_details"] = faces
        
        # If no face detected, try to analyze overall image mood
        if not emotion_analysis["face_detected"]:
            emotion_analysis["detected_emotion"] = "Neutral"
            emotion_analysis["confidence_score"] = 0.3
            emotion_analysis["note"] = "No face detected, defaulting to neutral emotion"
        
        return emotion_analysis
    
    def save_uploaded_image(self, uploaded_file) -> Optional[str]:
        """Save uploaded image to temporary file"""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                # Write uploaded file to temporary file
                tmp_file.write(uploaded_file.getvalue())
                return tmp_file.name
        except Exception as e:
            print(f"Error saving uploaded image: {e}")
            return None
    
    def cleanup_temp_file(self, file_path: str):
        """Clean up temporary file"""
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error cleaning up temp file: {e}")
    
    def get_emotion_emoji(self, emotion: str) -> str:
        """Get emoji for emotion"""
        emotion_emojis = {
            "Happy": "😊",
            "Sad": "😢",
            "Angry": "😠",
            "Stressed": "😰",
            "Anxious": "😟",
            "Neutral": "😐",
            "Surprised": "😲",
            "Fear": "😨"
        }
        return emotion_emojis.get(emotion, "😐")
    
    def validate_image(self, uploaded_file) -> Tuple[bool, str]:
        """Validate uploaded image"""
        # Check file size (5MB limit)
        if uploaded_file.size > 5 * 1024 * 1024:
            return False, "Image size should be less than 5MB"
        
        # Check file type
        allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp"]
        if uploaded_file.type not in allowed_types:
            return False, "Only JPEG, PNG, and WebP images are supported"
        
        # Try to open the image to verify it's valid
        try:
            image = Image.open(uploaded_file)
            image.verify()  # Verify it's a valid image
            return True, "Valid image"
        except Exception as e:
            return False, f"Invalid image file: {str(e)}"
    
    def get_emotion_description(self, emotion: str) -> str:
        """Get description for detected emotion"""
        descriptions = {
            "Happy": "You appear to be feeling joyful and positive! 😊",
            "Sad": "You seem to be feeling down or melancholic. It's okay to feel this way. 😢",
            "Angry": "You appear to be feeling frustrated or upset. Take a deep breath. 😠",
            "Stressed": "You seem to be feeling overwhelmed or tense. Let's work through this. 😰",
            "Anxious": "You appear to be feeling worried or nervous. You're not alone in this. 😟",
            "Neutral": "You appear to be in a calm, balanced state. 😐",
            "Surprised": "You seem to be feeling surprised or shocked! 😲",
            "Fear": "You appear to be feeling scared or fearful. It's okay to feel afraid. 😨"
        }
        return descriptions.get(emotion, "Your emotional state has been detected.")
