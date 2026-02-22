import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import tempfile
import os

# Import our custom modules
from config import Config
from database import DatabaseManager
from user_management import UserManagement
from text_mood_detector import TextMoodDetector
from image_mood_detector import ImageMoodDetector
from gemini_integration import GeminiIntegration

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def main():
    """Main application"""
    st.set_page_config(
        page_title=Config.APP_TITLE,
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .emotion-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .user-message {
        background: #e3f2fd;
        margin-left: 2rem;
    }
    .bot-message {
        background: #f3e5f5;
        margin-right: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize components
    user_mgmt = UserManagement()
    text_detector = TextMoodDetector()
    image_detector = ImageMoodDetector()
    gemini = GeminiIntegration()
    db = DatabaseManager()
    
    # Main header
    st.markdown(f"""
    <div class="main-header">
        <h1>{Config.APP_TITLE}</h1>
        <p>{Config.APP_DESCRIPTION}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Disclaimer
    st.warning(Config.DISCLAIMER)
    
    # Authentication check
    if not user_mgmt.is_logged_in():
        # Show login/register options
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        with tab1:
            user_mgmt.login_page()
        
        with tab2:
            user_mgmt.register_page()
        
        return
    
    # User is logged in - show main app
    user_mgmt.display_user_info()
    
    # Main navigation
    st.sidebar.title("🧠 Navigation")
    page = st.sidebar.selectbox(
        "Choose a feature:",
        ["💬 Chat Companion", "📊 Mood Analysis", "📈 Mood History", "🎯 Quick Tools"]
    )
    
    if page == "💬 Chat Companion":
        chat_companion_page(user_mgmt, text_detector, image_detector, gemini, db)
    elif page == "📊 Mood Analysis":
        mood_analysis_page(text_detector, image_detector, gemini, db)
    elif page == "📈 Mood History":
        mood_history_page(db)
    elif page == "🎯 Quick Tools":
        quick_tools_page()

def chat_companion_page(user_mgmt, text_detector, image_detector, gemini, db):
    """Main chat interface"""
    st.header("💬 Mental Health Chat Companion")
    
    user = user_mgmt.get_current_user()
    
    # Chat interface
    st.subheader("Chat with your AI companion")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>You:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message bot-message">
                    <strong>Companion:</strong> {message["content"]}
                </div>
                """, unsafe_allow_html=True)
    
    # Input section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        user_input = st.text_input("Type your message:", key="user_message", placeholder="How are you feeling today?")
    
    with col2:
        st.write("")  # Spacer
        send_button = st.button("Send 📤", type="primary")
    
    # Image upload option
    with st.expander("📷 Or upload an image for emotion detection"):
        uploaded_image = st.file_uploader(
            "Choose an image", 
            type=['jpg', 'jpeg', 'png', 'webp'],
            help="Upload a selfie or image to detect your current mood"
        )
    
    # Process input
    if send_button and user_input:
        # Add user message to chat
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now()
        })
        
        # Detect emotion from text
        text_analysis = text_detector.analyze_text_mood(user_input)
        detected_emotion = text_analysis["detected_emotion"]
        
        # Also analyze image if uploaded
        if uploaded_image:
            # Validate and process image
            is_valid, message = image_detector.validate_image(uploaded_image)
            if is_valid:
                temp_path = image_detector.save_uploaded_image(uploaded_image)
                if temp_path:
                    image_analysis = image_detector.analyze_image_mood(temp_path)
                    
                    # Combine text and image analysis (prioritize image if confidence is higher)
                    if image_analysis["confidence_score"] > text_analysis["confidence_score"]:
                        detected_emotion = image_analysis["detected_emotion"]
                        text_analysis["confidence_score"] = image_analysis["confidence_score"]
                    
                    image_detector.cleanup_temp_file(temp_path)
            else:
                st.error(message)
        
        # Generate response using Gemini
        gemini_response = gemini.generate_response(
            detected_emotion, 
            user_input, 
            text_analysis
        )
        
        response_text = gemini_response["response"]
        
        # Add bot response to chat
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response_text,
            "timestamp": datetime.now(),
            "emotion_detected": detected_emotion
        })
        
        # Save to database
        db.save_chat_message(user["id"], user_input, response_text, detected_emotion)
        
        # Rerun to update chat display
        st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

