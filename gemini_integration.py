import google.generativeai as genai
import json
from typing import Dict, List, Optional
from config import Config

class GeminiIntegration:
    def __init__(self, api_key: str = None):
        """Initialize Gemini API integration"""
        self.api_key = api_key or Config.GEMINI_API_KEY
        
        if self.api_key and self.api_key != "your_gemini_api_key_here":
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.is_configured = True
        else:
            self.model = None
            self.is_configured = False
    
    def create_emotion_prompt(self, emotion: str, user_message: str, 
                            context: Optional[Dict] = None) -> str:
        """Create structured prompt for Gemini API"""
        
        base_prompt = f"""
You are a compassionate and empathetic mental health companion AI. The user's current emotional state has been detected as: {emotion}

User's message: "{user_message}"

Please provide a response that includes:

1. **Empathetic Response**: A warm, understanding acknowledgment of their feelings
2. **3 Practical Coping Strategies**: Specific, actionable techniques they can use right now
3. **Motivational Message**: An encouraging and uplifting thought
4. **Situation-based Solution**: Tailored advice based on their specific situation

Guidelines:
- Be warm, compassionate, and non-judgmental
- Keep responses concise but comprehensive (around 200-300 words total)
- Focus on practical, evidence-based coping techniques
- Include breathing exercises, mindfulness, or cognitive reframing when appropriate
- Always include a disclaimer that this is not professional medical advice
- If the emotion is severe or concerning, suggest seeking professional help

Format your response with clear sections using markdown formatting.
"""
        
        # Add context if available
        if context:
            context_info = ""
            if 'sentiment_score' in context:
                sentiment = "positive" if context['sentiment_score'] > 0 else "negative" if context['sentiment_score'] < 0 else "neutral"
                context_info += f"\nSentiment analysis indicates {sentiment} sentiment (score: {context['sentiment_score']:.2f})"
            
            if 'confidence_score' in context:
                context_info += f"\nConfidence in emotion detection: {context['confidence_score']:.2f}"
            
            if context_info:
                base_prompt += f"\n\nAdditional Context:{context_info}"
        
        return base_prompt
    
    def generate_response(self, emotion: str, user_message: str, 
                         context: Optional[Dict] = None) -> Dict[str, str]:
        """Generate intelligent response using Gemini API"""
        
        if not self.is_configured:
            return self._get_fallback_response(emotion, user_message)
        
        try:
            prompt = self.create_emotion_prompt(emotion, user_message, context)
            
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                return {
                    "status": "success",
                    "response": response.text,
                    "source": "gemini_api"
                }
            else:
                return self._get_fallback_response(emotion, user_message)
                
        except Exception as e:
            print(f"Error generating Gemini response: {e}")
            return self._get_fallback_response(emotion, user_message)
    
    def _get_fallback_response(self, emotion: str, user_message: str) -> Dict[str, str]:
        """Get fallback response when Gemini API is not available"""
        
        fallback_responses = {
            "Happy": {
                "response": """### 🌟 Empathetic Response

It's wonderful to see you feeling happy! Your positive energy is contagious and it's great that you're embracing these joyful moments.

### 💡 3 Practical Coping Strategies

1. **Gratitude Journaling**: Write down 3 things you're grateful for right now to amplify your positive feelings
2. **Share Your Joy**: Reach out to a friend or family member and share what's making you happy
3. **Mindful Appreciation**: Take 2 minutes to fully savor this happy moment, noticing all the positive sensations

### 🌈 Motivational Message

"Joy is a net of love by which you can catch souls." - Mother Teresa. Your happiness has the power to uplift others around you.

### 🎯 Situation-based Solution

Since you're feeling good, this is a perfect time to:
- Set positive intentions for the week ahead
- Plan activities that maintain this positive momentum
- Reflect on what contributed to this happiness so you can recreate it

*Note: This is an AI-generated response. For professional mental health support, please consult a qualified healthcare provider.*""",
                "source": "fallback"
            },
            
            "Sad": {
                "response": """### 🤗 Empathetic Response

I hear that you're feeling sad right now, and I want you to know that it's completely okay to feel this way. Sadness is a natural human emotion, and allowing yourself to feel it is a sign of emotional strength.

### 💡 3 Practical Coping Strategies

1. **Gentle Breathing**: Try the 4-7-8 technique - breathe in for 4 counts, hold for 7, exhale for 8. Repeat 3-4 times
2. **Self-Compassion Break**: Place a hand over your heart and say: "This is a moment of suffering. Everyone feels sad sometimes. May I be kind to myself."
3. **Gentle Movement**: Take a slow 5-minute walk or do some gentle stretching to help process emotions physically

### 🌈 Motivational Message

"Every cloud has a silver lining, and every dark night has a dawn." This feeling is temporary, and you have the strength to move through it.

### 🎯 Situation-based Solution

When feeling sad, it's helpful to:
- Allow yourself to feel without judgment
- Connect with someone you trust
- Engage in a comforting activity (warm bath, favorite music, comforting food)

*Note: This is an AI-generated response. For professional mental health support, please consult a qualified healthcare provider.*""",
                "source": "fallback"
            },
            
            "Angry": {
                "response": """### 😌 Empathetic Response

I can see you're feeling angry right now. Anger is a powerful emotion that often signals that something important to you has been violated or that your boundaries have been crossed.

### 💡 3 Practical Coping Strategies

1. **Cooling Breath**: Practice "box breathing" - inhale for 4 counts, hold for 4, exhale for 4, hold for 4. Repeat 5 times
2. **Progressive Muscle Relaxation**: Start from your toes, tense each muscle group for 5 seconds, then release. Work your way up to your head
3. **Thought Reframing**: Ask yourself: "Will this matter in 5 hours? 5 days? 5 years?" This helps put things in perspective

### 🌈 Motivational Message

"Holding onto anger is like grasping a hot coal with the intent of throwing it at someone else; you are the one who gets burned." - Buddha

### 🎯 Situation-based Solution

To manage anger effectively:
- Step away from the situation temporarily
- Use "I" statements to express your feelings
- Channel the energy into physical activity or creative expression

*Note: This is an AI-generated response. For professional mental health support, please consult a qualified healthcare provider.*""",
                "source": "fallback"
            },
            
            "Stressed": {
                "response": """### 🧘 Empathetic Response

I can sense that you're feeling stressed right now. Stress can feel overwhelming, but remember that you have the capacity to handle whatever comes your way. You're stronger than you think.

### 💡 3 Practical Coping Strategies

1. **5-4-3-2-1 Grounding**: Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste
2. **Prioritization Matrix**: Write down your stressors, categorize them as urgent/important, and tackle them one by one
3. **Mini Meditation**: Set a timer for 3 minutes, close your eyes, and focus only on your breath

### 🌈 Motivational Message

"You don't have to control your thoughts. You just have to stop letting them control you." This moment of stress will pass.

### 🎯 Situation-based Solution

When feeling stressed:
- Break large tasks into smaller, manageable steps
- Take regular breaks to prevent burnout
- Practice saying "no" to non-essential commitments

*Note: This is an AI-generated response. For professional mental health support, please consult a qualified healthcare provider.*""",
                "source": "fallback"
            },
            
            "Anxious": {
                "response": """### 🌸 Empathetic Response

I notice you're feeling anxious right now. Anxiety can be uncomfortable, but please know that you're not alone in this experience. These feelings, while distressing, are manageable and will pass.

### 💡 3 Practical Coping Strategies

1. **Diaphragmatic Breathing**: Place one hand on your chest, one on your belly. Breathe so your belly hand rises more than your chest hand
2. **Reality Testing**: Ask yourself: "What's the evidence for/against this worry? What's a more balanced perspective?"
3. **Safe Space Visualization**: Close your eyes and imagine a place where you feel completely calm and safe. Engage all your senses

### 🌈 Motivational Message

"Anxiety doesn't empty tomorrow of its sorrows, but only empties today of its strength." You have survived 100% of your worst days.

### 🎯 Situation-based Solution

For anxiety management:
- Focus on what you can control, accept what you cannot
- Use the "worry time" technique - schedule 15 minutes daily to worry, then move on
- Practice progressive exposure to anxiety-provoking situations

*Note: This is an AI-generated response. For professional mental health support, please consult a qualified healthcare provider.*""",
                "source": "fallback"
            },
            
            "Neutral": {
                "response": """### 😊 Empathetic Response

I see you're in a neutral state right now. This balanced emotional state can be a wonderful foundation for mindfulness and self-reflection.

### 💡 3 Practical Coping Strategies

1. **Mindful Check-in**: Take a moment to scan your body and notice any sensations without judgment
2. **Gratitude Practice**: List 5 things you're grateful for, no matter how small
3. **Future Visualization**: Imagine your ideal self in 6 months and what steps you could take toward that vision

### 🌈 Motivational Message

"The present moment is the only time over which we have dominion." Your neutral state is perfect for conscious choice and intentional living.

### 🎯 Situation-based Solution

Use this balanced state to:
- Set meaningful goals for the coming week
- Practice self-reflection and personal growth
- Build healthy habits and routines

*Note: This is an AI-generated response. For professional mental health support, please consult a qualified healthcare provider.*""",
                "source": "fallback"
            }
        }
        
        return fallback_responses.get(emotion, {
            "response": """### 🤗 Empathetic Response

I'm here to support you through whatever you're experiencing. Your feelings are valid, and it's brave of you to reach out.

### 💡 3 Practical Coping Strategies

1. **Deep Breathing**: Take 5 slow, deep breaths, focusing on the exhale
2. **Self-Compassion**: Treat yourself with the same kindness you'd offer a friend
3. **Present Moment**: Focus on what you can see, hear, and feel right now

### 🌈 Motivational Message

"This too shall pass." Every emotion is temporary, and you have the strength to navigate through this.

### 🎯 Situation-based Solution

Take things one moment at a time, be gentle with yourself, and remember that seeking support is a sign of strength.

*Note: This is an AI-generated response. For professional mental health support, please consult a qualified healthcare provider.*""",
            "source": "fallback"
        })
    
    def is_api_available(self) -> bool:
        """Check if Gemini API is properly configured"""
        return self.is_configured
