# AI Receptionist for Mental Health – Streamlit App with Voice Input

import streamlit as st
import openai
from textblob import TextBlob
import speech_recognition as sr
import tempfile
import os

# Load OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="AI Emotional Receptionist", layout="centered")
st.title("🧠 AI Emotional Receptionist")
st.markdown("""
This is a safe space. You don't need to log in. Just speak or write.
If it seems like you could benefit from speaking with a real therapist, please do.
""")

# Text input
user_input = st.text_area("What's on your mind?", height=200)

st.markdown("---")
st.subheader("🎤 Or Speak Your Thoughts")

# File uploader for voice
uploaded_file = st.file_uploader("Upload a short voice message (WAV only)", type=["wav"])

if uploaded_file is not None:
    recognizer = sr.Recognizer()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name
    with sr.AudioFile(tmp_path) as source:
        audio = recognizer.record(source)
        try:
            voice_text = recognizer.recognize_google(audio)
            st.success("Voice transcription: " + voice_text)
            user_input = voice_text
        except sr.UnknownValueError:
            st.error("Could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"Could not request results; {e}")

# Process input text
if user_input:
    st.markdown("### 📝 Sentiment Analysis")
    sentiment = TextBlob(user_input).sentiment
    st.write(f"Polarity: `{sentiment.polarity}` — Subjectivity: `{sentiment.subjectivity}`")

    st.markdown("### 💬 AI Reflection")
    prompt = f"User said: '{user_input}'. How might an empathetic assistant respond?"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    st.info(response.choices[0].message.content)
from langdetect import detect
from googletrans import Translator

translator = Translator()

# Detect user language
user_lang = detect(user_input)

# Translate to English if needed
if user_lang != 'en':
    translated_input = translator.translate(user_input, dest='en').text
else:
    translated_input = user_input

# Send to OpenAI
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": translated_input}
    ]
)

# Translate back if needed
reply = response['choices'][0]['message']['content']
if user_lang != 'en':
    reply = translator.translate(reply, dest=user_lang).text

st.markdown(f"**Cognita says:** {reply}")
