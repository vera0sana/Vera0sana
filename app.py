# AI Receptionist for Mental Health - Streamlit App with Voice Input
import streamlit as st
import openai
from textblob import TextBlob
import speech_recognition as sr
import tempfile
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="AI Emotional Receptionist", layout="centered")
st.title("🧠 AI Emotional Receptionist")
st.markdown("""This is a safe space. You don't need to log in. Just share what you're feeling — by typing or speaking. 
If it seems like you could benefit from speaking with a real therapist, I'll help you connect.""")

user_input = st.text_area("What's on your mind?", height=200)

st.markdown("---")
st.subheader("🎤 Or Speak Your Thoughts")
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
            st.error(f"Speech recognition error: {e}")

system_prompt = """You are an AI emotional receptionist. You are not a therapist.
Your job is to listen gently, reflect emotions, and determine whether this user should be passed to a real human therapist.
If the user is respectful and seems to be in distress, gently validate their feelings and offer to connect them.
If the message is inappropriate or unserious, politely end the session.
Use a warm, non-judgmental, calming tone."""

def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

if st.button("Talk to Me") and user_input.strip() != "":
    with st.spinner("Thinking..."):
        sentiment_score = get_sentiment(user_input)
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )
        message = response["choices"][0]["message"]["content"]
        st.markdown("---")
        st.markdown(f"**🤖 AI Receptionist:**\n{message}")
        st.markdown(f"*Sentiment Score: {sentiment_score:.2f}* (visible only to therapist dashboard)")
        if any(word in message.lower() for word in ["connect", "therapist", "talk to someone"]):
            st.markdown("#### 🧑‍⚕️ Ready to Talk to a Real Person?\n[Click here to connect to a therapist now.](https://calendly.com/your-therapist-link)")
            st.markdown("---")
            st.markdown("### Therapist Summary")
            st.markdown(f"**User Input:** {user_input}")
            st.markdown(f"**AI Summary:** {message}")
            st.markdown(f"**Sentiment Score:** {sentiment_score:.2f}")
