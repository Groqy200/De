# Import necessary libraries
import streamlit as st
import pandas as pd

# Function to convert file to CSV format
def convert_to_csv(file):
    df = pd.read_excel(file)
    return df.to_csv(index=False)

# Function to convert file to Excel format
def convert_to_excel(file):
    df = pd.read_csv(file)
    return df.to_excel("converted_file.xlsx", index=False)

# Main function
def main():
    # File upload
    uploaded_file = st.file_uploader("Upload a file")

    # Convert to CSV
    if st.button("Convert to CSV"):
        if uploaded_file is not None:
            csv_file = convert_to_csv(uploaded_file)
            st.download_button("Download CSV", csv_file, "converted_file.csv")

    # Convert to Excel
    if st.button("Convert to Excel"):
        if uploaded_file is not None:
            excel_file = convert_to_excel(uploaded_file)
            st.download_button("Download Excel", excel_file, "converted_file.xlsx")

if __name__ == "__main__":
    main()
