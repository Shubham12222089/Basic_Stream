import streamlit as st
import cv2 as cv
import numpy as np

st.title("Edit Your Own picture : ")
image = st.file_uploader("Upload Your Image : ",type=['jpeg','jpg','png'])

if image is not None:
    
    file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
    img = cv.imdecode(file_bytes, 1)

    blue = [40,20,80]
    #blue = [20,20,30]
    bg = []
    #img = cv.imread(image)
    cols = img.shape[1]
    rows = img.shape[0]

    for i in range(rows):
        temp = []
        for j in range(cols):
            temp.append(blue)
        bg.append(temp)
    bg = np.array(bg).astype(np.uint8)

    final = cv.addWeighted(img,.5,bg,0.5,0)
    st.image(final)

