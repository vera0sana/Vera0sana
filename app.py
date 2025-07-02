import streamlit as st
import openai
from googletrans import Translator
from gtts import gTTS
from io import BytesIO
import base64

# 🌐 API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 🎨 Page setup
st.set_page_config(page_title="Cognira: Emotional Receptionist", page_icon="🧠", layout="centered")

# 🧠 Title
st.markdown("## 🧠 Cognira: AI Emotional Receptionist")
st.write("Share your feelings in any language. Cognira will understand and respond with empathy.")

# 🌍 Translator
translator = Translator()

def translate_to_english(text):
    result = translator.translate(text, dest='en')
    return result.text

def generate_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an empathetic emotional receptionist. Respond with warmth and care."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e}"

def speak_text(text):
    tts = gTTS(text)
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    return mp3_fp

# ✏️ Text Input Box
user_input = st.text_input("💬 What's on your mind?", placeholder="Write here...")

# ✅ Submit Button
if st.button("🧠 Submit"):
    if user_input:
        with st.spinner("Cognira is listening..."):
            # 1. Translate
            english_text = translate_to_english(user_input)
            st.markdown(f"**🔄 Translated to English:** *{english_text}*")
            
            # 2. AI Response
            reply = generate_response(english_text)
            st.success("🧠 Cognira says:")
            st.markdown(f"> {reply}")
            
            # 3. Text-to-Speech
            mp3_fp = speak_text(reply)
            st.audio(mp3_fp, format="audio/mp3")

# 🎙 Optional Voice Input Upload
st.markdown("---")
st.markdown("🎤 **Or upload a voice message (WAV only)**")
voice_file = st.file_uploader("Upload your voice file", type=["wav"])
if voice_file:
    st.audio(voice_file)
    st.info("🗣️ Voice-to-text is not yet enabled – coming soon!")
