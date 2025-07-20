import streamlit as st

st.set_page_config(page_title="Dashboard Generator")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from dotenv import load_dotenv
import google.generativeai as genai
from io import BytesIO

# Load Gemini API Key from .env
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env file or environment variables.")
genai.configure(api_key=GOOGLE_API_KEY)

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

# model = genai.GenerativeModel('gemini-1.5-flash-002', generation_config=generation_config)
model = genai.GenerativeModel('gemini-1.5-flash-8b-001', generation_config=generation_config)


# Streamlit Page Config

st.title("📊 Dashboard Generator ")

# Upload Section
uploaded_file = st.file_uploader("📎 Upload CSV or Excel", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("✅ File uploaded successfully.")
    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    st.subheader("📊 Summary Stats")
    st.write(df.describe(include="all"))

    # Numeric columns for charts
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()

    if numeric_cols:
        col1, col2 = st.columns(2)
        with col1:
            hist_col = st.selectbox("📌 Column for Histogram", numeric_cols)
            fig1, ax1 = plt.subplots()
            sns.histplot(df[hist_col], kde=True, ax=ax1)
            st.pyplot(fig1)

        with col2:
            box_col = st.selectbox("📌 Column for Boxplot", numeric_cols, key="box")
            fig2, ax2 = plt.subplots()
            sns.boxplot(x=df[box_col], ax=ax2)
            st.pyplot(fig2)

        if len(numeric_cols) > 1:
            st.subheader("📊 Correlation Heatmap")
            fig3, ax3 = plt.subplots(figsize=(10, 5))
            sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax3)
            st.pyplot(fig3)

    # AI INSIGHTS (Gemini)
    st.subheader("🧠  AI Insights")
    if st.button("Generate Insights "):
        with st.spinner("Asking Model..."):
            summary_prompt = f"""
            Analyze the following dataset and return 5 insights, trends, or anomalies.

            Dataset Preview:
            {df.head(10).to_string()}

            Stats Summary:
            {df.describe(include='all').to_string()}
            """
            response = model.generate_content(summary_prompt)
            st.markdown(response.text)

    # Download Button
    st.subheader("📥 Download Data")
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    st.download_button("Download CSV", buffer, "processed_data.csv", "text/csv")

else:
    st.info("Upload a file above to start building your dashboard.")
