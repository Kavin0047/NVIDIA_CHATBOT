import streamlit as st
import google.generativeai as genai
import time

genai.configure(api_key='AIzaSyBZ2_kNMN0cK81n9iSaEPEXFUDir4Sax8Q')

generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat = model.start_chat(history=[])

def clear_chat_history():
    st.session_state.messages = []
    st.session_state.chat = model.start_chat(history=[])

st.set_page_config(page_title="NVIDIA Chatbot", page_icon=":robot_face:", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #121212;
        color: #ffffff;
    }
    .stTextInput > div > div > input {
        background-color: #2b2b2b;
        color: #ffffff;
    }
    .stButton > button {
        background-color: #76b900;
        color: white;
    }
    .stButton > button:hover {
        background-color: #5c9300;
    }
    .stMarkdown {
        color: #ffffff;
    }
    .st-emotion-cache-16idsys p {
        color: #ffffff;
    }
    .sidebar .sidebar-content {
        background-color: #1e1e1e;
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.title("About")
st.sidebar.info("This is an NVIDIA-focused chatbot powered by Google's Gemini AI. It provides information about NVIDIA products, history, and technologies.")
st.sidebar.warning("Note: This chatbot's knowledge is limited to NVIDIA-related topics and will not provide information on unrelated subjects.")

st.sidebar.image("https://www.nvidia.com/content/dam/en-zz/Solutions/about-nvidia/logo-and-brand/01-nvidia-logo-vert-500x200-2c50-d.png", width=200)

if st.sidebar.button("Clear Chat History"):
    clear_chat_history()
    st.rerun()

st.title("NVIDIA Chatbot powered by Gemini")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            placeholder = st.empty()
            full_response = message["content"]
            for i in range(len(full_response) + 1):
                placeholder.markdown(full_response[:i] + "▌")
                time.sleep(0.01)
            placeholder.markdown(full_response)
        else:
            st.markdown(message["content"])

prompt = st.chat_input("Ask me about NVIDIA...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    nvidia_prompt = f"""You are an AI assistant specifically focused on NVIDIA. Your knowledge is limited to NVIDIA's products, history, technologies, and directly related topics. Follow these guidelines:
    
    1. If the query is about NVIDIA or directly related to NVIDIA's business, products, or industry, provide a detailed and informative response.
    2. If asked to compare NVIDIA products with others, you may briefly mention competitors but always bring the focus back to NVIDIA's strengths.
    3. If the query is not related to NVIDIA or its industry (e.g., asking about Apple stocks or unrelated topics), politely explain that you're an NVIDIA-specific assistant and cannot provide information on unrelated topics.
    4. Do not invent or assume information. If you're unsure about something specific to NVIDIA, say so.
    5. Always maintain a professional and helpful tone.
    
    Human: {prompt}
    
    AI Assistant: """
    
    try:
        with st.spinner("Thinking..."):
            response = st.session_state.chat.send_message(nvidia_prompt)
            assistant_response = response.text
    except Exception as e:
        assistant_response = "I apologize, but I encountered an error while processing your request. Please try again or rephrase your question."
    
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    
    with st.chat_message("assistant"):
        placeholder = st.empty()
        for i in range(len(assistant_response) + 1):
            placeholder.markdown(assistant_response[:i] + "▌")
            time.sleep(0.01)
        placeholder.markdown(assistant_response)