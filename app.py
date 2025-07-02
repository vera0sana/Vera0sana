import streamlit as st
import openai
from deep_translator import GoogleTranslator
from langdetect import detect
from textblob import TextBlob
from gtts import gTTS
import os
from io import BytesIO
import base64
import tempfile
from transformers import pipeline

# Setup
openai.api_key = st.secrets["OPENAI_API_KEY"]
emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=1)

st.set_page_config(page_title="Cognira", layout="centered")
st.title("🧠 Cognira")
st.markdown("Share your feelings in any language. Cognira will understand and respond with empathy.")

# Input
user_input = st.text_input("💬 What's on your mind?")

if st.button("🧠 Submit") and user_input:
    # Detect language
    detected_lang = detect(user_input)
    
    # Translate to English
    if detected_lang != "en":
        translated = GoogleTranslator(source='auto', target='en').translate(user_input)
    else:
        translated = user_input
    st.markdown(f"**Translated to English:** *{translated}*")

    # Emotion Detection
    emotion_result = emotion_classifier(translated)[0]
    emotion = emotion_result['label']
    st.markdown(f"**Detected Emotion:** *{emotion}*")

    try:
        # OpenAI Response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an empathetic emotional AI receptionist."},
                {"role": "user", "content": f"Emotion: {emotion}. Message: {translated}"}
            ]
        )
        reply = response['choices'][0]['message']['content']
        st.markdown(f"**Cognira says:** {reply}")

        # TTS
        tts = gTTS(reply)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tts.save(tmp.name)
            audio_path = tmp.name

        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
            st.audio(audio_bytes, format='audio/mp3')

    except Exception as e:
        st.error(f"An error occurred: {e}")
