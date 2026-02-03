import streamlit as st

# Page configuration
st.set_page_config(page_title="Confidential Art", layout="centered")

# Disable download, right-click, and text selection
st.markdown("""
    <style>
        img {
            pointer-events: none;
            user-select: none;
        }
        .no-download::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            height: 100%;
            width: 100%;
            z-index: 10;
        }
    </style>
    <script>
        document.addEventListener('contextmenu', event => event.preventDefault());
    </script>
""", unsafe_allow_html=True)

st.title("🎨 My Confidential Art Gallery")

# Use your image here
image_url = "https://drive.google.com/uc?export=view&id=1CFeW74cMO09hiA0jF6_h6oFFBlm_bJC9"

# Display image with download protection
st.markdown(f"""
<div class="no-download" style="position:relative; display:flex; justify-content:center;">
    <img src="{image_url}" width="600">
</div>
""", unsafe_allow_html=True)
