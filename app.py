import streamlit as st
import openai
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO

# 🔐 API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 🧠 Title
st.set_page_config(page_title="Cognira: Emotional Receptionist", page_icon="🧠", layout="centered")
st.markdown("## 🧠 Cognira: AI Emotional Receptionist")
st.write("Share your feelings in any language. Cognira will understand and gently respond in English with empathy.")

# 🌐 Translate input
def translate_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except:
        return "Translation failed."

# 💬 Generate AI reply
def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an empathetic AI assistant. Respond kindly."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

# 🔊 Convert text to speech
def speak_text(text):
    tts = gTTS(text)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    return mp3_fp

# 🧾 Input Box
user_input = st.text_input("💬 What's on your mind?", placeholder="Write here...")

# 🔘 Submit Button
if st.button("🧠 Submit"):
    if user_input:
        with st.spinner("Thinking..."):
            translated = translate_to_english(user_input)
            st.markdown(f"**Translated to English:** _{translated}_")
            reply = generate_response(translated)
            st.markdown(f"**Cognira says:** {reply}")
            st.audio(speak_text(reply), format='audio/mp3')

# 🎙️ Optional Voice Upload (future feature)
st.markdown("---")
st.markdown("🎤 Upload voice (optional, WAV only)")
voice = st.file_uploader("Upload voice input", type=["wav"])
if voice:
    st.audio(voice)
    st.warning("Voice-to-text feature coming soon.")
