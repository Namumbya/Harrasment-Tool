import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
import os

def init_gemini():
    """Initialize and return Gemini model"""
    try:
        # Load environment variables
        load_dotenv()
        
        # Get API key
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
        if not GOOGLE_API_KEY:
            st.error("Google API Key not found. Please check your .env file.")
            return None
            
        # Configure Gemini
        genai.configure(api_key=GOOGLE_API_KEY)
        
        # Initialize model
        model = genai.GenerativeModel('gemini-pro')
        return model
        
    except Exception as e:
        st.error(f"Error initializing Gemini: {str(e)}")
        return None