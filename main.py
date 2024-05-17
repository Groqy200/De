import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Excel to CSV Converter", page_icon=":excel:", layout="wide")

st.title("Excel to CSV Converter")
st.subheader("Upload your Excel file and convert it to CSV format")

uploaded_file = st.file_uploader("Upload Excel file", type="xlsx")

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file, engine="openpyxl")
        csv_file = pd.ExcelFile(uploaded_file).parse(0).to_csv(index=False)

        st.subheader("File Details")
        st.write("File Type: Excel (.xlsx)")
        st.write("File Size: {:.2f} MB".format(uploaded_file.size / (1024 * 1024)))
        st.write("Number of Rows: ", len(df.index))

        st.subheader("Download CSV File")
        st.download_button(
            label="Download CSV",
            data=csv_file,
            file_name="output.csv",
            mime="text/csv"
        )

        st.write("CSV file has been downloaded successfully.")

    except Exception as e:
        st.error("Error occurred while reading the Excel file:", e)
