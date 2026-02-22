# 🧠 Mental Health Companion Chatbot

An AI-powered mental health companion that combines mood detection through text and image analysis with intelligent responses powered by Google's Gemini API.

## 🌟 Features

### 🎭 Mood Detection
- **Text Analysis**: Advanced NLP using TextBlob, VADER, and BERT transformers
- **Image Analysis**: Facial emotion detection using OpenCV and DeepFace
- **Combined Analysis**: Intelligent fusion of text and image inputs

### 🤖 Intelligent Responses
- **Gemini API Integration**: Personalized coping strategies and empathetic responses
- **Fallback System**: Built-in responses when API is unavailable
- **Context-Aware**: Responses tailored to detected emotions and user input
- **Dynamic Responses**: Multiple response variations for each emotion

### 👤 User Management
- **Secure Authentication**: Registration and login system
- **Anonymous Mode**: Privacy-focused anonymous sessions
- **Profile Management**: Personal data storage and preferences
- **Local Storage**: Data persistence using localStorage

### 📊 Mood Tracking
- **History Visualization**: Charts and graphs showing mood trends
- **Sentiment Analysis**: Detailed emotional insights
- **Progress Tracking**: Monitor mental health over time
- **Statistics Dashboard**: Mood counts and analytics

### 🛠️ Quick Tools
- **Breathing Exercises**: Guided relaxation techniques
- **Gratitude Journal**: Daily positive practices
- **Mood Check-ins**: Quick emotional state tracking
- **Positive Affirmations**: Motivational messages

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Quick Start

1. **Start Backend Server** (for AI features):
   ```bash
   cd c:/Users/gayatri/OneDrive/Desktop/AI
   python server.py
   ```

2. **Start Frontend Server**:
   ```bash
   cd c:/Users/gayatri/OneDrive/Desktop/AI
   python -m http.server 8080
   ```

3. **Open Application**:
   - **Frontend**: http://localhost:8080
   - **Backend API**: http://localhost:5000

### Dependencies

#### Core Libraries
```bash
pip install flask>=2.3.0
pip install flask-cors>=4.0.0
pip install textblob>=0.17.1
pip install vaderSentiment>=3.3.2
pip install transformers>=4.36.0
pip install torch>=2.6.0
```

#### Image Processing
```bash
pip install opencv-python>=4.8.0
pip install deepface>=0.0.79
pip install pillow>=10.0.0
```

#### API & Data
```bash
pip install google-generativeai>=0.3.2
pip install pandas>=2.1.0
pip install numpy>=1.24.0
pip install plotly>=5.17.0
pip install python-dotenv>=1.0.0
```

## 🎯 Usage Guide

### Getting Started

1. **Launch the Application**
   - Run both backend and frontend servers (see Quick Start)
   - Open browser to http://localhost:8080

2. **Create an Account or Use Anonymous Mode**
   - Register with username/email/password
   - Or use anonymous mode for privacy

3. **Start Chatting**
   - Type your feelings and thoughts
   - Optionally upload images for emotion detection
   - Receive personalized AI responses

### Main Features

#### 💬 Chat Companion
- **Real-time conversation** with AI companion
- **Automatic emotion detection** from text
- **Image-based emotion analysis** (optional)
- **Personalized coping strategies** for each emotion
- **Chat history** with timestamps

#### 📊 Mood Analysis
- **Text Analysis**: Detailed sentiment and emotion breakdown
- **Image Analysis**: Facial expression recognition
- **Combined Analysis**: Multi-modal emotion detection
- **Visual results** with emotion badges and confidence scores

#### 📈 Mood History
- **Visual mood trends** over time
- **Emotion distribution** charts
- **Sentiment score** tracking
- **Historical chat** and analysis records
- **Statistics dashboard** with mood counts

#### 🎯 Quick Tools
- **🧘 Breathing Exercises**: 4-7-8 technique guidance
- **📝 Gratitude Journal**: Daily positive practice with save functionality
- **🎯 Mood Tracker**: Quick emotional check-ins with sliders
- **🌈 Positive Affirmations**: Random motivational messages

## 🎨 Project Structure

```
c:/Users/gayatri/OneDrive/Desktop/AI/
├── index.html              # Main web interface
├── style.css               # Styling and animations
├── app.js                  # JavaScript functionality
├── server.py               # Flask backend API
├── config.py               # Configuration settings
├── database.py             # Database management
├── user_management.py       # User authentication
├── text_mood_detector.py   # Text-based emotion detection
├── image_mood_detector.py  # Image-based emotion detection
├── gemini_integration.py    # Gemini API integration
├── requirements.txt         # Python dependencies
└── README.md              # This documentation
```

## 🔧 Configuration

