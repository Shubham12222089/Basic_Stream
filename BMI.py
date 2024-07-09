import streamlit as st

def rate_yourself():
    with st.sidebar:
        st.title('Rate YourSelf')
        languages = st.text_input("Enter the programming language you know with comma separation : ", value = 'python')
        languages = [i.strip() for i in languages.split(',')]
    st.subheader('How would you rate your experience in the following programming languages and tools? ')
    for language in languages:
        st.write(language)
        st.slider(language,min_value = 0.,max_value = 10.,step=.5)



def bmi_calulator():
    st.title("BMI Calculator")

    with st.form("BMI Calcultor"):
        col1,col2,col3 = st.columns([3,2,1])

    with col1:
        weight = st.number_input('Enter Your weight in KGs: ')

    with col2:
        height = st.number_input('Enter Your weight in Metres: ')

    with col3:
        submit = st.form_submit_button('Calculate')

    if submit:
        BMI = round((weight/(height**2)),2)
        if(BMI <= 18.5):
            st.error('Under-Weight')
        elif(BMI >= 18.5 and BMI <= 24.9):
            st.success('Healthy / Normal')
        elif(BMI >= 25 and BMI <=29.9):
            st.warning('Over-Weight')
        elif BMI >= 30:
            st.error('Obese')


choice = st.sidebar.selectbox('Menu',['BMI','Rate Yourself'])

if(choice == 'BMI'):
    bmi_calulator()
elif choice == 'Rate Yourself':
    rate_yourself()