import re
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline
import torch
from typing import Dict, List, Tuple, Optional

class TextMoodDetector:
    def __init__(self):
        """Initialize text-based mood detection models"""
        self.vader_analyzer = SentimentIntensityAnalyzer()
        
        # Initialize BERT emotion classifier
        try:
            self.emotion_classifier = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                return_all_scores=True,
                device=0 if torch.cuda.is_available() else -1
            )
        except Exception as e:
            print(f"Error loading emotion classifier: {e}")
            self.emotion_classifier = None
        
        # Emotion keywords mapping
        self.emotion_keywords = {
            "Happy": ["happy", "joy", "excited", "glad", "cheerful", "delighted", "pleased", "content", "satisfied"],
            "Sad": ["sad", "depressed", "unhappy", "miserable", "down", "blue", "gloomy", "melancholy", "heartbroken"],
            "Angry": ["angry", "mad", "furious", "irritated", "annoyed", "frustrated", "rage", "upset", "resentful"],
            "Stressed": ["stressed", "overwhelmed", "pressured", "tense", "anxious", "worried", "burdened", "strained"],
            "Anxious": ["anxious", "nervous", "worried", "apprehensive", "fearful", "uneasy", "restless", "panicked"],
            "Neutral": ["okay", "fine", "normal", "alright", "neutral", "balanced", "calm", "peaceful"]
        }
    
    def preprocess_text(self, text: str) -> str:
        """Preprocess text for analysis"""
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove user mentions and hashtags
        text = re.sub(r'@\w+|#\w+', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def get_vader_sentiment(self, text: str) -> Dict[str, float]:
        """Get VADER sentiment scores"""
        scores = self.vader_analyzer.polarity_scores(text)
        return scores
    
    def get_textblob_sentiment(self, text: str) -> Tuple[float, float]:
        """Get TextBlob sentiment and subjectivity"""
        blob = TextBlob(text)
        return blob.sentiment.polarity, blob.sentiment.subjectivity
    
    def detect_emotion_keywords(self, text: str) -> Dict[str, int]:
        """Detect emotions based on keyword matching"""
        text_lower = text.lower()
        emotion_counts = {}
        
        for emotion, keywords in self.emotion_keywords.items():
            count = sum(1 for keyword in keywords if keyword in text_lower)
            if count > 0:
                emotion_counts[emotion] = count
        
        return emotion_counts
    
    def classify_emotion_bert(self, text: str) -> Dict[str, float]:
        """Classify emotion using BERT model"""
        if not self.emotion_classifier:
            return {}
        
        try:
            results = self.emotion_classifier(text)
            if results and len(results) > 0:
                # Convert to dictionary format
                emotion_scores = {}
                for result in results[0]:
                    label = result['label']
                    score = result['score']
                    
                    # Map BERT labels to our emotion categories
                    if label.lower() in ['joy', 'happiness']:
                        emotion_scores['Happy'] = score
                    elif label.lower() in ['sadness', 'sad']:
                        emotion_scores['Sad'] = score
                    elif label.lower() in ['anger', 'angry']:
                        emotion_scores['Angry'] = score
                    elif label.lower() in ['fear', 'anxiety']:
                        emotion_scores['Anxious'] = score
                    elif label.lower() in ['neutral']:
                        emotion_scores['Neutral'] = score
                
                return emotion_scores
        except Exception as e:
            print(f"Error in BERT emotion classification: {e}")
        
        return {}
    
    def analyze_text_mood(self, text: str) -> Dict[str, any]:
        """Comprehensive text mood analysis"""
        if not text or not text.strip():
            return {
                "detected_emotion": "Neutral",
                "sentiment_score": 0.0,
                "confidence_score": 0.0,
                "analysis_details": {
                    "vader_scores": {},
                    "textblob_scores": {"polarity": 0.0, "subjectivity": 0.0},
                    "keyword_emotions": {},
                    "bert_emotions": {}
                }
            }
        
        # Preprocess text
        processed_text = self.preprocess_text(text)
        
        # Get VADER sentiment
        vader_scores = self.get_vader_sentiment(processed_text)
        
        # Get TextBlob sentiment
        textblob_polarity, textblob_subjectivity = self.get_textblob_sentiment(processed_text)
        
        # Detect emotion keywords
        keyword_emotions = self.detect_emotion_keywords(processed_text)
        
        # Get BERT emotion classification
        bert_emotions = self.classify_emotion_bert(processed_text)
        
        # Combine all emotion detection methods
        emotion_scores = {}
        
        # Add keyword-based emotions
        for emotion, count in keyword_emotions.items():
            emotion_scores[emotion] = emotion_scores.get(emotion, 0) + (count * 0.3)
        
        # Add BERT-based emotions
        for emotion, score in bert_emotions.items():
            emotion_scores[emotion] = emotion_scores.get(emotion, 0) + (score * 0.5)
        
        # Add sentiment-based emotion mapping
        compound_score = vader_scores['compound']
        if compound_score >= 0.05:
            emotion_scores['Happy'] = emotion_scores.get('Happy', 0) + (compound_score * 0.2)
        elif compound_score <= -0.05:
            if textblob_subjectivity > 0.5:  # More subjective
                emotion_scores['Sad'] = emotion_scores.get('Sad', 0) + (abs(compound_score) * 0.2)
            else:
                emotion_scores['Angry'] = emotion_scores.get('Angry', 0) + (abs(compound_score) * 0.2)
        
        # Determine dominant emotion
        if emotion_scores:
            detected_emotion = max(emotion_scores, key=emotion_scores.get)
            confidence_score = emotion_scores[detected_emotion]
        else:
            detected_emotion = "Neutral"
            confidence_score = 0.5
        
        # Normalize confidence score
        confidence_score = min(confidence_score, 1.0)
        
        # Use compound sentiment score as overall sentiment
        sentiment_score = compound_score
        
        return {
            "detected_emotion": detected_emotion,
            "sentiment_score": sentiment_score,
            "confidence_score": confidence_score,
            "analysis_details": {
                "vader_scores": vader_scores,
                "textblob_scores": {"polarity": textblob_polarity, "subjectivity": textblob_subjectivity},
                "keyword_emotions": keyword_emotions,
                "bert_emotions": bert_emotions
            }
        }
    
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
    
    def get_sentiment_label(self, score: float) -> str:
        """Get sentiment label from score"""
        if score >= 0.05:
            return "Positive 😊"
        elif score <= -0.05:
            return "Negative 😔"
        else:
            return "Neutral 😐"
