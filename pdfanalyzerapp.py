import streamlit as st
import openai
from pdfminer.high_level import extract_text
import tempfile
import os

# Function to extract text from uploaded PDF
def extract_text_from_pdf(pdf_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf_file.read())
        tmp_path = tmp_file.name
    return extract_text(tmp_path)

# Function to summarize the report using GPT-4 (latest OpenAI SDK format)
def summarize_report(text):
    client = openai.OpenAI(api_key="")
    prompt = (
        "You are a financial analyst. Summarize the following annual report. "
        "Highlight key financial metrics such as revenue, profit, net income, growth, risks, and outlook:\n\n"
        f"{text[:6000]}"  # Trim to stay under token limit
    )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return response.choices[0].message.content

# Streamlit app UI
st.title("📊 AI Financial Report Analyzer")
uploaded_pdf = st.file_uploader("Upload a Financial Report (PDF)", type="pdf")

if uploaded_pdf:
    with st.spinner("Extracting and analyzing the report..."):
        raw_text = extract_text_from_pdf(uploaded_pdf)
        summary = summarize_report(raw_text)

    st.subheader("📌 Summary:")
    st.write(summary)
