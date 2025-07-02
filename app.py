import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import detect
from textblob import TextBlob
import openai
from gtts import gTTS
import os
import speech_recognition as sr
import torch
from transformers import pipeline

# Set OpenAI API key from environment or hardcode (NOT recommended to hardcode in production)
openai.api_key = st.secrets["openai_api_key"]

# Emotion detection model
emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=1)

# App layout
st.set_page_config(page_title="Cognira - Empathetic AI", page_icon="🧠")
st.title("🌍 Cognira")
st.subheader("Share your feelings in any language. Cognira will understand and respond with empathy.")

user_input = st.text_input("💬 What's on your mind?")
uploaded_file = st.file_uploader("🎤 Upload voice (optional, WAV only)", type=["wav"])
submit = st.button("🧠 Submit")

if submit or uploaded_file:
    if uploaded_file:
        r = sr.Recognizer()
        with sr.AudioFile(uploaded_file) as source:
            audio = r.record(source)
        try:
            user_input = r.recognize_google(audio)
            st.markdown(f"**Recognized Speech:** {user_input}")
        except:
            st.error("Could not process the uploaded audio.")

    if user_input:
        # Language detection
        lang = detect(user_input)
        translated = user_input
        if lang != 'en':
            translated = GoogleTranslator(source='auto', target='en').translate(user_input)
            st.markdown(f"**Translated to English:** *{translated}*")

        # Emotion Detection
        emotion_result = emotion_classifier(translated)[0]
        emotion = emotion_result['label']
        st.markdown(f"**Detected Emotion:** *{emotion}*")

        # OpenAI ChatGPT 3.5 call
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are an empathetic AI therapist. The user is feeling {emotion}. Respond in a warm and human-like tone."},
                    {"role": "user", "content": translated}
                ]
            )
            reply = response['choices'][0]['message']['content']
            st.markdown(f"**Cognira says:** {reply}")

            # Voice Output
            tts = gTTS(reply)
            tts.save("response.mp3")
            audio_file = open("response.mp3", "rb")
            st.audio(audio_file.read(), format="audio/mp3")
            audio_file.close()
            os.remove("response.mp3")
        except Exception as e:
            st.error(f"An error occurred: {e}")
