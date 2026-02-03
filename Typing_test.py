import streamlit as st
import random
import time

# Sample texts
texts = [
    "The quick brown fox jumps over the lazy dog.",
    "Streamlit is an open-source Python library.",
    "Typing tests are a great way to improve your typing skills."
]

# Initialize session state if not already done
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'text' not in st.session_state:
    st.session_state.text = random.choice(texts)

st.title("Typing Test")

# Display the text to be typed
st.write("Type the following text:")
st.write(f"**{st.session_state.text}**")

# Input field for typing
typed_text = st.text_area("Start typing here:")

# Create columns for buttons
col1, col2 = st.columns([5, 1])

# Button to start the test
with col1:
    start_test = st.button("Start Test")

# Button to finish the test
with col2:
    finish_test = st.button("Finish Test")

# Handle the start test button click
if start_test:
    st.session_state.start_time = time.time()

# Handle the finish test button click
if finish_test and st.session_state.start_time:
    end_time = time.time()
    time_taken = end_time - st.session_state.start_time

    # Calculate words per minute
    words = len(typed_text.split())
    wpm = (words / time_taken) * 60

    # Calculate the number of correct characters
    correct_chars = 0
    for i in range(min(len(st.session_state.text), len(typed_text))):
        if st.session_state.text[i] == typed_text[i]:
            correct_chars += 1

    # Calculate accuracy
    accuracy = (correct_chars / len(st.session_state.text)) * 100

    # Display the results
    st.subheader('Result')
    st.write(f"Time taken: {time_taken:.2f} seconds")
    st.write(f"Words per minute: {wpm:.2f}")
    st.write(f"Accuracy: {accuracy:.2f}%")
