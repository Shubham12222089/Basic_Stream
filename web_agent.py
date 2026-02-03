import streamlit as st
import os
import subprocess
import speech_recognition as sr
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# ---- CONFIG ----
WORKDIR = "./workspace"
APP_FILE = os.path.join(WORKDIR, "app.py")
os.makedirs(WORKDIR, exist_ok=True)

llm=ChatGroq(groq_api_key="",model_name="llama-3.3-70b-versatile")

# ---- FUNCTIONS ----
def call_llm(prompt, code):
    
    system = "You are an expert Streamlit developer. Modify the app.py file based on user instructions. Always return the full corrected code. Whatever the user asks, you must comply. If the user asks for something that is not possible in Streamlit, politely inform them that it cannot be done. Whatever the unnecessary parts of the code, remove them. Ensure the code is functional and follows best practices. Do not include any explanations or apologies. Only return the code."
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", system),
        ("user", "User request:\n{prompt}\n\nCurrent code:\n{code}")
    ])
    chain = prompt_template | llm
    response = chain.invoke({"prompt": prompt, "code": code})
    # If response is a string, return it. If it's a Message object, get .content
    if hasattr(response, "content"):
        return response.content.strip("```python").strip("```")
    return str(response).strip("```python").strip("```")

def get_current_code():
    if not os.path.exists(APP_FILE):
        return "import streamlit as st\nst.title('My Streamlit App')"
    with open(APP_FILE, "r", encoding="utf-8") as f:
        return f.read()

def update_code(new_code):
    with open(APP_FILE, "w", encoding="utf-8") as f:
        f.write(new_code)

def run_streamlit():
    # Launch the app if not already running
    cmd = f"streamlit run {APP_FILE} --server.port=8502"
    return subprocess.Popen(cmd, shell=True)

def listen_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = r.listen(source, phrase_time_limit=5)
    try:
        text = r.recognize_google(audio)
        return text
    except Exception as e:
        return f"(Voice error: {e})"

# ---- STREAMLIT UI ----
st.set_page_config(page_title="AI Streamlit Agent", layout="wide")
st.title("AI Streamlit Builder")

col1, col2 = st.columns([2,1])

with col1:
    user_input = st.text_area("Type your request:")
    if st.button("Submit Text"):
        code = get_current_code()
        new_code = call_llm(user_input, code)
        update_code(new_code)
        st.success("App updated!")

    if st.button("🎤 Speak"):
        voice_cmd = listen_voice()
        st.write("You said:", voice_cmd)
        code = get_current_code()
        new_code = call_llm(voice_cmd, code)
        update_code(new_code)
        st.success("App updated!")

with col2:
    st.info("Your Streamlit app is running at [http://localhost:8502](http://localhost:8502)")

    if st.button("Start App"):
        run_streamlit()
