import streamlit as st
st.title("Hello Geeks, welcome to geeks for geeks")
st.header("Header -> GFG")
st.subheader("subheader -> GFG")
st.text("Text -> GFG")

#markdown
st.markdown('Hi')
st.markdown('##### Hi')
st.markdown('#### Hi')
st.markdown('### Hi')
st.markdown('## Hi')
st.markdown('# Hi')

#success
st.success("Data is submitted!")
st.info("Information")
st.warning("Warning!")
st.error("Error")

st.exception(ZeroDivisionError("Division by zero not possible"))
st.help(ZeroDivisionError)

st.write(range(1,10))
st.write(1+2+3)

st.code('x=10\n'
        'for i in range(x)\n'
        '\tprint(i)')


#chcek box
st.checkbox('Male')
st.checkbox('Female')

#checkbox with validation
if(st.checkbox('Adult')):
    st.write('You are an adult')

#Radio button
st.radio('select your category: ',('Male','Female','others'))

#select box
st.subheader('Select box')
selectBox = st.selectbox("Data Science : ", ['Data Analysis','Web scrapping','Machine Learning','Computer Vision','Deep Learning'])
st.write("You have selected : ",selectBox)

#multi selectbox
st.subheader('MultiSelect box')
multiSelectBox = st.multiselect("Data Science : ", ['Data Analysis','Web scrapping','Machine Learning','Computer Vision','Deep Learning'])
st.write("You have selected : ",multiSelectBox)

st.subheader('Buttons')
if(st.button('Click me')):
    st.write("Thanks for clicking me")


st.subheader('Slider')
st.slider('select the volume',1,10,step=1)

st.subheader('User Input')
name = st.text_input("Enter your name: ")
if(name):
    st.write("Hi, ",name)

password  = st.text_input("Password : ",type = 'password')

st.subheader('Text Area')
textArea = st.text_area("write about yourself in 100 words")

st.subheader('Number Input')
st.number_input("Enter your age : ",18,110)

st.subheader('Date Input')
st.date_input('Date')

st.subheader('Time input')
st.time_input('Time')