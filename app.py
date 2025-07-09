import streamlit as st
import pandas as pd

# Replace 'data.xlsx' with your actual Excel file name
EXCEL_FILE = 'races.csv'

st.title('Excel Data Visualization')

# Upload Excel file or use local file
uploaded_file = st.file_uploader('Upload your Excel file', type=['csv'])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
else:
    try:
        df = pd.read_excel(EXCEL_FILE)
    except FileNotFoundError:
        st.warning('No Excel file found. Please upload one.')
        st.stop()

st.subheader('Data Table')
st.dataframe(df)

# If there are at least two columns, plot a line chart
if df.shape[1] >= 2:
    st.subheader('Line Chart (First Two Columns)')
    st.line_chart(df.iloc[:, :2])
else:
    st.info('Need at least two columns for a line chart.')
