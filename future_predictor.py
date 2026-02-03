import streamlit as st
import time
import datetime

st.set_page_config(page_title="Future Predictor", page_icon="🔮", layout="centered")

st.title("Future Predictor 🔮")

st.markdown("Enter your details below to know your future!")

name = st.text_input("Enter your name:")
dob = st.date_input("Enter your date of birth:", min_value=datetime.date(1950, 1, 1))

if st.button("Predict My Future!"):
    if name and dob:
        prediction_placeholder = st.empty()
        animation_emojis = ["🔮", "✨", "⏳", "📜", "💫"]
        for i in range(10):
            prediction_placeholder.markdown(f"<h1 style='text-align: center;'>Predicting your future... {animation_emojis[i % len(animation_emojis)]}</h1>", unsafe_allow_html=True)
            time.sleep(0.3)
        prediction_placeholder.empty()
        
        st.success("Future Predicted!")
        
        st.balloons()
        
        st.markdown("### Here is your future:")
        
        # --- VIDEO FROM YOUR DEVICE ---
        # 1. Make sure your video file (e.g., "meme.mp4") is in the same folder as this script.
        # 2. Uncomment the line below and make sure the filename matches your video.
        st.video("C:\\Users\\shubh\\OneDrive\\Desktop\\streamlit\\duniya_khatam.mp4",autoplay=True)
        
        st.markdown("##### 2026 me duniya khatam hai 😂")

    else:
        st.warning("Please enter your name and date of birth.")
