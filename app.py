import streamlit as st
import boto3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup
st.set_page_config(
    page_title="Caly Poly Math Placement Chatbot", 
    page_icon="🧮",  # Change icon here
    layout="wide"
)

# Custom CSS for colors
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background-color: white;
        font-family: 'Poppins', sans-serif;
    }
    * {
        font-family: 'Poppins', sans-serif !important;
    }
    .stChatMessage {
        background-color: #f8f9fa;
        color: black !important;
        max-width: 800px !important;
        margin: 0 auto !important;
    }
    .stChatMessage p {
        color: black !important;
    }
    .stChatMessage div {
        color: black !important;
    }
    .stTextInput > div > div > input {
        background-color: white;
        color: black;
    }
    .stChatInput {
        max-width: 800px !important;
        margin: 0 auto !important;
        background-color: #4A8B6B !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    .stChatInput > div {
        max-width: 800px !important;
        margin: 0 auto !important;
    }
    .stChatInput input {
        background-color: white !important;
        color: black !important;
        border: none !important;
        border-radius: 20px !important;
    }
    .stChatInput input:focus {
        outline: none !important;
        border: none !important;
        border-radius: 20px !important;
    }
    .stChatInput textarea:focus {
        outline: none !important;
        border: none !important;
        border-radius: 20px !important;
    }
    h1 {
        color: #235F45 !important;
        text-align: center !important;
    }
    .stMarkdown h1 {
        color: #235F45 !important;
        text-align: center !important;
    }
    .stBottom {
        background-color: #4A8B6B !important;
    }
    footer {
        background-color: #4A8B6B !important;
    }
    .stApp > footer {
        background-color: #4A8B6B !important;
    }
    .stChatInputContainer {
        background-color: #4A8B6B !important;
    }
    .stChatFloatingInputContainer {
        background-color: #4A8B6B !important;
    }
    section[data-testid="stChatInput"] {
        background-color: #4A8B6B !important;
    }
    div[data-testid="stChatInput"] {
        background-color: #4A8B6B !important;
    }
    .stChatMessage[data-testid="chat-message-assistant"] .stChatMessageAvatar {
        background-color: #235F45 !important;
    }
    .stChatMessage[data-testid="chat-message-assistant"] svg {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Add centered image at the top
col1, col2, col3 = st.columns([1,1,1])
with col2:
    st.image("calpoly-logo.png", width=200)

st.title("Cal Poly Math Placement Chatbot")

# AWS Setup
@st.cache_resource
def setup_bedrock():
    return boto3.client(
        'bedrock-agent-runtime',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_DEFAULT_REGION')
    )

# Initialize
if "messages" not in st.session_state:
    st.session_state.messages = []

bedrock = setup_bedrock()
kb_id = os.getenv('KNOWLEDGE_BASE_ID')

# Display chat history
for message in st.session_state.messages:
    if message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.write(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Chat input
if prompt := st.chat_input("Math ain't mathing? Ask me..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Call Bedrock Knowledge Base
                response = bedrock.retrieve_and_generate(
                    input={
                        'text': (
                            "You are a helpful assistant. "
                            "Always respond in clear, concise sentences. "
                            "When you use information from the knowledge base, cite it at the end.\n\n"
                            f"User question: {prompt}"
                        )
                    },
                    retrieveAndGenerateConfiguration={
                        'type': 'KNOWLEDGE_BASE',
                        'knowledgeBaseConfiguration': {
                            'knowledgeBaseId': kb_id,
                            'modelArn': f'arn:aws:bedrock:us-west-2::foundation-model/{os.getenv("BEDROCK_MODEL_ID")}'
                        }
                    }
                )
                
                answer = response['output']['text']
                st.write(answer)
                
                # Add to chat history
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except Exception as e:
                st.error(f"Error: {e}")
