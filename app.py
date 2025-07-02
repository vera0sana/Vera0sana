import streamlit as st
from deep_translator import GoogleTranslator
from openai import OpenAI
import os

# App title
st.set_page_config(page_title="Cognira – Emotional Receptionist", layout="centered")
st.title("🧠 Cognira: AI Emotional Receptionist")
st.markdown("Share your feelings in any language. Cognira will understand and respond with empathy.")

# User input
user_input = st.text_area("💬 What's on your mind?", placeholder="Type how you're feeling...")

# Language detection and translation
def translate_to_english(text):
    try:
        translated = GoogleTranslator(source='auto', target='en').translate(text)
        return translated
    except Exception as e:
        return f"Translation error: {str(e)}"

# OpenAI Response
def generate_response(text):
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an empathetic mental health assistant named Cognira."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Response error: {str(e)}"

# Main logic
if user_input:
    with st.spinner("Cognira is listening..."):
        english_input = translate_to_english(user_input)
        st.markdown(f"**Translated to English:** {english_input}")
        reply = generate_response(english_input)
        st.markdown(f"**Cognira says:** {reply}")
