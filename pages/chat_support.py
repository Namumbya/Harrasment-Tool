import streamlit as st
import datetime
import json
from geopy.geocoders import Nominatim
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Loading environment variables
load_dotenv()

# Initializing Gemini
def init_gemini():
    """Initialize Gemini model"""
    try:
        GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
        if not GOOGLE_API_KEY:
            st.error("Google API Key not found. Please check your .env file.")
            return None
            
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        return model
    except Exception as e:
        st.error(f"Error initializing Gemini: {str(e)}")
        return None

def get_user_location():
    """Get user's location using geopy"""
    try:
        geolocator = Nominatim(user_agent="harassment_support_tool")
        location = geolocator.geocode(st.session_state.get('location', ''))
        return location
    except Exception:
        return None

def handle_emergency(location):
    """Handle emergency harassment situations"""
    emergency_response = """
    I understand you're in a dangerous situation. Let me help you right away:

    1. 🚨 Immediate Safety Steps:
       • Move to a safe location if possible (police station, hospital, trusted friend's house)
       • Call Police: 911 
       • Gender-Based Violence Command Centre: 0800-428-428
       • Save all evidence (screenshots, recordings, messages)
       
    2. 📱 Document Everything:
       • Time and location of incident
       • Description of harasser
       • Names of any witnesses
       • Take photos of any injuries or damage
    """
    
    st.session_state.messages.append({
        "role": "assistant",
        "content": emergency_response
    })

def handle_support_request():
    """Handle harassment support conversations"""
    model = init_gemini()
    if model is None:
        st.error("I'm having trouble connecting. Please try again in a moment.")
        return
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        welcome_msg = {
            "role": "assistant",
            "content": """Hi, I'm Sara, your harassment support assistant. I can help you with:
            • Immediate safety planning
            • Reporting harassment (workplace, cyber, public spaces)
            • Finding local support services
            • Understanding your legal rights
            • Safety strategies and prevention
            
            What kind of harassment situation would you like help with?"""
        }
        st.session_state.messages.append(welcome_msg)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Type your message here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            with st.chat_message("assistant"):
                # Enhanced harassment-specific context
                context = f"""You are Sara, a specialized harassment support assistant in Africa.
                Your primary focus is helping women dealing with harassment situations.

                Key areas of support:
                1. Workplace harassment
                2. Cyber harassment
                3. Public space harassment
                4. Sexual harassment
                5. Educational institution harassment

                For each response:
                1. Identify the type of harassment
                2. Provide immediate safety steps
                3. Suggest documentation methods
                4. Offer relevant support services
                5. Include legal rights information
                6. Share prevention strategies

                Previous conversation: {str(st.session_state.messages[-3:]) if len(st.session_state.messages) > 1 else 'None'}
                User message: {prompt}

                Response must:
                - Be specific to harassment situations
                - Include practical safety steps
                - Mention relevant local support services
                - Provide actionable advice
                - End with a supportive question about their safety needs
                """
                
                # Checking for emergency keywords
                emergency_keywords = ["attack", "following", "threat", "scared", "help", "emergency", "danger"]
                if any(keyword in prompt.lower() for keyword in emergency_keywords):
                    location = get_user_location()
                    handle_emergency(location)
                else:
                    response = model.generate_content(context)
                    if response and hasattr(response, 'text'):
                        assistant_response = response.text.strip()
                        
                        # harassment-focused response
                        if not any(word in assistant_response.lower() for word in ['harassment', 'safety', 'report', 'support', 'protect']):
                            assistant_response = """Let me help you address this harassment situation. 
                            
                            First, let's focus on your immediate safety. Are you currently in a safe place? 
                            
                            I can guide you through:
                            • Documenting the harassment
                            • Reporting options
                            • Safety planning
                            • Support services
                            
                            What would be most helpful right now?"""
                        
                        st.markdown(assistant_response)
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": assistant_response
                        })
                    else:
                        st.error("I'm having trouble understanding. Could you please provide more details about the harassment situation?")
                        
        except Exception as e:
            st.error("I'm having trouble connecting. Please try again in a moment.")

def show():
    """Main function to display the chat support interface"""
    st.title("🛡️ Harassment Support Chat")
    
    st.markdown("""
    I'm Sara, your dedicated harassment support assistant. I'm here to help you:
    • Deal with immediate harassment situations
    • Create safety plans
    • Find local support services
    • Understand your rights
    • Document and report incidents
    """)
    
    handle_support_request()
    
    with st.sidebar:
        st.subheader("🆘 Anti-Harassment Resources")
        st.markdown("""
        ### Emergency Contacts
        • Police: 112
        • GBV Command Centre: 0800-428-428
        • Women's Legal Aid: 0800-150-150
        
        ### Report Harassment
        • Workplace: Labour Department
        • Cyber: Cybercrime Unit
        • Educational: Institution Board
        
        ### Support Services
        • Counseling
        • Legal Aid
        • Safe Houses
        • Women's Support Groups
        
        [Find local services →](link)
        """)
        
        if st.button("💾 Save Chat History"):
            chat_data = {
                "history": st.session_state.messages,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.download_button(
                "Download Chat",
                json.dumps(chat_data, indent=2),
                "chat_history.json",
                "application/json"
            )
