import streamlit as st
from streamlit_lottie import st_lottie
import requests
import time

# ----------------- Page Settings -----------------
st.set_page_config(page_title="Next Level Portfolio 🚀", page_icon="💻", layout="wide", initial_sidebar_state="collapsed")

# -------------- Helper Functions ------------------
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def animated_typing(text_list, speed=0.05):
    display = st.empty()
    while True:
        for word in text_list:
            full_text = ""
            for letter in word:
                full_text += letter
                display.markdown(f"<h1 style='color:#00FFF0; text-align:center;'>{full_text}</h1>", unsafe_allow_html=True)
                time.sleep(speed)
            time.sleep(1)
            display.empty()

# ------------- Load Lottie Animations ---------------
lottie_coding = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_tno6cg2w.json")
lottie_hello = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_qp1q7mct.json")
lottie_space = load_lottieurl("https://assets10.lottiefiles.com/private_files/lf30_jbdzjccz.json")

# -------------- Custom CSS -------------------------
st.markdown("""
    <style>
    body {
        background-color: #0f0f0f;
    }
    .main {
        background-color: #0f0f0f;
        color: #FFFFFF;
    }
    header, footer {visibility: hidden;}
    .css-1d391kg {background: linear-gradient(90deg, #000000 0%, #0f0f0f 100%);}
    </style>
""", unsafe_allow_html=True)

# --------------- Sidebar Navigation ----------------
st.sidebar.title("✨ Navigation")
nav = st.sidebar.radio("Go to", ["Home 🏠", "Projects 🚀", "Skills 🔥", "Connect 🌎"])

# --------------- Home Page -------------------------
if nav == "Home 🏠":
    col1, col2 = st.columns([2, 1])

    with col1:
        animated_typing(["Hi, I'm a Dreamer 🚀", "An ML Enthusiast 🤖", "AI Adventurer 🧠", "Creative Hacker 💻"])

    with col2:
        st_lottie(lottie_hello, height=400)

    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #FFA500;'>🚀 Welcome to my Next Level Portfolio! 🚀</h2>", unsafe_allow_html=True)
    st_lottie(lottie_space, height=300)

# --------------- Projects Page ---------------------
elif nav == "Projects 🚀":
    st.markdown("<h2 style='color:#00FFFF;'>🚀 Major Projects Showcase</h2>", unsafe_allow_html=True)

    project_info = {
        "Weather Data Collector 🌦️": "Automated city-wise weather tracking & historical trends storage.",
        "Crypto Price Tracker 💹": "Live BTC, ETH price dashboard with trend charts.",
        "News Aggregator 📰": "Daily tech & science news scraper with sentiment analysis.",
        "Stock Snapshot 📉": "Stock price tracker with intelligent alert system.",
        "Twitter Trend Tracker 🐦": "Tracks global trending hashtags with time series graphs."
    }

    for project, description in project_info.items():
        with st.expander(f"✨ {project}"):
            st.write(description)
            st.success("Demo: Coming Soon 🚀")

# --------------- Skills Page ----------------------
elif nav == "Skills 🔥":
    st.markdown("<h2 style='color:#00FFFF;'>🛠️ Skills & Superpowers</h2>", unsafe_allow_html=True)

    skill_categories = {
        "Languages & Scripting": ["Python", "SQL", "R"],
        "Data Science/ML/DL": ["Pandas", "NumPy", "Scikit-Learn", "TensorFlow", "Keras", "CNN", "RNN", "NLP", "Deep Learning"],
        "Big Data & Cloud": ["Apache Spark", "Hadoop", "Hive", "Kafka", "Databricks"],
        "Web Development": ["Streamlit", "FastAPI"],
        "MLOps & DevOps": ["Docker", "Airflow"],
        "Generative AI": ["LangChain", "GenAI", "Agentic AI", "HuggingFace", "Ollama"],
    }

    for category, items in skill_categories.items():
        st.subheader(f"🔹 {category}")
        st.markdown(", ".join(items))
        st.markdown("---")

# --------------- Contact Page ----------------------
elif nav == "Connect 🌎":
    st.markdown("<h2 style='color:#00FFFF;'>📞 Let's Connect & Collaborate!</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Reach Out 📬")
        with st.form(key="contact_form2"):
            name = st.text_input("Your Name")
            email = st.text_input("Your Email")
            message = st.text_area("Your Awesome Message")
            submit = st.form_submit_button("🚀 Send Message")
            if submit:
                st.success("Thanks for connecting! 📬 Will get back ASAP!")

    with col2:
        st.subheader("Find me here 🌍")
        st.markdown("[🔗 LinkedIn](https://linkedin.com)")
        st.markdown("[🔗 GitHub](https://github.com)")
        st.markdown("[🔗 Medium](https://medium.com)")
        st_lottie(lottie_coding, height=300)

# -------------- Footer --------------------------
st.markdown("""
    <hr style="border: 0.5px solid #00FFFF;">
    <center style="color: #00FFFF;">Made with ❤️ using Streamlit • © 2025 Your Name</center>
""", unsafe_allow_html=True)
