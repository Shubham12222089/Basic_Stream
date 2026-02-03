import streamlit as st

def main():
    st.sidebar.title("Portfolio Navigation")
    menu = ["Home", "Projects", "Skills", "Experience", "Contact", "Blog"]
    choice = st.sidebar.selectbox("Go to", menu)

    if choice == "Home":
        home()
    elif choice == "Projects":
        projects()
    elif choice == "Skills":
        skills()
    elif choice == "Experience":
        experience()
    elif choice == "Contact":
        contact()
    elif choice == "Blog":
        blog()

def home():
    st.title("Welcome to My Portfolio")
    #st.image("path/to/your/image.jpg", use_column_width=True)
    st.write("""
        ## Hello, I'm [Your Name]
        I'm a [Your Profession]. Welcome to my interactive portfolio.
        Here you can find details about my projects, skills, experience, and more.
    """)

def projects():
    st.title("Projects")
    #st.write("## Project 1: [Project Title](http://project-link.com)")
    st.image("path/to/project1_image.jpg", use_column_width=True)
    st.write("Description of Project 1.")

    #st.write("## Project 2: [Project Title](http://project-link.com)")
    st.image("path/to/project2_image.jpg", use_column_width=True)
    st.write("Description of Project 2.")

def skills():
    st.title("Skills")
    st.write("## Python")
    st.progress(90)

    st.write("## Data Analysis")
    st.progress(80)

    st.write("## Machine Learning")
    st.progress(70)

def experience():
    st.title("Experience")
    st.write("""
        ### [Job Title] at [Company]
        **Duration:** [Start Date] - [End Date]
        - Achieved X
        - Developed Y
        - Improved Z
    """)

def contact():
    st.title("Contact")
    with st.form(key='contact_form'):
        name = st.text_input("Name")
        email = st.text_input("Email")
        message = st.text_area("Message")
        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            st.success(f"Thank you {name}, your message has been received!")

def blog():
    st.title("Blog")
    #st.write("## Post 1: [Post Title](http://post-link.com)")
    st.write("Summary of Post 1.")

    #st.write("## Post 2: [Post Title](http://post-link.com)")
    st.write("Summary of Post 2.")

if __name__ == "__main__":
    main()
