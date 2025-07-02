import streamlit as st
import openai
from deep_translator import GoogleTranslator
from langdetect import detect
from textblob import TextBlob
from gtts import gTTS
import os
import tempfile
import base64
import torch
from transformers import pipeline

# Set OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Emotion detection model
emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=1)

# UI Configuration
st.set_page_config(page_title="Cognira", layout="centered")
st.markdown("<h1 style='text-align: center; color: pink;'>🧠 Cognira</h1>", unsafe_allow_html=True)
st.markdown("Share your feelings in any language. Cognira will understand and respond with empathy.")

# Text Input
user_input = st.text_area("💬 What's on your mind?", placeholder="Type here...", height=150)

# Submit Button
if st.button("🧠 Submit"):
    if not user_input.strip():
        st.warning("Please type something first.")
    else:
        # Language detection and translation
        lang = detect(user_input)
        if lang != "en":
            translated = GoogleTranslator(source='auto', target='en').translate(user_input)
        else:
            translated = user_input
        st.markdown(f"**Translated to English:** *{translated}*")

        # Emotion detection
        emotion = emotion_classifier(translated)[0][0]["label"]
        st.markdown(f"**Detected Emotion:** _{emotion}_")

        try:
            # OpenAI Chat (GPT-3.5)
            response = openai.ChatCompletion.create(
