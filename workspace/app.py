
import streamlit as st

st.title('Hello Streamlit')
name = st.text_input('Please enter your name')
if st.button('Submit'):
    st.write(f'Hello, {name}!')
