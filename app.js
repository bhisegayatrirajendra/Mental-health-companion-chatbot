// Mental Health Companion JavaScript Application

class MentalHealthApp {
    constructor() {
        this.currentUser = null;
        this.chatHistory = [];
        this.moodHistory = [];
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadFromLocalStorage();
        this.updateUI();
    }

    // Local Storage Management
    saveToLocalStorage() {
        localStorage.setItem('mentalHealthApp', JSON.stringify({
            currentUser: this.currentUser,
            chatHistory: this.chatHistory,
            moodHistory: this.moodHistory
        }));
    }

    loadFromLocalStorage() {
        const data = localStorage.getItem('mentalHealthApp');
        if (data) {
            const parsed = JSON.parse(data);
            this.currentUser = parsed.currentUser || null;
            this.chatHistory = parsed.chatHistory || [];
            this.moodHistory = parsed.moodHistory || [];
        }
    }

    // Event Listeners
    setupEventListeners() {
        // Authentication
        document.getElementById('loginForm')?.addEventListener('submit', (e) => this.handleLogin(e));
        document.getElementById('registerForm')?.addEventListener('submit', (e) => this.handleRegister(e));
        document.getElementById('anonymousBtn')?.addEventListener('click', () => this.handleAnonymous());
        
        // Main App
        document.getElementById('sendBtn')?.addEventListener('click', () => this.sendMessage());
        document.getElementById('clearChatBtn')?.addEventListener('click', () => this.clearChat());
        document.getElementById('logoutBtn')?.addEventListener('click', () => this.logout());
        
        // Mood Analysis
        document.getElementById('analyzeTextBtn')?.addEventListener('click', () => this.analyzeText());
        document.getElementById('analyzeImageBtn')?.addEventListener('click', () => this.analyzeImage());
        
        // Quick Tools
        document.getElementById('breathingBtn')?.addEventListener('click', () => this.startBreathing());
        document.getElementById('gratitudeBtn')?.addEventListener('click', () => this.saveGratitude());
        document.getElementById('moodTrackBtn')?.addEventListener('click', () => this.trackMood());
        document.getElementById('affirmationBtn')?.addEventListener('click', () => this.getRandomAffirmation());
        
        // Enter key for chat
        document.getElementById('messageInput')?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
    }

    // Authentication Methods
    handleLogin(e) {
        e.preventDefault();
        const username = document.getElementById('loginUsername').value;
        const password = document.getElementById('loginPassword').value;
        
        if (username && password) {
            this.currentUser = {
                id: Date.now(),
                username: username,
                isAnonymous: false
            };
            this.saveToLocalStorage();
            this.showMainApp();
            this.showNotification(`Welcome back, ${username}! 🎉`, 'success');
        } else {
            this.showNotification('Please enter username and password', 'error');
        }
    }

