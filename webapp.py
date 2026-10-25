
import streamlit as st
from google import genai

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="Gemini AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Gemini AI Chatbot")
st.caption("Ask me anything!")

# -----------------------------
# Load API key securely
# -----------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"].strip()
except Exception:
    st.error(
        "Gemini API key not found. "
        "Please check D:/087/.streamlit/secrets.toml"
    )
    st.stop()

if not api_key or api_key == "YOUR_ACTUAL_GEMINI_API_KEY":
    st.error("Please add your actual Gemini API key to secrets.toml.")
    st.stop()

# -----------------------------
# Initialize Gemini client
# -----------------------------
client = genai.Client(api_key=api_key)

# -----------------------------
# Chat history
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# Chat input
# -----------------------------
user_prompt = st.chat_input("Type your message here...")

if user_prompt:
    # Display user message
    st.session_state.messages.append(
        {"role": "user", "content": user_prompt}
    )

    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Generate Gemini response
    with st.chat_message("assistant"):
        with st.spinner("Gemini is thinking..."):
            try:
                response = client.interactions.create(
                    model="gemini-3-flash-preview",
                    input=user_prompt
                )

                answer = response.output_text

                if not answer:
                    answer = "Sorry, I couldn't generate a response."

                st.markdown(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as e:
                st.error(f"Gemini API error: {e}")

