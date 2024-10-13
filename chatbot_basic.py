import streamlit as st
import google.generativeai as genai

# Configure the Gemini API
genai.configure(api_key='YOUR API-KEY')

# Set up the model
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

# Initialize chat history and Gemini chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat = model.start_chat(history=[])

# Function to clear chat history
def clear_chat_history():
    st.session_state.messages = []
    st.session_state.chat = model.start_chat(history=[])

# Streamlit UI
st.title("NVIDIA Chatbot powered by Gemini")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
prompt = st.chat_input("Ask me about NVIDIA...")

if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.write(prompt)

    # Generate NVIDIA-focused response
    nvidia_prompt = f"""You are an AI assistant specifically focused on NVIDIA. Your knowledge is limited to NVIDIA's products, history, technologies, and directly related topics. Follow these guidelines:

    1. If the query is about NVIDIA or directly related to NVIDIA's business, products, or industry, provide a detailed and informative response.
    2. If asked to compare NVIDIA products with others, you may briefly mention competitors but always bring the focus back to NVIDIA's strengths.
    3. If the query is not related to NVIDIA or its industry (e.g., asking about Apple stocks or unrelated topics), politely explain that you're an NVIDIA-specific assistant and cannot provide information on unrelated topics.
    4. Do not invent or assume information. If you're unsure about something specific to NVIDIA, say so.
    5. Always maintain a professional and helpful tone.

    Human: {prompt}

    AI Assistant: """

    try:
        response = st.session_state.chat.send_message(nvidia_prompt)
        assistant_response = response.text
    except Exception as e:
        assistant_response = "I apologize, but I encountered an error while processing your request. Please try again or rephrase your question."

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.write(assistant_response)

# Sidebar with additional information
st.sidebar.title("About")
st.sidebar.info("This is an NVIDIA-focused chatbot powered by Google's Gemini AI. It provides information about NVIDIA products, history, and technologies.")
st.sidebar.warning("Note: This chatbot's knowledge is limited to NVIDIA-related topics and will not provide information on unrelated subjects.")

# Add a button to clear chat history
if st.sidebar.button("Clear Chat History"):
    clear_chat_history()
    st.rerun()