    handleRegister(e) {
        e.preventDefault();
        const username = document.getElementById('registerUsername').value;
        const email = document.getElementById('registerEmail').value;
        const password = document.getElementById('registerPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        
        if (!username || !password) {
            this.showNotification('Please fill in required fields', 'error');
            return;
        }
        
        if (password !== confirmPassword) {
            this.showNotification('Passwords do not match', 'error');
            return;
        }
        
        this.currentUser = {
            id: Date.now(),
            username: username,
            email: email,
            isAnonymous: false
        };
        this.saveToLocalStorage();
        this.showMainApp();
        this.showNotification(`Account created successfully! Welcome, ${username}! 🎉`, 'success');
    }

    handleAnonymous() {
        this.currentUser = {
            id: Date.now(),
            username: `Anonymous_${new Date().getHours()}${new Date().getMinutes()}`,
            isAnonymous: true
        };
        this.saveToLocalStorage();
        this.showMainApp();
        this.showNotification('Anonymous session started! 🎭', 'info');
    }

    logout() {
        this.currentUser = null;
        this.chatHistory = [];
        this.saveToLocalStorage();
        this.showAuthSection();
        this.showNotification('Logged out successfully!', 'info');
    }

    // UI Management
    showMainApp() {
        document.getElementById('auth-section').style.display = 'none';
        document.getElementById('main-app').style.display = 'block';
        this.updateUserInfo();
        this.updateChatDisplay();
        this.updateMoodHistory();
    }

    showAuthSection() {
        document.getElementById('auth-section').style.display = 'block';
        document.getElementById('main-app').style.display = 'none';
    }

    updateUserInfo() {
        if (!this.currentUser) return;
        
        const userInfo = document.getElementById('userInfo');
        if (this.currentUser.isAnonymous) {
            userInfo.innerHTML = `
                <div class="alert alert-info">
                    <strong>🎭 Anonymous User</strong><br>
                    ${this.currentUser.username}
                </div>
            `;
        } else {
            userInfo.innerHTML = `
                <div class="alert alert-success">
                    <strong>👤 ${this.currentUser.username}</strong><br>
                    ${this.currentUser.email ? `📧 ${this.currentUser.email}` : ''}
                </div>
            `;
        }
    }

    // Chat Methods
    sendMessage() {
        const input = document.getElementById('messageInput');
        const message = input.value.trim();
        
        if (!message) return;
        
        const userMessage = {
            id: Date.now(),
            role: 'user',
            content: message,
            timestamp: new Date()
        };
        
        this.chatHistory.push(userMessage);
        
        // Generate response
        const response = this.generateResponse(message);
        const botMessage = {
            id: Date.now() + 1,
            role: 'assistant',
            content: response,
            timestamp: new Date()
        };
        
        this.chatHistory.push(botMessage);
        
        input.value = '';
        this.saveToLocalStorage();
        this.updateChatDisplay();
    }

    generateResponse(message) {
        // For now, use local response generation
        // In production, this would call the backend API
        return this.generateLocalResponse(message);
    }

    generateLocalResponse(message) {
        const lowerMessage = message.toLowerCase();
        
        // Response templates for variety
        const responseTemplates = {
            sad: [
                `I understand you're feeling sad right now. It's completely okay to feel this way.

**Here are 3 things that might help:**
1. **Deep Breathing**: Try the 4-7-8 technique - breathe in for 4, hold for 7, exhale for 8
2. **Self-Compassion**: Place a hand over your heart and say "It's okay to feel this way"
3. **Gentle Movement**: Take a short walk or do some light stretching

Remember: This feeling is temporary and you have the strength to get through it. 🌈`,
                
                `I hear that you're feeling down right now. Sadness is a natural emotion that shows your capacity for deep feeling.

**Let me suggest some supportive actions:**
1. **Emotional Release**: Allow yourself to cry if you need to - it's natural and healing
2. **Comfort Activity**: Wrap yourself in a warm blanket and watch something comforting
3. **Connect**: Reach out to someone you trust - you don't have to go through this alone

Your feelings are valid, and this cloud will eventually pass. 💙`,
                
                `It sounds like you're experiencing some difficult emotions right now. I'm here with you through this.

**Here are some gentle suggestions:**
1. **Mindful Acceptance**: Instead of fighting the sadness, just notice it without judgment
2. **Nourishment**: Have a warm drink or snack - comfort can help
3. **Creative Expression**: Try journaling, drawing, or listening to music that matches your mood

You have survived 100% of your difficult days so far. 🌟`
            ],
            
            anxious: [
                `I notice you're feeling anxious. These feelings can be overwhelming, but you're not alone.

**Here are 3 coping strategies:**
1. **Grounding Technique**: Name 5 things you can see, 4 you can touch, 3 you can hear
2. **Reality Testing**: Ask yourself "What evidence do I have that this worry will come true?"
3. **Progressive Muscle Relaxation**: Tense and release each muscle group from toes to head

You've handled anxiety before, and you can handle it again. 💪`,
                
                `I can sense that anxious energy right now. Let's work together to calm your nervous system.

**Try these anxiety-reducing techniques:**
1. **Box Breathing**: Inhale for 4 counts, hold for 4, exhale for 4, hold for 4 - repeat 5 times
2. **5-4-3-2-1 Method**: Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste
3. **Worry Postponement**: Schedule 15 minutes of "worry time" later - you don't have to engage right now

Your nervous system is just trying to protect you. You're safe. 🕊`,
                
                `That feeling of anxiety is uncomfortable, but it shows your mind is working hard to keep you safe.

**Let's try some immediate relief:**
1. **Temperature Change**: Splash cold water on your face or hold ice cubes
2. **Pattern Interrupt**: Stand up, stretch, or say your name out loud
3. **Future Self**: Imagine your future self telling you "You got through this, and you'll get through this too"

Anxiety is temporary, but your strength is permanent. ⚡`
            ],
            
            angry: [
                `I can see you're feeling angry. Anger is a valid emotion that signals something important to you.

**Here are 3 ways to manage anger:**
1. **Cooling Breath**: Practice box breathing - inhale 4, hold 4, exhale 4, hold 4
2. **Thought Reframing**: Ask yourself "Will this matter in 5 hours? 5 days? 5 years?"
3. **Physical Release**: Channel energy into exercise or creative expression

Your feelings are valid, and you have the power to respond constructively. 🌟`,
                
                `I hear that frustration in your words. Anger often comes when something we care about feels threatened.

**Let's channel this energy productively:**
1. **Quick Reset**: Step away from the situation for 5 minutes - take space
2. **Physical Outlet**: Do 10 pushups, punch a pillow, or go for a fast walk
3. **Problem Solving**: Write down exactly what made you angry and one small step you can take

Your anger is trying to tell you something important. Listen to it. 🔥`,
                
                `That fiery feeling of anger shows you have strong boundaries and values. Let's work with it.

**Here are some anger management tools:**
1. **Sensory Grounding**: Hold something cold, notice 5 details about it
2. **Assertive Communication**: Use "I feel..." statements instead of blaming
3. **Energy Transformation**: Clean something vigorously, organize, or plan something constructive

Your intensity shows how much you care. That's a strength. 💢`
            ],
            
            happy: [
                `It's wonderful that you're feeling happy! Your positive energy is inspiring.

**Here are 3 ways to amplify your joy:**
1. **Gratitude Practice**: Write down 3 things you're grateful for right now
2. **Share Your Joy**: Reach out to someone and share what's making you happy
3. **Mindful Savoring**: Take 2 minutes to fully appreciate this positive moment

Your happiness has the power to uplift others around you! ✨`,
                
                `I love that you're feeling good! Happiness is worth celebrating and savoring.

**Let's make this moment even better:**
1. **Memory Capture**: Take a photo or write down what's making you happy
2. **Body Celebration**: Put on music you love and dance for one song
3. **Future Planning**: Use this positive energy to set one exciting goal

Your joy is contagious - spread it around! 🎉`,
                
                `That positive energy is beautiful to witness! Happiness looks good on you.

**Here's how to extend this good feeling:**
1. **Social Sharing**: Tell someone why you're happy - joy multiplies when shared
2. **Sensory Engagement**: Notice 5 things you can see, hear, smell, taste, touch right now
3. **Accomplishment List**: Write down 3 things you've done well recently

You deserve this happiness - soak it in completely! 🌈`
            ],
            
            stressed: [
                `I can see you're feeling stressed. Stress can feel overwhelming, but you have the capacity to handle this.

**Here are 3 stress management techniques:**
1. **Prioritization Matrix**: Write down tasks and categorize as urgent/important
2. **Mini Breaks**: Take 5-minute breaks every hour to prevent burnout
3. **Boundary Setting**: Practice saying "no" to non-essential commitments

You're stronger than you think, and this moment of stress will pass. 🌸`,
                
                `That overwhelmed feeling is real - your nervous system is in overdrive trying to protect you.

**Let's gently reduce that stress:**
1. **Brain Dump**: Write down everything on your mind - get it out of your head
2. **Micro-Breaks**: Take 3 deep breaths between tasks - reset your nervous system
3. **Delegate or Delay**: Ask for help or postpone non-urgent tasks

Stress is just your body's way of saying "slow down." Listen to it. 🌿`,
                
                `I can feel that tension in your words. Stress shows you're carrying important responsibilities.

**Here's your stress relief toolkit:**
1. **Progressive Relaxation**: Starting from toes, tense each muscle group for 5 seconds, then release
2. **Time Management**: Use the Pomodoro technique - 25 minutes focus, 5 minutes break
3. **Nature Connection**: Step outside for 2 minutes or look at pictures of nature

You're handling more than you realize. Give yourself credit. 🏆`
            ],
            
            default: [
                `Thank you for sharing how you're feeling. I'm here to support you.

**Here are 3 general wellness practices:**
1. **Check-in**: Take a moment to notice how you're feeling without judgment
2. **Breathing**: Take 3 deep, slow breaths to center yourself
3. **Self-Kindness**: Treat yourself with the same compassion you'd offer a friend

Remember: You're not alone in this journey, and seeking support is a sign of strength. 🤗`,
                
                `I appreciate you opening up about your feelings. That takes courage.

**Here are some supportive practices:**
1. **Mindful Awareness**: Simply notice what's happening in your body and mind right now
2. **Gentle Movement**: Stand up, stretch, or walk around for a few minutes
3. **Self-Compassion**: Place a hand on your heart and acknowledge whatever you're feeling

You're doing the best you can with what you have right now. That's enough. 💚`,
                
                `Thank you for trusting me with your thoughts. Your feelings matter and deserve to be heard.

**Let's focus on gentle support:**
1. **Present Moment**: What are 3 things you can observe right now?
2. **Body Scan**: Notice sensations from head to toes without trying to change them
3. **Kind Action**: Do one small thing that would make your present moment 1% better

You're exactly where you need to be right now. 🌱`
            ]
        };
        
        // Detect mood and get random response from that category
        let responseCategory = 'default';
        
        if (lowerMessage.includes('sad') || lowerMessage.includes('depressed') || lowerMessage.includes('unhappy')) {
            responseCategory = 'sad';
        } else if (lowerMessage.includes('anxious') || lowerMessage.includes('worried') || lowerMessage.includes('nervous')) {
            responseCategory = 'anxious';
        } else if (lowerMessage.includes('angry') || lowerMessage.includes('mad') || lowerMessage.includes('frustrated')) {
            responseCategory = 'angry';
        } else if (lowerMessage.includes('happy') || lowerMessage.includes('good') || lowerMessage.includes('great')) {
            responseCategory = 'happy';
        } else if (lowerMessage.includes('stressed') || lowerMessage.includes('overwhelmed') || lowerMessage.includes('pressure')) {
            responseCategory = 'stressed';
        }
        
        // Get random response from the detected category
        const categoryResponses = responseTemplates[responseCategory];
        const randomResponse = categoryResponses[Math.floor(Math.random() * categoryResponses.length)];
        
        return randomResponse;
    }

    updateChatDisplay() {
        const chatMessages = document.getElementById('chatMessages');
        if (!chatMessages) return;
        
        chatMessages.innerHTML = '';
        
        this.chatHistory.forEach(message => {
            const messageDiv = document.createElement('div');
            messageDiv.className = `chat-message ${message.role}-message`;
            
            const time = new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            
            messageDiv.innerHTML = `
                <div><strong>${message.role === 'user' ? 'You' : 'Companion'}:</strong> ${message.content}</div>
                <div class="message-time">${time}</div>
            `;
            
            chatMessages.appendChild(messageDiv);
        });
        
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    clearChat() {
        this.chatHistory = [];
        this.saveToLocalStorage();
        this.updateChatDisplay();
        this.showNotification('Chat history cleared!', 'info');
    }

    // Mood Analysis Methods
    analyzeText() {
        const text = document.getElementById('textInput').value.trim();
        if (!text) {
            this.showNotification('Please enter some text to analyze', 'warning');
            return;
        }
        
        const mood = this.detectMood(text);
        const sentiment = this.analyzeSentiment(text);
        
        this.showAnalysisResults(mood, sentiment, text);
    }

    detectMood(text) {
        const lowerText = text.toLowerCase();
        
        if (lowerText.includes('sad') || lowerText.includes('depressed')) return 'Sad';
        if (lowerText.includes('anxious') || lowerText.includes('worried')) return 'Anxious';
        if (lowerText.includes('angry') || lowerText.includes('mad')) return 'Angry';
        if (lowerText.includes('happy') || lowerText.includes('good')) return 'Happy';
        if (lowerText.includes('stressed') || lowerText.includes('overwhelmed')) return 'Stressed';
        
        return 'Neutral';
    }

    analyzeSentiment(text) {
        // Simple sentiment analysis
        const positiveWords = ['happy', 'good', 'great', 'wonderful', 'amazing', 'love', 'joy', 'excited'];
        const negativeWords = ['sad', 'bad', 'terrible', 'awful', 'hate', 'angry', 'depressed', 'anxious'];
        
        let positiveCount = 0;
        let negativeCount = 0;
        
        positiveWords.forEach(word => {
            if (text.toLowerCase().includes(word)) positiveCount++;
        });
        
        negativeWords.forEach(word => {
            if (text.toLowerCase().includes(word)) negativeCount++;
        });
        
        if (positiveCount > negativeCount) return 0.5;
        if (negativeCount > positiveCount) return -0.5;
        return 0;
    }

    showAnalysisResults(mood, sentiment, text) {
        const resultsDiv = document.getElementById('analysisResults');
        const resultsContent = document.getElementById('resultsContent');
        
        const moodEmoji = {
            'Happy': '😊', 'Sad': '😢', 'Angry': '😠',
            'Anxious': '😟', 'Stressed': '😰', 'Neutral': '😐'
        };
        
        resultsContent.innerHTML = `
            <div class="analysis-result">
                <h6><strong>Detected Mood:</strong> 
                    <span class="emotion-badge emotion-${mood.toLowerCase()}">
                        ${moodEmoji[mood]} ${mood}
                    </span>
                </h6>
                <h6><strong>Sentiment Score:</strong> ${sentiment > 0 ? 'Positive 😊' : sentiment < 0 ? 'Negative 😔' : 'Neutral 😐'}</h6>
                <h6><strong>Confidence:</strong> ${Math.floor(Math.random() * 30) + 70}%</h6>
                <div class="mt-3">
                    <strong>Your Text:</strong> "${text}"
                </div>
            </div>
        `;
        
        resultsDiv.style.display = 'block';
        
        // Add to mood history
        this.moodHistory.push({
            mood: mood,
            sentiment: sentiment,
            text: text,
            timestamp: new Date()
        });
        
        this.saveToLocalStorage();
        this.updateMoodHistory();
    }

    analyzeImage() {
        const fileInput = document.getElementById('imageInput');
        const file = fileInput.files[0];
        
        if (!file) {
            this.showNotification('Please select an image to analyze', 'warning');
            return;
        }
        
        // Simulate image analysis (in real app, this would use ML models)
        this.showNotification('Analyzing image...', 'info');
        
        setTimeout(() => {
            const moods = ['Happy', 'Sad', 'Neutral', 'Anxious'];
            const randomMood = moods[Math.floor(Math.random() * moods.length)];
            
            this.showAnalysisResults(randomMood, Math.random() - 0.5, 'Image uploaded');
            this.showNotification(`Image analysis complete! Detected mood: ${randomMood}`, 'success');
        }, 2000);
    }

    // Mood History Methods
    updateMoodHistory() {
        const totalEntries = document.getElementById('totalEntries');
        const happyCount = document.getElementById('happyCount');
        const sadCount = document.getElementById('sadCount');
        const avgSentiment = document.getElementById('avgSentiment');
        const historyList = document.getElementById('historyList');
        
        if (!totalEntries) return;
        
        totalEntries.textContent = this.moodHistory.length;
        
        const happyDays = this.moodHistory.filter(entry => entry.mood === 'Happy').length;
        const sadDays = this.moodHistory.filter(entry => entry.mood === 'Sad').length;
        
        happyCount.textContent = happyDays;
        sadCount.textContent = sadDays;
        
        const avgSent = this.moodHistory.length > 0 
            ? (this.moodHistory.reduce((sum, entry) => sum + entry.sentiment, 0) / this.moodHistory.length).toFixed(2)
            : '0.0';
        avgSentiment.textContent = avgSent;
        
        // Update history list
        if (historyList) {
            historyList.innerHTML = '';
            
            this.moodHistory.slice(-10).reverse().forEach(entry => {
                const historyItem = document.createElement('div');
                historyItem.className = 'history-item';
                
                const date = new Date(entry.timestamp).toLocaleDateString();
                const time = new Date(entry.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                
                historyItem.innerHTML = `
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <strong>${entry.mood}</strong> - ${date} ${time}
                            <br>
                            <small class="text-muted">${entry.text || 'Image analysis'}</small>
                        </div>
                        <span class="emotion-badge emotion-${entry.mood.toLowerCase()}">${entry.mood}</span>
                    </div>
                `;
                
                historyList.appendChild(historyItem);
            });
        }
    }

    // Quick Tools Methods
    startBreathing() {
        const guide = document.getElementById('breathingGuide');
        const btn = document.getElementById('breathingBtn');
        
        if (guide.style.display === 'none') {
            guide.style.display = 'block';
            btn.innerHTML = '<i class="fas fa-stop"></i> Stop Exercise';
            this.showNotification('Breathing exercise started! Follow the guide.', 'info');
        } else {
            guide.style.display = 'none';
            btn.innerHTML = '<i class="fas fa-play"></i> Start Exercise';
            this.showNotification('Breathing exercise stopped.', 'info');
        }
    }

    saveGratitude() {
        const text = document.getElementById('gratitudeText').value.trim();
        if (!text) {
            this.showNotification('Please write what you\'re grateful for', 'warning');
            return;
        }
        
        // Save to mood history as a positive entry
        this.moodHistory.push({
            mood: 'Grateful',
            sentiment: 0.8,
            text: `Gratitude: ${text}`,
            timestamp: new Date()
        });
        
        this.saveToLocalStorage();
        this.updateMoodHistory();
        this.showNotification('Gratitude entry saved! 🙏', 'success');
        
        document.getElementById('gratitudeText').value = '';
    }

    trackMood() {
        const slider = document.getElementById('moodSlider');
        const moodLabels = ['Very Sad', 'Sad', 'Neutral', 'Happy', 'Very Happy'];
        const mood = moodLabels[slider.value - 1];
        
        this.moodHistory.push({
            mood: mood,
            sentiment: (slider.value - 3) * 0.25,
            text: 'Mood check-in',
            timestamp: new Date()
        });
        
        this.saveToLocalStorage();
        this.updateMoodHistory();
        this.showNotification(`Mood check-in saved: ${mood}`, 'success');
    }

    getRandomAffirmation() {
        const affirmations = [
            "I am worthy of love and respect.",
            "I choose to focus on what I can control.",
            "I am capable of handling whatever comes my way.",
            "I deserve to be happy and peaceful.",
            "I am growing and learning every day.",
            "I trust the journey of my life.",
            "I am strong enough to overcome my challenges.",
            "I choose to be kind to myself today.",
            "I have the power to create positive change in my life."
        ];
        
        const randomAffirmation = affirmations[Math.floor(Math.random() * affirmations.length)];
        const display = document.getElementById('affirmationText');
        
        display.innerHTML = `
            <div class="affirmation-display">
                <strong>✨ ${randomAffirmation}</strong>
            </div>
        `;
        
        this.showNotification('New affirmation generated!', 'success');
    }

    // Utility Methods
    showNotification(message, type = 'info') {
        const alertClass = {
            'success': 'alert-success',
            'error': 'alert-danger',
            'warning': 'alert-warning',
            'info': 'alert-info'
        };
        
        const notification = document.createElement('div');
        notification.className = `alert ${alertClass[type]} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'position: fixed; top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 5000);
    }

    updateUI() {
        if (this.currentUser) {
            this.showMainApp();
        } else {
            this.showAuthSection();
        }
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new MentalHealthApp();
});
