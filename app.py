import streamlit as st
from deep_translator import GoogleTranslator
from openai import OpenAI
import os

# Page setup
st.set_page_config(page_title="Cognira – Emotional Receptionist", layout="centered")
st.markdown("<h1 style='text-align: center;'>🧠 Cognira: AI Emotional Receptionist</h1>", unsafe_allow_html=True)
st.markdown("#### 📱 Type your thoughts below in any language. Cognira will gently respond in English with empathy.")

# User input
user_input = st.text_area("💬 What's on your mind?", placeholder="Write here...", height=150)

# Translate text
def translate_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception as e:
        return f"Translation error: {str(e)}"

# Generate AI response
def generate_response(text):
    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You're a warm and empathetic emotional support assistant named Cognira."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Response error: {str(e)}"

# Response area
if user_input:
    with st.spinner("Cognira is listening..."):
        english_input = translate_to_english(user_input)
        st.success(f"🔄 Translated to English: *{english_input}*")
        reply = generate_response(english_input)
        st.markdown(f"🧠 **Cognira says:**\n\n> {reply}")

st.markdown("---")
st.caption("🌍 Cognira supports all major languages. Powered by OpenAI + Google Translate.")
