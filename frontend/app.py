import streamlit as st
import requests
import json
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="RAG Query Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with better color coding
st.markdown("""
<style>
/* Import Google Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Global styles */
.stApp {
    font-family: 'Inter', sans-serif;
}

/* Main header with gradient animation */
.main-header {
    font-size: 2.8rem;
    font-weight: 800;
    text-align: center;
    margin-bottom: 2rem;
    background: linear-gradient(
        135deg,
        #667eea 0%,
        #764ba2 50%,
        #f093fb 100%
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-size: 300% 300%;
    animation: gradientShift 4s ease-in-out infinite;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* User message bubbles */
.user-message {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 0.8rem 1.2rem;
    border-radius: 18px 18px 4px 18px;
    max-width: 80%;
    margin-left: auto;
    margin-bottom: 0.8rem;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    animation: slideInRight 0.3s ease-out;
}

/* Assistant message container */
.assistant-container {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 0.8rem 1.2rem;
    border-radius: 18px 18px 18px 4px;
    max-width: 85%;
    margin-right: auto;
    margin-bottom: 0.8rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    animation: slideInLeft 0.3s ease-out;
}

@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(20px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-20px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

/* Answer box with gradient border */
.answer-box {
    padding: 1.2rem 1.5rem;
    border-radius: 12px;
    margin: 0.8rem 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,255,255,0.6));
    border-left: 4px solid #667eea;
    border-image: linear-gradient(180deg, #667eea, #764ba2) 1;
    box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    color: #2d3748;
    font-size: 0.95rem;
    line-height: 1.6;
}

/* Source cards with gradient hover */
.source-box {
    padding: 0.8rem 1rem;
    border-radius: 10px;
    margin: 0.5rem 0;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.08), rgba(118, 75, 162, 0.05));
    border: 1px solid rgba(102, 126, 234, 0.2);
    transition: all 0.3s ease;
    color: #4a5568;
    font-size: 0.9rem;
}

.source-box:hover {
    border-color: #667eea;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.15), rgba(118, 75, 162, 0.08));
    transform: translateX(5px);
    box-shadow: 0 3px 12px rgba(102, 126, 234, 0.15);
}

.source-icon {
    color: #764ba2;
    margin-right: 8px;
}

/* Source details summary */
details summary {
    cursor: pointer;
    color: #667eea;
    font-weight: 600;
    padding: 0.5rem 0;
    transition: color 0.3s ease;
    font-size: 0.95rem;
}

details summary:hover {
    color: #764ba2;
}

details summary::-webkit-details-marker {
    color: #667eea;
}

/* Input field styling */
.stTextInput input {
    border-radius: 12px !important;
    border: 2px solid #e2e8f0 !important;
    padding: 0.6rem 1rem !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
    background: white !important;
    color: #2d3748 !important;
}

.stTextInput input:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
}

/* Button with gradient */
.stButton button {
    width: 100%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 0.6rem 1.2rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
}

.stButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
}

.stButton button:active {
    transform: translateY(0px) !important;
}

/* Sidebar styling */
.css-1d391kg {
    background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%) !important;
}

.sidebar-title {
    color: #2d3748;
    font-weight: 700;
    font-size: 1.2rem;
}

/* Divider styling */
hr {
    border: none;
    height: 2px;
    background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
    margin: 1.5rem 0;
    opacity: 0.3;
}

/* Status badges */
.status-success {
    background: linear-gradient(135deg, #48bb78, #38a169);
    color: white;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-weight: 600;
    display: inline-block;
}

.status-error {
    background: linear-gradient(135deg, #fc8181, #e53e3e);
    color: white;
    padding: 0.3rem 0.8rem;
    border-radius: 20px;
    font-weight: 600;
    display: inline-block;
}

/* Info box */
.stInfo {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.08), rgba(118, 75, 162, 0.05)) !important;
    border-left: 4px solid #667eea !important;
    border-radius: 10px !important;
}

/* Spinner customization */
.stSpinner > div {
    border-color: #667eea !important;
}

/* Error/Success messages */
.stAlert {
    border-radius: 12px !important;
}

/* Dark mode overrides */
@media (prefers-color-scheme: dark) {
    .assistant-container {
        background: linear-gradient(135deg, #2d3748, #1a202c) !important;
        color: #e2e8f0 !important;
    }
    
    .answer-box {
        background: linear-gradient(135deg, rgba(45, 55, 72, 0.9), rgba(26, 32, 44, 0.8)) !important;
        color: #e2e8f0 !important;
        border-left-color: #9f7aea !important;
    }
    
    .source-box {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.12), rgba(118, 75, 162, 0.08)) !important;
        border-color: rgba(102, 126, 234, 0.3) !important;
        color: #e2e8f0 !important;
    }
    
    .source-box:hover {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.12)) !important;
    }
    
    .stTextInput input {
        background: #2d3748 !important;
        border-color: #4a5568 !important;
        color: #e2e8f0 !important;
    }
    
    .stTextInput input:focus {
        border-color: #9f7aea !important;
        box-shadow: 0 0 0 3px rgba(159, 122, 234, 0.2) !important;
    }
    
    .css-1d391kg {
        background: linear-gradient(180deg, #1a202c, #2d3748) !important;
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.12), rgba(118, 75, 162, 0.08)) !important;
    }
}

/* Responsive design */
@media (max-width: 768px) {
    .main-header {
        font-size: 2rem;
    }
    
    .user-message, .assistant-container {
        max-width: 95%;
    }
    
    .answer-box {
        padding: 1rem;
    }
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #667eea, #764ba2);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #764ba2, #667eea);
}
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'api_url' not in st.session_state:
    st.session_state.api_url = "http://172.20.113.214:8000/api/v1/hybrid-query"
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

# Sidebar with gradient background
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)
    st.markdown('<h2 style="color: #2d3748; font-weight: 700;">⚙️ Settings</h2>', unsafe_allow_html=True)
    
    # API Configuration
    api_url = st.text_input(
        "API URL",
        value=st.session_state.api_url,
        help="URL of your FastAPI backend"
    )
    st.session_state.api_url = api_url
    
    st.divider()
    
    # Health check with colored button
    if st.button("🔍 Check API Health", use_container_width=True):
        try:
            response = requests.get(f"{api_url}/health", timeout=5)
            if response.status_code == 200:
                st.markdown('<span class="status-success">✅ API is healthy!</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="status-error">❌ API is not responding</span>', unsafe_allow_html=True)
        except:
            st.markdown('<span class="status-error">❌ Cannot connect to API</span>', unsafe_allow_html=True)
    
    st.divider()
    
    # Clear history
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()
    
    st.divider()
    
    # Statistics in sidebar
    query_count = len([msg for msg in st.session_state.chat_history if msg['type'] == 'user'])
    st.metric("Total Queries", query_count)
    
    st.divider()
    st.caption("💡 Tip: Ask questions about your documents")
    st.caption("🔄 App Version: 1.0.0")

# Main content
st.markdown('<h1 class="main-header">🤖 RAG Query Assistant</h1>', unsafe_allow_html=True)

# Input section
col1, col2 = st.columns([5, 1])

with col1:
    user_question = st.text_input(
        "Ask a question:",
        placeholder="Type your question here...",
        key="user_input",
        label_visibility="collapsed",
        value=st.session_state.input_text
    )

with col2:
    submit_button = st.button(
        "🚀 Ask",
        use_container_width=True,
        type="primary"
    )

# Display chat history
st.divider()
st.subheader("💬 Conversation")

# Create placeholder for chat messages
chat_container = st.container()

with chat_container:
    if not st.session_state.chat_history:
        st.info("💡 Start a conversation by asking a question above!")
    
    for idx, message in enumerate(st.session_state.chat_history):
        if message["type"] == "user":
            # User message with gradient
            st.markdown(f"""
                <div class="user-message">
                    <strong>👤 You</strong><br>
                    {message["content"]}
                </div>
            """, unsafe_allow_html=True)
        else:
            # Assistant response with better styling
            sources_html = ''
            for source in message.get("sources", []):
                sources_html += f'<div class="source-box"><span class="source-icon">📄</span> {source}</div>'
            
            st.markdown(f"""
                <div class="assistant-container">
                    <strong>🤖 Assistant</strong>
                    <div class="answer-box">
                        {message["answer"]}
                    </div>
                    <details>
                        <summary>📚 View Sources ({len(message.get("sources", []))})</summary>
                        {sources_html}
                    </details>
                    <div style="font-size: 0.7rem; color: #a0aec0; margin-top: 0.5rem; text-align: right;">
                        {message.get("timestamp", "")}
                    </div>
                </div>
            """, unsafe_allow_html=True)

# Handle new query
if submit_button and user_question:
    with st.spinner("🧠 Generating response..."):
        try:
            # Prepare request
            payload = {
                "query": user_question,
                "max_sources": 3
            }
            
            # Make API call
            response = requests.post(
                st.session_state.api_url,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Add to chat history
                st.session_state.chat_history.append({
                    "type": "user",
                    "content": user_question
                })
                
                st.session_state.chat_history.append({
                    "type": "assistant",
                    "answer": data.get("answer", "No answer received"),
                    "sources": data.get("sources", []),
                    "timestamp": datetime.now().strftime("%I:%M %p")
                })
                
                # Clear input by setting session state
                st.session_state.input_text = ""
                
                # Rerun to update UI
                st.rerun()
                
            else:
                st.error(f"❌ Error: {response.status_code} - {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to API. Please check if FastAPI is running.")
        except requests.exceptions.Timeout:
            st.error("❌ Request timed out. Please try again.")
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")

# Footer with gradient
st.divider()
col1, col2, col3, col4 = st.columns(4)

with col1:
    query_count = len([msg for msg in st.session_state.chat_history if msg['type'] == 'user'])
    st.caption(f"📝 Total queries: {query_count}")

with col2:
    st.caption("🔗 Built with Streamlit + FastAPI")

with col3:
    last_query = st.session_state.chat_history[-1]["timestamp"] if st.session_state.chat_history else "N/A"
    st.caption(f"⏱️ Last query: {last_query}")

with col4:
    st.caption("🏷️ v1.0.0")