import streamlit as st

st.title("Calculator App")

# Initialize session state to store the current input and result
if 'input' not in st.session_state:
    st.session_state.input = ""
if 'result' not in st.session_state:
    st.session_state.result = None

# Define calculator buttons
buttons = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', '.', '=', '+']
]

# Custom CSS for button styling
st.markdown("""
    <style>
    .stButton button {
        height: 60px;
        width: 60px;
        font-size: 24px;
        margin: 2px;
    }
    </style>
    """, unsafe_allow_html=True)

# Display current input and result
st.text_input("Input", st.session_state.input, key="input_display", disabled=True)
if st.session_state.result is not None:
    st.text_input("Result", st.session_state.result, key="result_display", disabled=True)

def update_input(value):
    if value == '=':
        try:
            st.session_state.result = eval(st.session_state.input)
        except Exception:
            st.session_state.result = "Error"
    else:
        st.session_state.input += value

# Display buttons
for row in buttons:
    cols = st.columns(len(row))
    for col, button in zip(cols, row):
        if col.button(button):
            update_input(button)
            st.experimental_rerun()  # Ensure the app reruns to reflect the button click immediately

# Clear button
if st.button("C"):
    st.session_state.input = ""
    st.session_state.result = None
    st.experimental_rerun()  # Ensure the app reruns to reflect the clear action immediately
