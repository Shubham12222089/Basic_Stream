import streamlit as st
import pandas as pd
import numpy as np
st.subheader('Working with different kind of plots')

chart_data = pd.DataFrame(np.random.randn(20,3),columns = ['line1','line2','line3'])
st.subheader('Line chart')
st.line_chart(chart_data)

#Area Chart
st.subheader('Area chart')
st.area_chart(chart_data)

#Bar Chart
st.subheader('Bar chart')
st.bar_chart(chart_data)

import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv("C:\\Users\\shubh\\OneDrive\\Desktop\\Data Science\\data_science\\Streamlit\\iris.csv")

#multiple Graphs
st.header('Multiple Columns')
fig = plt.figure(figsize=(15,8))
col1, col2 = st.columns(2)

with col1:
    col1.header = 'KDE = False'
    fig1 = plt.figure()
    sns.distplot(df['sepal_length'], kde = False)
    st.pyplot(fig1)

with col2:
    col2.header = 'Hist = False'
    fig2 = plt.figure()
    sns.distplot(df['sepal_length'], hist = False)
    st.pyplot(fig2)



