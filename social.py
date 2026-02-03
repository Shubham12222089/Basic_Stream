import streamlit as st

# Page configuration
st.set_page_config(page_title="Shubham Portfolio", page_icon="✨", layout="centered")

# CSS for styling
st.markdown("""
    <style>
        .container {
            text-align: center;
            padding-top: 20%;
        }

        .title {
            font-size: 3em;
            font-weight: bold;
            margin-bottom: 20px;
        }

        .button {
            font-size: 1.2em;
            padding: 10px 20px;
            border: 2px solid white;
            border-radius: 50px;
            color: white;
            text-decoration: none;
            transition: 0.3s;
        }

        .button:hover {
            background-color: white;
            color: #f37055;
        }

        .social-icons {
            margin-top: 30px;
            font-size: 2em;
        }

        .social-icons a {
            margin: 0 15px;
            text-decoration: none;
        }

        .social-icons svg {
            width: 40px;
            height: 40px;
            fill: white;
            transition: 0.3s;
        }

        .social-icons svg:hover {
            fill: #f37055;
        }

        .pink-bg {
            background-color: pink;
            transition: background-color 0.5s ease;
        }
    </style>
""", unsafe_allow_html=True)

# Create a button for surprise
if st.button("Surprise!"):
    st.markdown('<div class="pink-bg">', unsafe_allow_html=True)

# Main content
st.markdown("""
<div class="container">
    <div class="title">Shubham</div>
    <div class="button">Click Me!</div>
    <div class="social-icons">
        <a href="https://github.com" target="_blank">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.438 9.8 8.207 11.387.6.11.793-.26.793-.577v-2.16c-3.338.725-4.033-1.61-4.033-1.61-.546-1.387-1.333-1.757-1.333-1.757-1.09-.745.082-.73.082-.73 1.205.084 1.838 1.238 1.838 1.238 1.07 1.836 2.805 1.306 3.492.998.108-.775.418-1.305.76-1.605-2.665-.305-5.466-1.332-5.466-5.93 0-1.31.467-2.38 1.235-3.22-.123-.305-.535-1.53.117-3.186 0 0 1.007-.322 3.3 1.23a11.5 11.5 0 013.003-.405c1.02.005 2.045.137 3.003.405 2.29-1.552 3.295-1.23 3.295-1.23.655 1.655.243 2.88.12 3.186.77.84 1.235 1.91 1.235 3.22 0 4.61-2.805 5.625-5.475 5.92.43.37.823 1.102.823 2.222v3.293c0 .322.19.694.8.577C20.565 21.795 24 17.295 24 12c0-6.63-5.373-12-12-12z"/></svg>
        </a>
        <a href="https://twitter.com" target="_blank">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M24 4.56c-.89.39-1.84.65-2.83.77a4.92 4.92 0 002.16-2.71 9.72 9.72 0 01-3.1 1.2 4.88 4.88 0 00-8.38 4.45A13.89 13.89 0 011.67 3.15a4.88 4.88 0 001.51 6.51 4.85 4.85 0 01-2.21-.61v.06a4.88 4.88 0 003.91 4.79 4.9 4.9 0 01-2.2.08 4.88 4.88 0 004.55 3.38A9.8 9.8 0 010 20.29a13.86 13.86 0 007.56 2.21c9.06 0 14-7.5 14-14 0-.21 0-.42-.02-.63a10.08 10.08 0 002.46-2.57z"/></svg>
        </a>
        <a href="https://instagram.com" target="_blank">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M12 2.163c3.2 0 3.584.012 4.85.07 1.366.062 2.633.343 3.608 1.318.976.976 1.256 2.243 1.318 3.608.058 1.267.07 1.651.07 4.85s-.012 3.584-.07 4.85c-.062 1.366-.342 2.633-1.318 3.608-.975.976-2.242 1.256-3.608 1.318-1.267.058-1.651.07-4.85.07s-3.584-.012-4.85-.07c-1.366-.062-2.633-.342-3.608-1.318-.976-.975-1.256-2.242-1.318-3.608-.058-1.267-.07-1.651-.07-4.85s.012-3.584.07-4.85c.062-1.366.342-2.633 1.318-3.608.975-.975 2.242-1.256 3.608-1.318 1.267-.058 1.651-.07 4.85-.07zm0-2.163C8.755 0 8.333.013 7.052.07c-1.657.071-3.15.455-4.331 1.636C1.55 2.888 1.167 4.381 1.096 6.038.964 7.32.952 7.742.952 12s.013 4.678.07 5.96c.071 1.657.455 3.15 1.636 4.331 1.181 1.182 2.674 1.566 4.331 1.636 1.282.058 1.704.07 5.96.07s4.678-.013 5.96-.07c1.657-.071 3.15-.455 4.331-1.636 1.182-1.181 1.566-2.674 1.636-4.331.058-1.282.07-1.704.07-5.96s-.013-4.678-.07-5.96c-.071-1.657-.455-3.15-1.636-4.331-1.181-1.182-2.674-1.566-4.331-1.636-1.282-.058-1.704-.07-5.96-.07zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zm0 10.162a4 4 0 110-8 4 4 0 010 8zm5.974-10.91a1.488 1.488 0 100 2.977 1.488 1.488 0 000-2.977z"/></svg>
        </a>
    </div>
</div>
""", unsafe_allow_html=True)
