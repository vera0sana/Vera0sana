
import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import detect
from textblob import TextBlob
import openai
from gtts import gTTS
import os
from io import BytesIO
import base64
import emoji
from transformers import pipeline
import speech_recognition as sr

# Set your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Load emotion classifier
emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=1)

# Function to detect emotion
def detect_emotion_advanced(text):
    try:
        result = emotion_classifier(text)[0]
        return f"{emoji.emojize(':thought_balloon:')} Emotion: {result['label']} (confidence: {round(result['score'], 2)})"
    except Exception as e:
        return f"Could not detect emotion: {e}"

# Function to convert text to speech
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    b64 = base64.b64encode(mp3_fp.read()).decode()
    audio_html = f'<audio autoplay controls><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
    st.markdown(audio_html, unsafe_allow_html=True)

# Function to get AI response
def get_openai_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are an empathetic emotional AI receptionist."},
                  {"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message['content'].strip()

# Streamlit UI
st.markdown("### ðŸ§  Cognira: AI Emotional Receptionist")
st.markdown("Share your feelings in any language. Cognira will gently respond in English with empathy.")

user_input = st.text_area("ðŸ’¬ What's on your mind?", placeholder="Type here...")

if st.button("Submit"):
    if user_input:
        try:
            lang = detect(user_input)
            translated = GoogleTranslator(source='auto', target='en').translate(user_input)
            st.markdown(f"**Translated to English:** {translated}")

            # Emotion detection
            emotion = detect_emotion_advanced(translated)
            st.markdown(emotion)

            # AI response
            response = get_openai_response(translated)
            st.markdown(f"**Cognira says:** {response}")

            # Text-to-speech
            text_to_speech(response)

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter your feelings above.")
