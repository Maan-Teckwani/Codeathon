import streamlit as st
import google.generativeai as genai
import os
import base64

# Configure API key
os.environ['GOOGLE_API_KEY'] = ''
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

st.set_page_config(page_title="Mental Health Chatbot")

# Load and encode background image
def get_base64(background):
    try:
        with open(background, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

# Try to load background image
bg_path = "meditation.jpg"
bin_str = get_base64(bg_path)
if bin_str:
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{bin_str}");
            background-size: cover;
        }}
        </style>
        """, unsafe_allow_html=True)
else:
    st.warning(f"Could not load background image from {bg_path}")

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

def generate_response(user_input):
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(
            f"""
            Someone is feeling emotional and sharing their thoughts with you. 
            Be warm, deeply understanding, and respond like a nurturing and compassionate guide. 
            Provide comfort, reassurance, and encouragement rather than just facts.
            
            User: {user_input}
            """
        )
        ai_response = response.text
        return ai_response
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        st.error(error_msg)
        return error_msg

def generate_affirmation():
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(
            "Share a warm and deeply reassuring positive affirmation for someone who needs comfort."
        )
        return response.text
    except Exception as e:
        st.error(f"Error generating affirmation: {str(e)}")
        return str(e)

def generate_meditation_guide():
    try:
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(
            "Provide a gentle and soothing 5-minute guided meditation script for deep relaxation and emotional healing."
        )
        return response.text
    except Exception as e:
        st.error(f"Error generating meditation guide: {str(e)}")
        return str(e)

st.title("🌿 Gentle Companion: Your Mental Wellness Chatbot")

# Display chat history
for message in st.session_state.messages:
    role_display = "You" if message["role"] == "user" else "AI"
    st.markdown(f"{role_display}: {message['content']}")

# Pin user input to bottom of the screen
user_message = st.chat_input("How are you feeling today? I'm here for you. 💙")
if user_message:
    with st.spinner("Listening with an open heart..."):
        ai_response = generate_response(user_message)
        st.session_state.messages.append({"role": "user", "content": user_message})
        st.session_state.messages.append({"role": "model", "content": ai_response})
        st.rerun()

# Buttons for additional features
col1, col2 = st.columns(2)

with col1:
    if st.button("🌞 Send me a positive affirmation"):
        with st.spinner("Sending love your way..."):
            st.markdown(f"Affirmation: {generate_affirmation()}")

with col2:
    if st.button("🧘 Guide me through meditation"):
        with st.spinner("Let’s breathe and find peace together..."):
            st.markdown(f"Guided Meditation: {generate_meditation_guide()}")