### Environment Setup
1. **Copy environment template**:
   ```bash
   copy .env.example .env
   ```

2. **Edit .env file**:
   ```bash
   GEMINI_API_KEY=your_gemini_api_key_here
   DATABASE_URL=sqlite:///mental_health_companion.db
   ```

### Gemini API Setup (Optional)

1. **Get API Key**
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create a new API key
   - Copy the key for configuration

2. **Configure Environment**
   ```bash
   # In your .env file
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## � Emotion Detection

### Supported Emotions
- 😊 Happy
- 😢 Sad
- 😠 Angry
- 😰 Stressed
- 😟 Anxious
- 😐 Neutral
- 😲 Surprised
- 😨 Fear

### Detection Methods

#### Text Analysis
- **VADER Sentiment**: Rule-based sentiment analysis
- **TextBlob**: Polarity and subjectivity scoring
- **BERT Transformers**: Deep learning emotion classification
- **Keyword Matching**: Emotion-specific word patterns

#### Image Analysis
- **DeepFace**: CNN-based facial emotion recognition
- **OpenCV**: Face detection and preprocessing
- **Confidence Scoring**: Reliability assessment
- **Multi-face Support**: Handles multiple faces in image

## 🛡️ Privacy & Security

### Data Protection
- **Anonymous Mode**: No personal data required
- **Local Storage**: All data stored locally in browser
- **No Cloud Dependencies**: Optional Gemini API only
- **Secure Authentication**: Password hashing with SHA-256

### Disclaimer
⚠️ **Important**: This chatbot is not a replacement for professional medical help. If you're experiencing severe mental health issues, please consult a qualified healthcare professional.

## 🎨 Frontend Features

### Modern Web Interface
- **Bootstrap 5**: Responsive design framework
- **Custom CSS**: Gradient headers, animations, transitions
- **Vanilla JavaScript**: No framework dependencies
- **Local Storage**: Client-side data persistence
- **Mobile Responsive**: Works on all devices

### Interactive Elements
- **Real-time Chat**: Message threading with timestamps
- **Dynamic Forms**: Validation and feedback
- **Progressive Enhancement**: Features load as needed
- **Smooth Animations**: CSS transitions and transforms

## 🔌 Backend API

### Flask Endpoints
- `GET /` - Serve main application
- `POST /api/analyze-text` - Text mood analysis
- `POST /api/analyze-image` - Image emotion detection
- `POST /api/chat` - Chat with AI responses
- `GET /api/mood-history` - Retrieve mood history
- `POST /api/save-mood` - Save mood entry
- `GET /api/health` - Health check

### API Features
- **CORS Enabled**: Cross-origin requests supported
- **JSON Responses**: Structured data format
- **Error Handling**: Comprehensive error responses
- **File Upload**: Multipart form data support

## 🌐 Deployment Options

### Local Development
- **Frontend**: Python HTTP server (port 8080)
- **Backend**: Flask development server (port 5000)
- **Database**: SQLite local database

### Production Deployment
- **Static Hosting**: Upload to GitHub Pages, Netlify, Vercel
- **Backend Hosting**: Heroku, PythonAnywhere, Railway
- **Database**: PostgreSQL/MySQL for production

## 🐛 Troubleshooting

### Common Issues

1. **Server Won't Start**
   - Check Python version (3.8+ required)
   - Install dependencies: `pip install -r requirements.txt`
   - Check port availability

2. **Images Not Analyzing**
   - Verify image format (JPG, PNG, WebP)
   - Check file size limit (5MB)
   - Ensure face is visible in image

3. **API Not Responding**
   - Verify Gemini API key in .env file
   - Check internet connection
   - Review server logs

4. **Database Issues**
   - Ensure write permissions in application directory
   - Delete `mental_health_companion.db` to reset
   - Check SQLite installation

### Performance Optimization

1. **Memory Usage**
   - Limit chat history size
   - Clear temporary image files
   - Restart application periodically

2. **Model Loading**
   - First-time usage may be slower (model downloads)
   - Subsequent uses will be faster

## 🤝 Contributing

### Development Setup
1. Install development dependencies
2. Create feature branches
3. Test thoroughly
4. Submit pull requests

### Enhancement Ideas
- Additional emotion categories
- Voice input support
- Integration with wearable devices
- Multi-language support
- Advanced analytics dashboard

## 📄 License

This project is for educational and personal use. Please ensure compliance with:
- Google Gemini API terms of service
- Open-source library licenses
- Healthcare application regulations in your region

## 📞 Support

For issues, questions, or suggestions:
1. Check the troubleshooting section
2. Review the documentation
3. Create an issue report with details

---

**Remember**: Your mental health matters. This tool is designed to support, not replace, professional healthcare. 🌈
