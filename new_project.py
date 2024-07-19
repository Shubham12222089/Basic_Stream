import streamlit as st
from pydub import AudioSegment
import os

# Get the list of audio files
audio_files = [
    'Chahun Main Ya Naa.mp3',
    'Heeriye.mp3',
    'Samjhawan.mp3',
    'Saware (Phantom).mp3',
    'Ho Gaya Hai Tujhko To Pyar Sajna.mp3',
    'Chaleya.mp3',
    'Mujhe Neend Na Aaye.mp3',
    'Main Khiladi Tu Anari.mp3'
]

# Function to load audio file
def load_audio(file_name):
    return open(os.path.join('audio', file_name), 'rb')

# Streamlit app title
st.title("Music Player App")

tab1, tab2 = st.tabs(['Cover', 'Lyrics'])

selected_file = st.selectbox('Select From this Box', audio_files)
st.sidebar.selectbox('Choose your Favourite Artist: ',['Arijit','Sonu nigam'])
if selected_file:
    audio_data = load_audio(selected_file)
    st.audio(audio_data, format='audio/mp3')
st.balloons()