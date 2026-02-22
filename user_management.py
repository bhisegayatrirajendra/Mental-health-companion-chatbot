import streamlit as st
import random
import string
from database import DatabaseManager
from typing import Optional, Dict, Any

class UserManagement:
    def __init__(self):
        self.db = DatabaseManager()
        
    def generate_anonymous_username(self) -> str:
        """Generate random anonymous username"""
        adjectives = ["Happy", "Calm", "Peaceful", "Bright", "Gentle", "Kind", "Wise"]
        nouns = ["Mind", "Soul", "Heart", "Spirit", "Star", "Moon", "Sun"]
        number = random.randint(100, 999)
        
        username = f"{random.choice(adjectives)}{random.choice(nouns)}{number}"
        return username
    
    def login_page(self) -> Optional[Dict[str, Any]]:
        """Display login page"""
        st.title("🔐 Login")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col1, col2 = st.columns(2)
            with col1:
                login_button = st.form_submit_button("Login", type="primary")
            with col2:
                anonymous_button = st.form_submit_button("Use Anonymous Mode")
            
            if login_button:
                if not username or not password:
                    st.error("Please enter both username and password")
                    return None
                
                user = self.db.authenticate_user(username, password)
                if user:
                    st.success(f"Welcome back, {user['username']}! 🎉")
                    st.session_state.current_user = user
                    st.session_state.logged_in = True
                    return user
                else:
                    st.error("Invalid username or password")
                    return None
            
            if anonymous_button:
                anonymous_username = self.generate_anonymous_username()
                user_id = self.db.create_user(anonymous_username, is_anonymous=True)
                
                user = {
                    'id': user_id,
                    'username': anonymous_username,
                    'email': None,
                    'is_anonymous': True,
                    'profile_data': {}
                }
                
                st.success(f"Anonymous session created as {anonymous_username}! 🎭")
                st.session_state.current_user = user
                st.session_state.logged_in = True
                return user
    
    def register_page(self) -> Optional[Dict[str, Any]]:
        """Display registration page"""
        st.title("📝 Register")
        
        with st.form("register_form"):
            username = st.text_input("Username", placeholder="Choose a unique username")
            email = st.text_input("Email (Optional)", placeholder="your.email@example.com")
            password = st.text_input("Password", type="password", placeholder="Create a strong password")
            confirm_password = st.text_input("Confirm Password", type="password", 
                                           placeholder="Confirm your password")
            
            submitted = st.form_submit_button("Create Account", type="primary")
            
            if submitted:
                if not username or not password:
                    st.error("Username and password are required")
                    return None
                
                if password != confirm_password:
                    st.error("Passwords do not match")
                    return None
                
                if len(password) < 6:
                    st.error("Password must be at least 6 characters long")
                    return None
                
                try:
                    user_id = self.db.create_user(username, email, password, is_anonymous=False)
                    
                    user = {
                        'id': user_id,
                        'username': username,
                        'email': email,
                        'is_anonymous': False,
                        'profile_data': {}
                    }
                    
                    st.success(f"Account created successfully! Welcome, {username}! 🎉")
                    st.session_state.current_user = user
                    st.session_state.logged_in = True
                    return user
                    
                except Exception as e:
                    st.error("Username or email already exists. Please try another one.")
                    return None
    
    def logout(self):
        """Logout current user"""
        if 'current_user' in st.session_state:
            del st.session_state.current_user
        st.session_state.logged_in = False
        st.success("Logged out successfully!")
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get current logged-in user"""
        return st.session_state.get('current_user')
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        return st.session_state.get('logged_in', False)
    
    def display_user_info(self):
        """Display current user information"""
        user = self.get_current_user()
        if user:
            with st.sidebar:
                st.markdown("---")
                st.markdown("### 👤 User Profile")
                
                if user['is_anonymous']:
                    st.info(f"🎭 **Anonymous User**\n\n{user['username']}")
                else:
                    st.success(f"👤 **{user['username']}**")
                    if user['email']:
                        st.caption(f"📧 {user['email']}")
                
                if st.button("🚪 Logout", key="logout_btn"):
                    self.logout()
                    st.rerun()
