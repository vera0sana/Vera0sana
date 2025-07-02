import streamlit as st
from openai import OpenAI
from deep_translator import GoogleTranslator
from langdetect import detect
from textblob import TextBlob
from gtts import gTTS
import os
import uuid
import base64
import tempfile

# Streamlit UI setup
st.set_page_config(page_title="Cognira: Emotional Receptionist", layout="centered")

st.markdown("""
    <h1 style='text-align: center;'>🧠 Cognira: AI Emotional Receptionist</h1>
    <p style='text-align: center;'>Share your feelings in any language. Cognira will understand and respond with empathy.</p>
""", unsafe_allow_html=True)

# Initialize OpenAI client with latest version
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Text input
user_input = st.text_area("💬 What's on your mind?", placeholder="Write here...", height=100)

# Function to detect and translate input to English
def translate_to_english(text):
    try:
        lang = detect(text)
        if lang != 'en':
            return GoogleTranslator(source='auto', target='en').translate(text)
        return text
    except:
        return text

# Generate empathetic response from GPT-3.5
def get_openai_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an empathetic AI that provides emotional support in a warm and understanding way."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

# Convert GPT response to speech
def text_to_speech(text):
    tts = gTTS(text)
    filename = f"{uuid.uuid4().hex}.mp3"
    filepath = os.path.join(tempfile.gettempdir(), filename)
    tts.save(filepath)
    return filepath

# On submit
if st.button("🧠 Submit") and user_input.strip():
    with st.spinner("Analyzing your emotion..."):
        translated = translate_to_english(user_input)
        st.markdown(f"**Translated to English:** _{translated}_")

        try:
            response = get_openai_response(translated)
            st.markdown(f"**Cognira says:** {response}")

            # Voice playback
            mp3_file = text_to_speech(response)
            with open(mp3_file, "rb") as f:
                audio_data = f.read()
                audio_b64 = base64.b64encode(audio_data).decode()
                st.markdown(
                    f'<audio controls autoplay><source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3"></audio>',
                    unsafe_allow_html=True
                )
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Footer
st.markdown("🌍 Cognira supports all languages. Powered by OpenAI + Google Translate.")
