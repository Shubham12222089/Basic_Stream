import streamlit as st
import time
import pandas as pd
import numpy as np
# col1,col2,col3 = st.columns(3)

# with col1:
#     st.write('image1')
# with col2:
#     st.write('image2')
# with col3:
#     st.write('image3')

# st.subheader('Working with tabs')
# imgs = pd.read_csv('imgs.csv')['img_link']
# tabs = st.tabs(['ID']*30)
# for tab in tabs:
#     img = imgs[np.random.randint(1,1000)]
#     tab.image(img)

st.subheader("Advanced display and progress options")
with st.spinner('wait for it'):
    time.sleep(5)
    st.success('Thanks for being patient')

st.subheader('Progress')
with st.empty():
    for p in range(100):
        time.sleep(.1)
        st.progress(p+1,text = 'progressing')
    st.success('Completed')
# st.balloons()
st.snow()