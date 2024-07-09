import streamlit as st

# Title of the web app
st.header("Connect with me")

# Image and Introduction
col1, col2 = st.columns(2)
with col2:
    st.image("C:\\Users\\shubh\\OneDrive\\Pictures\\IMG_20220501_231601_598.jpg", width=170)
with col1:
    st.text("Hello! I'm Shubham, a B.Tech CSE \nstudent at Lovely Professional University, \npassionate about the intersection of \ntechnology, social good, and sports.")

st.text('Tell me about yourself: ')
name = st.text_input("Enter Your Name: ")
if name:
    st.write(f"Hello {name}, nice to meet you.")
profession = st.selectbox("Tell me about your Profession", ['Engineer', 'Doctor', 'Student', 'Civil Servant'])
st.slider("Slide this to your current age: ",1,25,1)
if profession:
    st.write(f"Great!! You're a {profession}.")

# Displaying the social media links
st.subheader("You can connect with me using these links.")
social_media = {
    "LinkedIn": "https://www.linkedin.com/in/shubhamjha3039/",
    "GitHub": "https://github.com/Shubham12222089",
    "Facebook": "https://www.facebook.com/shubhamjha.jha.566",
    # Add more social media links here
}

for platform, link in social_media.items():
    st.button(f"[{platform}]({link})")

# Optionally, add some contact information
st.write("Feel free to reach out to me on any of these platforms!")
