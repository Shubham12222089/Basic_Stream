import streamlit as st
import pandas as pd
st.subheader("Upload the csv file")
df = st.file_uploader("upload the csv file",type = ['csv','xlsx'])

# if df is not None:
#     st.dataframe(df)

df = pd.read_csv("C:\\Users\\shubh\\OneDrive\\Desktop\\Data Science\\data_science\\Streamlit\\Products.csv")
if df is not None:
    st.table(df.head())


st.subheader("Dealing with images")
st.image("C:\\Users\\shubh\\OneDrive\\Desktop\\Data Science\\data_science\\Streamlit\\img.png")

st.subheader("Dealing with images files while uploading")
imgfile = st.file_uploader("Upload the image: ",type = ['png','jpeg'])
if(imgfile is not None):
    st.image(imgfile)



st.subheader("Working with Videos")
vdoFile = st.file_uploader("Upload the video file : ",type = ['mkv','mp4'])
if(vdoFile is not None):
    if vdoFile is not None:
        st.video(vdoFile, start_time=0)


st.subheader("Working with Audios")
adoFile = st.file_uploader("Upload the video file : ",type = ['mp3','wav'])
if(adoFile is not None):
    if adoFile is not None:
        st.audio(adoFile.read())