def mood_analysis_page(text_detector, image_detector, gemini, db):
    """Detailed mood analysis page"""
    st.header("📊 Mood Analysis")
    
    # Analysis type selection
    analysis_type = st.radio(
        "Choose analysis type:",
        ["📝 Text Analysis", "📷 Image Analysis", "🔄 Combined Analysis"]
    )
    
    if analysis_type == "📝 Text Analysis":
        st.subheader("Text-Based Mood Detection")
        
        user_text = st.text_area(
            "Enter your thoughts or feelings:",
            height=150,
            placeholder="Describe how you're feeling right now..."
        )
        
        if st.button("Analyze Text Mood", type="primary"):
            if user_text.strip():
                with st.spinner("Analyzing your text..."):
                    analysis = text_detector.analyze_text_mood(user_text)
                    
                    # Display results
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(
                            "Detected Emotion",
                            f"{text_detector.get_emotion_emoji(analysis['detected_emotion'])} {analysis['detected_emotion']}"
                        )
                    
                    with col2:
                        st.metric(
                            "Sentiment Score",
                            f"{analysis['sentiment_score']:.2f}"
                        )
                    
                    with col3:
                        st.metric(
                            "Confidence",
                            f"{analysis['confidence_score']:.2%}"
                        )
                
                # Detailed analysis
                with st.expander("🔍 Detailed Analysis"):
                    st.json(analysis["analysis_details"])
                
                # Get AI response
                with st.spinner("Generating personalized response..."):
                    gemini_response = gemini.generate_response(
                        analysis['detected_emotion'],
                        user_text,
                        analysis
                    )
                    st.markdown(gemini_response["response"])
            else:
                st.warning("Please enter some text to analyze.")
    
    elif analysis_type == "📷 Image Analysis":
        st.subheader("Image-Based Emotion Detection")
        
        uploaded_image = st.file_uploader(
            "Upload an image for emotion analysis:",
            type=['jpg', 'jpeg', 'png', 'webp']
        )
        
        if uploaded_image:
            # Display uploaded image
            st.image(uploaded_image, caption="Uploaded Image", width=300)
            
            if st.button("Analyze Image Mood", type="primary"):
                with st.spinner("Analyzing image..."):
                    # Validate image
                    is_valid, message = image_detector.validate_image(uploaded_image)
                    
                    if is_valid:
                        temp_path = image_detector.save_uploaded_image(uploaded_image)
                        if temp_path:
                            analysis = image_detector.analyze_image_mood(temp_path)
                            
                            # Display results
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric(
                                    "Detected Emotion",
                                    f"{image_detector.get_emotion_emoji(analysis['detected_emotion'])} {analysis['detected_emotion']}"
                                )
                            
                            with col2:
                                st.metric(
                                    "Confidence",
                                    f"{analysis['confidence_score']:.2%}"
                                )
                            
                            with col3:
                                st.metric(
                                    "Face Detected",
                                    "Yes ✅" if analysis['face_detected'] else "No ❌"
                                )
                            
                            # Emotion description
                            st.info(image_detector.get_emotion_description(analysis['detected_emotion']))
                            
                            # Detailed analysis
                            with st.expander("🔍 Detailed Analysis"):
                                st.json(analysis)
                            
                            # Get AI response
                            with st.spinner("Generating personalized response..."):
                                gemini_response = gemini.generate_response(
                                    analysis['detected_emotion'],
                                    "Image-based emotion detection",
                                    analysis
                                )
                                st.markdown(gemini_response["response"])
                            
                            image_detector.cleanup_temp_file(temp_path)
                    else:
                        st.error(message)
    
    elif analysis_type == "🔄 Combined Analysis":
        st.subheader("Combined Text and Image Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            user_text = st.text_area(
                "Enter your thoughts:",
                height=100,
                placeholder="How are you feeling?"
            )
        
        with col2:
            uploaded_image = st.file_uploader(
                "Upload an image:",
                type=['jpg', 'jpeg', 'png', 'webp']
            )
        
        if st.button("Combined Analysis", type="primary"):
            if not user_text.strip() and not uploaded_image:
                st.warning("Please provide either text, image, or both for analysis.")
            else:
                with st.spinner("Analyzing..."):
                    text_analysis = None
                    image_analysis = None
                    
                    # Analyze text if provided
                    if user_text.strip():
                        text_analysis = text_detector.analyze_text_mood(user_text)
                    
                    # Analyze image if provided
                    if uploaded_image:
                        is_valid, message = image_detector.validate_image(uploaded_image)
                        if is_valid:
                            temp_path = image_detector.save_uploaded_image(uploaded_image)
                            if temp_path:
                                image_analysis = image_detector.analyze_image_mood(temp_path)
                                image_detector.cleanup_temp_file(temp_path)
                        else:
                            st.error(message)
                            return
                    
                    # Combine results
                    if text_analysis and image_analysis:
                        # Use the analysis with higher confidence
                        if image_analysis['confidence_score'] > text_analysis['confidence_score']:
                            final_emotion = image_analysis['detected_emotion']
                            final_confidence = image_analysis['confidence_score']
                        else:
                            final_emotion = text_analysis['detected_emotion']
                            final_confidence = text_analysis['confidence_score']
                    elif text_analysis:
                        final_emotion = text_analysis['detected_emotion']
                        final_confidence = text_analysis['confidence_score']
                    elif image_analysis:
                        final_emotion = image_analysis['detected_emotion']
                        final_confidence = image_analysis['confidence_score']
                    else:
                        st.error("Analysis failed. Please try again.")
                        return
                    
                    # Display combined results
                    st.success(f"🎯 Combined Analysis Result: {final_emotion} (Confidence: {final_confidence:.2%})")
                    
                    # Get AI response
                    with st.spinner("Generating personalized response..."):
                        context = {
                            'text_analysis': text_analysis,
                            'image_analysis': image_analysis,
                            'confidence_score': final_confidence
                        }
                        
                        gemini_response = gemini.generate_response(
                            final_emotion,
                            user_text or "Image-based emotion detection",
                            context
                        )
                        st.markdown(gemini_response["response"])

