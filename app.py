 import streamlit as st
import openai
from deep_translator import GoogleTranslator
from langdetect import detect
from textblob import TextBlob

# Load API key from secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# App Title and Description
st.set_page_config(page_title="Cognita", layout="centered")
st.markdown("<h1 style='text-align: center;'>🧠 Cognita: Your Emotional Receptionist</h1>", unsafe_allow_html=True)
st.markdown("Welcome to a safe space. Express your thoughts in any language. Cognita will understand and respond with empathy.")

# Input from user
user_input = st.text_area("💬 What's on your mind?", height=200, placeholder="Type how you're feeling...")

# Language options
languages = GoogleTranslator.get_supported_languages(as_dict=True)
lang_choices = list(languages.keys())
target_lang = st.selectbox("🌐 Respond to me in:", lang_choices, index=lang_choices.index("english"))

# Translate user input to English for processing
if st.button("Send to Cognita"):
    if user_input.strip():
        try:
            detected_lang = detect(user_input)
            translated_input = GoogleTranslator(source='auto', target='english').translate(user_input)

            # Call OpenAI for empathetic response
            prompt = (
                f"You are an empathetic AI therapist. A user said: \"{translated_input}\" "
                "Respond with warmth and comfort."
            )
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )

            english_reply = response.choices[0].message["content"].strip()

            # Translate response back to target language
            translated_reply = GoogleTranslator(source='english', target=target_lang).translate(english_reply)

            # Display output
            st.markdown("### 🧠 Cognita says:")
            st.success(translated_reply)

        except Exception as e:
            st.error(f"Oops! Something went wrong: {e}")
    else:
        st.warning("Please share something with me so I can help.")
