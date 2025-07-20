import streamlit as st
st.set_page_config(page_title="Document Summarizer")

import os
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document
from PIL import Image
from dotenv import load_dotenv
from langdetect import detect
import easyocr
import numpy as np
from PIL import Image
import fitz 
from io import BytesIO


load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("API_KEY not found in .env file or environment variables.")
genai.configure(api_key=GOOGLE_API_KEY)

# Gemini Model Configuration (adjust as needed)
generation_config = {
  "temperature": 0.7,  # Lower temperature for more focused summaries
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
model = genai.GenerativeModel('gemini-1.5-flash-8b-001', generation_config=generation_config)

def detect_language(text):
    lang = detect(text)
    return lang

def read_image(file, lang):
    image = Image.open(file)
    image_np = np.array(image)  # Convert PIL Image to numpy array
    
    # Language groups
    latin_languages = ['en', 'fr', 'de', 'es', 'it', 'pt']
    cyrillic_languages = ['ru', 'rs_cyrillic', 'be', 'bg', 'uk', 'mn', 'en']
    ja_ko_zh_languages = ['ja', 'ko', 'zh-cn', 'zh-tw', 'en']
    
    if lang in ['ja', 'ko', 'zh-cn', 'zh-tw']:
        reader = easyocr.Reader(ja_ko_zh_languages)
    elif lang in cyrillic_languages:
        reader = easyocr.Reader(cyrillic_languages)
    else:
        reader = easyocr.Reader(latin_languages)
    
    result = reader.readtext(image_np, detail=0)
    
    text = ' '.join(result)
    return text

def extract_text_from_file(file):
    """Extracts text from various file types."""
    try:
        if file.name.endswith(".pdf"):
            text = ""
            pdf_bytes = file.read()

            if len(pdf_bytes) == 0:
                st.error("Error: Uploaded PDF file is empty.")
                return None

            try:
                # Try PyPDF2 first
                pdf_reader = PdfReader(BytesIO(pdf_bytes))
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
            except Exception:
                pass  # Proceed to next method if PyPDF2 fails

            if not text:
                try:
                    # Try PyMuPDF if PyPDF2 failed or was empty
                    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                    for page in doc:
                        page_text = page.get_text("text")
                        if page_text.strip():
                            text += page_text + "\n\n"
                except Exception:
                    pass # Proceed to next method if PyMuPDF fails

            if not text:
                try:
                    # Attempt OCR using EasyOCR to extract text from images in PDF
                    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
                    for page_num in range(len(doc)):
                        page = doc.load_page(page_num)
                        pix = page.get_pixmap()
                        img_bytes = pix.tobytes("png")
                        img = Image.open(BytesIO(img_bytes))
                        lang = detect_language(read_image(BytesIO(img_bytes), 'en')) #detect language of image.
                        text += read_image(BytesIO(img_bytes), lang) + "\n\n"

                except Exception as e:
                    st.error(f"OCR Failed on PDF: {e}")
                    return None

            return text

        elif file.name.endswith(".txt"):
            text = file.read().decode("utf-8")  # Handle text encoding
            return text

        elif file.name.endswith(".docx"):
            doc = Document(file)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text

        elif file.name.endswith((".jpg", ".jpeg", ".png")):
            temp_image_text = read_image(file, 'en')  # Use English as a placeholder for detection
            detected_lang = detect_language(temp_image_text)
            text = read_image(file, detected_lang)
            return text

        else:
            st.error("Unsupported file type. Please upload a PDF, TXT, DOCX, JPG, JPEG, or PNG file.")
            return None

    except Exception as e:
        st.error(f"Error extracting text: {e}")
        return None

    
def summarize_with_gemini(text):
    """Summarizes text using the API."""
    
    # """ For Chart pargaraph """
    prompt_template = "Summarize the following text, focusing on key information and providing a concise overview:\n\n{text}"  
    
    # """ For Chart pointers """
    # prompt_template = "Summarize the following medical document in the defined order and in precise manner and in pointers wherever neccessary, Patient information and vital information to be merged, key concerns and Symptoms, medical history, Immunization history and social history to be merged, parent history, Medications, tests undergone with results:\n\n{text}"
    
    # prompt_template = "Summarize the following medical document in the statement wise manner and in pointers wherever neccessary. Patient information and vital information, key concerns and Symptoms, medical history, Immunization history and social history to be merged, parent history, Medications, tests undergone with results.\n\n{text}"
    # prompt_template = "Summarize the information under each heading:\n\n{text}"
    # prompt_template = "Summarize patient details in a readable format in pargaraph format:\n\n{text}"
    
    # """ For resume shortlisting"""
    # prompt_template = "based on the uploaded resume ; check whether the candidate is suitable for data scinece role with minimum 5 years of experience having basic experience in machine learning, deep learning, computer vision, llm etc in a short manner. Please consider all parameters and suggest if the candidate is suitable for hiring or not.:\n\n{text}"
    # prompt_template = "based on the uploaded resume ; check which candidates are suitable for data science role with minimum 5 years of experience having basic experience in machine learning, deep learning, computer vision, llm etc in a short manner. Please consider all parameters and suggest if the candidate is suitable for hiring or not.:\n\n{text}"

    if not text:
        st.error("No text provided to summarize")
        return None
    try:
        prompt = prompt_template.format(text=text)
        response = model.generate_content(prompt)
        if response.text:
            return response.text
        else:
            st.error(f" API did not generate a summary: {response}")
            return None
    except Exception as e:
        st.error(f"Error communicating with  API: {e}")
        return None

def summarize_document(file):
    """Summarizes the uploaded document."""
    text = extract_text_from_file(file)
    if text:
      return summarize_with_gemini(text)
    else:
      return None

def main():
    st.title("Document Summarizer")
    st.write("Upload a document (PDF, TXT, DOCX, JPG, JPEG, PNG) and get a summary.")

    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt", "docx", "jpg", "jpeg", "png"])

    if uploaded_file is not None:
        with st.spinner("Processing..."):
            summary = summarize_document(uploaded_file)
            if summary:
                st.subheader("Summary:")
                st.write(summary)

if __name__ == "__main__":
    main()