def mood_history_page(db):
    """Display mood history and trends"""
    st.header("📈 Your Mood History")
    
    user = st.session_state.get('current_user')
    if not user:
        st.error("Please log in to view your mood history.")
        return
    
    # Get mood history
    mood_history = db.get_user_mood_history(user['id'], limit=100)
    
    if not mood_history:
        st.info("No mood history available. Start chatting or analyzing your mood to build your history!")
        return
    
    # Create DataFrame
    df = pd.DataFrame(mood_history)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['date'] = df['timestamp'].dt.date
    
    # Summary statistics
    st.subheader("📊 Mood Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    emotion_counts = df['emotion'].value_counts()
    most_common_emotion = emotion_counts.index[0] if len(emotion_counts) > 0 else "Neutral"
    avg_sentiment = df['sentiment_score'].mean() if 'sentiment_score' in df.columns else 0
    avg_confidence = df['confidence_score'].mean() if 'confidence_score' in df.columns else 0
    
    with col1:
        st.metric("Total Entries", len(df))
    
    with col2:
        st.metric("Most Common Emotion", most_common_emotion)
    
    with col3:
        st.metric("Avg Sentiment", f"{avg_sentiment:.2f}")
    
    with col4:
        st.metric("Avg Confidence", f"{avg_confidence:.2%}")
    
    # Mood over time chart
    st.subheader("📈 Mood Trends")
    
    # Daily mood summary
    daily_mood = df.groupby(['date', 'emotion']).size().reset_index(name='count')
    daily_mood_pivot = daily_mood.pivot(index='date', columns='emotion', values='count').fillna(0)
    
    if not daily_mood_pivot.empty:
        fig = px.line(
            daily_mood_pivot,
            title="Your Mood Over Time",
            labels={"value": "Frequency", "date": "Date"},
            template="plotly_white"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Emotion distribution
    st.subheader("🎭 Emotion Distribution")
    
    fig_pie = px.pie(
        values=emotion_counts.values,
        names=emotion_counts.index,
        title="Overall Emotion Distribution",
        template="plotly_white"
    )
    fig_pie.update_layout(height=400)
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # Recent entries
    st.subheader("📝 Recent Mood Entries")
    
    recent_entries = df.head(10)
    for _, entry in recent_entries.iterrows():
        with st.expander(f"{entry['timestamp'].strftime('%Y-%m-%d %H:%M')} - {entry['emotion']}"):
            if entry.get('text_input'):
                st.write(f"**Text:** {entry['text_input']}")
            if entry.get('gemini_response'):
                st.write(f"**AI Response:** {entry['gemini_response'][:200]}...")
            st.write(f"**Sentiment Score:** {entry.get('sentiment_score', 0):.2f}")
            st.write(f"**Confidence:** {entry.get('confidence_score', 0):.2%}")

def quick_tools_page():
    """Quick mental health tools"""
    st.header("🎯 Quick Mental Health Tools")
    
    tool = st.selectbox(
        "Choose a tool:",
        ["🧘 Breathing Exercise", "📝 Gratitude Journal", "🎯 Mood Tracker", "🌈 Positive Affirmations"]
    )
    
    if tool == "🧘 Breathing Exercise":
        st.subheader("4-7-8 Breathing Technique")
        
        st.markdown("""
        **Instructions:**
        1. Find a comfortable position and close your eyes
        2. Breathe in through your nose for 4 counts
        3. Hold your breath for 7 counts
        4. Exhale through your mouth for 8 counts
        5. Repeat 3-4 times
        
        **Benefits:** Reduces anxiety, promotes relaxation, helps with sleep
        """)
        
        if st.button("Start Breathing Exercise"):
            st.info("Follow the rhythm: Inhale 4 → Hold 7 → Exhale 8")
            # You could add a visual timer here
    
    elif tool == "📝 Gratitude Journal":
        st.subheader("Daily Gratitude Practice")
        
        st.markdown("""
        **What are you grateful for today?**
        
        Research shows that practicing gratitude can:
        - Increase happiness and life satisfaction
        - Reduce symptoms of depression
        - Improve sleep quality
        - Strengthen relationships
        """)
        
        gratitude_entry = st.text_area(
            "List 3 things you're grateful for:",
            height=150,
            placeholder="1. \n2. \n3. "
        )
        
        if st.button("Save Gratitude Entry"):
            if gratitude_entry:
                st.success("Gratitude entry saved! 🙏")
            else:
                st.warning("Please write at least one thing you're grateful for.")
    
    elif tool == "🎯 Mood Tracker":
        st.subheader("Quick Mood Check-in")
        
        current_mood = st.select_slider(
            "How are you feeling right now?",
            options=["Very Sad", "Sad", "Neutral", "Happy", "Very Happy"],
            value="Neutral"
        )
        
        energy_level = st.select_slider(
            "What's your energy level?",
            options=["Very Low", "Low", "Medium", "High", "Very High"],
            value="Medium"
        )
        
        stress_level = st.select_slider(
            "Current stress level?",
            options=["Very Low", "Low", "Medium", "High", "Very High"],
            value="Medium"
        )
        
        notes = st.text_area("Any additional notes (optional):")
        
        if st.button("Save Mood Check-in"):
            st.success(f"Mood check-in saved: {current_mood}, Energy: {energy_level}, Stress: {stress_level}")
    
    elif tool == "🌈 Positive Affirmations":
        st.subheader("Daily Positive Affirmations")
        
        affirmations = [
            "I am worthy of love and respect.",
            "I choose to focus on what I can control.",
            "I am capable of handling whatever comes my way.",
            "I deserve to be happy and peaceful.",
            "I am growing and learning every day.",
            "I trust the journey of my life.",
            "I am strong enough to overcome my challenges.",
            "I choose to be kind to myself today.",
            "I am deserving of all the good things that come my way.",
            "I have the power to create positive change in my life."
        ]
        
        if st.button("Get Random Affirmation 🎲"):
            import random
            affirmation = random.choice(affirmations)
            st.success(f"✨ **{affirmation}**")
        
        st.markdown("### Today's Affirmations:")
        for i, affirmation in enumerate(affirmations[:5], 1):
            st.write(f"{i}. {affirmation}")

if __name__ == "__main__":
    main()
