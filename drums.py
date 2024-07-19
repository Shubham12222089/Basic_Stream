import streamlit as st

st.header('Virtual Drum Kit')

def play_song(sound_file):
    st.audio(sound_file, format="audio/mp3")

drum_kit = {
    "Kick Drum": {"image": "kick_drum.jpeg", "sound": "kick_drum.mp3"},
    
    "Hi-Hat": {"image": "hi_hat.jpg", "sound": "hi_hat.mp3"},
    "Crash Cymbal": {"image": "crash_cymbal.jpeg", "sound": "crash_cymbal.mp3"},
    
    # Add more drum pieces as needed
}

for drum, files in drum_kit.items():
    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button(drum):
            play_song(files["sound"])
    with col2:
        st.image(files["image"], use_column_width=True)
