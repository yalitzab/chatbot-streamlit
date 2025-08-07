import streamlit as st

# Setup
st.set_page_config(
    page_title="Mr. Mini Clint Bot", 
    page_icon="🤖",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@400;600;700&family=Georgia:wght@400;700&display=swap');
    
    .stApp {
        background-color: #F8F8F8;
        font-family: 'Georgia', serif;
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        padding: 20px;
    }
    
    .main-container {
        width: 100%;
        max-width: 400px;
        aspect-ratio: 9/16;
        background-color: white;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }
    
    .header {
        background-color: #154734;
        color: white;
        padding: 20px;
        text-align: center;
        font-family: 'Oswald', sans-serif;
        font-weight: 700;
        font-size: 18px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .chat-area {
        flex: 1;
        padding: 20px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 15px;
    }
    
    .bot-message {
        display: flex;
        align-items: flex-start;
        gap: 10px;
    }
    
    .user-message {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        flex-direction: row-reverse;
    }
    
    .bot-bubble {
        background-color: #154734;
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 4px;
        max-width: 70%;
        font-family: 'Georgia', serif;
        font-size: 14px;
        line-height: 1.4;
    }
    
    .user-bubble {
        background-color: #e0e0e0;
        color: black;
        padding: 12px 16px;
        border-radius: 18px 18px 4px 18px;
        max-width: 70%;
        font-family: 'Georgia', serif;
        font-size: 14px;
        line-height: 1.4;
    }
    
    .avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        flex-shrink: 0;
        overflow: hidden;
        background-color: #C69214;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .avatar img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    
    .input-area {
        padding: 15px 20px;
        border-top: 1px solid #e0e0e0;
        display: flex;
        gap: 10px;
        align-items: center;
    }
    
    .stTextInput > div > div > input {
        background-color: white !important;
        color: black !important;
        font-family: 'Georgia', serif !important;
        border: 2px solid #154734 !important;
        border-radius: 20px !important;
        padding: 10px 15px !important;
        font-size: 14px !important;
        width: 100% !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #C69214 !important;
        box-shadow: 0 0 0 2px rgba(198, 146, 20, 0.2) !important;
    }
    
    .stButton > button {
        background-color: #154734 !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 10px 20px !important;
        font-family: 'Oswald', sans-serif !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        font-size: 12px !important;
        min-width: 60px !important;
    }
    
    .stButton > button:hover {
        background-color: #C69214 !important;
    }
    
    /* Hide Streamlit elements */
    .stDeployButton {display: none;}
    header[data-testid="stHeader"] {display: none;}
    .stMainBlockContainer {padding: 0 !important;}
    
    @media (max-width: 768px) {
        .stApp {
            padding: 0;
            align-items: stretch;
        }
        .main-container {
            max-width: 100%;
            height: 100vh;
            border-radius: 0;
            aspect-ratio: unset;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main container
st.markdown("""
<div class="main-container">
    <div class="header">
        MR. MINI CLINT BOT
    </div>
    <div class="chat-area" id="chat-area">
""", unsafe_allow_html=True)

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "bot":
        st.markdown(f"""
        <div class="bot-message">
            <div class="avatar">
                <img src="https://www.calpoly.edu/themes/custom/calpoly/logo.svg" alt="Bot" onerror="this.innerHTML='🤖'">
            </div>
            <div class="bot-bubble">{message["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="user-message">
            <div class="avatar">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Mustang_logo_black.svg/512px-Mustang_logo_black.svg.png" alt="User" onerror="this.innerHTML='🐎'">
            </div>
            <div class="user-bubble">{message["content"]}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
    </div>
    <div class="input-area">
""", unsafe_allow_html=True)

# Chat input
col1, col2 = st.columns([4, 1])
with col1:
    user_input = st.text_input("", placeholder="Math ain't mathing? Ask me...", key="chat_input", label_visibility="collapsed")
with col2:
    send_button = st.button("SEND")

st.markdown("</div></div>", unsafe_allow_html=True)

# Handle user input
if (send_button and user_input) or (user_input and user_input != st.session_state.get("last_input", "")):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Add bot response (placeholder)
    bot_response = f"Let me check on that for you... I see you're asking about '{user_input}'. This is a placeholder response from Mr. Mini Clint Bot!"
    st.session_state.messages.append({"role": "bot", "content": bot_response})
    
    # Update last input
    st.session_state.last_input = user_input
    
    # Rerun to show new messages
    st.rerun()