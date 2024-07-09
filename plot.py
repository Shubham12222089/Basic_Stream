import numpy as np
import pandas as pd
import altair as alt
import streamlit as st

st.header('Altair Scatter plot')
chart_data = pd.DataFrame(np.random.randn(500,5),columns=['a','b','c','d','e'])
chart = alt.Chart(chart_data).mark_circle().encode(x='a',y='b',size='c',tooltip = ['a','b','c',
'd','e'])
st.altair_chart(chart)

st.header('Interactive Chart')
df = pd.read_csv("C:\\Users\\shubh\\OneDrive\\Desktop\\Data Science\\data_science\\Streamlit\\lang_data.csv")
lang_list = df.columns.tolist()
lang_choices = st.multiselect("choose your Language : ", lang_list)
new_df = df[lang_choices]
st.line_chart(new_df)