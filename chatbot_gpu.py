import streamlit as st
import pandas as pd
import google.generativeai as genai
import time
import feedparser

genai.configure(api_key='YOUR API-KEY')

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

def fetch_nvidia_news():
    feed_url = "https://nvidianews.nvidia.com/releases.xml"
    feed = feedparser.parse(feed_url)
    return feed.entries[:5]  # Return the 5 most recent news items

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
    .news-item {
        background-color: #2b2b2b;
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 5px;
    }
    .news-item h4 {
        color: #76b900;
    }
    .news-item p {
        font-size: 0.9em;
    }
</style>
""", unsafe_allow_html=True)

gpu_data = {
    'Model': ["GTX 1050", "GTX 1060", "GTX 1070", "GTX 1080", "RTX 2060", "RTX 2070", "RTX 2080", "RTX 2080 Ti",'RTX 3060', 'RTX 3070', 'RTX 3080', 'RTX 3090'],
    'CUDA Cores': [ 640, 1280, 1920, 2560, 1920, 2304, 2944, 4352,3584, 5888, 8704, 10496],
    'Boost Clock (MHz)': [1455, 1708, 1683, 1733,1680, 1620, 1800, 1545,1777, 1725, 1710, 1695],
    'Memory Size (GB)': [2, 6, 8, 8, 6, 8, 8, 11, 12, 8, 10, 24],
    'Memory Type': ["GDDR5", "GDDR5", "GDDR5", "GDDR5X", "GDDR6", "GDDR6", "GDDR6", "GDDR6",'GDDR6', 'GDDR6', 'GDDR6X', 'GDDR6X']
}

df_gpu = pd.DataFrame(gpu_data)

def render_gpu_comparison():
    st.subheader("NVIDIA GPU Comparison")
    selected_gpus = st.multiselect("Select GPUs to compare", df_gpu['Model'].tolist())
    if selected_gpus:
        st.table(df_gpu[df_gpu['Model'].isin(selected_gpus)])
    else:
        st.info("Please select GPUs to compare")

with st.sidebar:
    st.title("About")
    st.info("This is an NVIDIA-focused chatbot.")
    st.image("https://www.nvidia.com/content/dam/en-zz/Solutions/about-nvidia/logo-and-brand/01-nvidia-logo-vert-500x200-2c50-d.png", width=200)
    
    if st.button("Clear Chat History"):
        clear_chat_history()
        st.rerun()

st.title("NVIDIA AI Assistant")

tab1, tab2, tab3 = st.tabs(["Chat", "GPU Comparison", "News"])

with tab1:
    if not st.session_state.messages:
        st.info("Welcome to the NVIDIA AI Assistant! Ask me anything about NVIDIA's products, technologies, or history.")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
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
        6. If the query is about recent news or events, you can refer to the news items displayed in the sidebar and incorporate that information into your response.
        7. Your name is JD.
        8. Keep the answer short and straightforward wherever possible. 
    
        Human: {prompt}
        AI Assistant: """
    
        try:
            with st.spinner("Writing..."):
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

with tab2:
    render_gpu_comparison()

with tab3:
    st.subheader("Recent NVIDIA News")
    news_items = fetch_nvidia_news()
    for item in news_items:
        st.markdown(f"**{item.title}**")
        st.write(item.summary[:200] + "...")
        st.markdown(f"[Read more]({item.link})")
        st.divider()
