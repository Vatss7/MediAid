import streamlit as st
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
from gtts import gTTS
import base64
import os
import requests
from deep_translator import GoogleTranslator
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Flask Backend API URL
BACKEND_URL = "http://127.0.0.1:5000/send_alert"

# Streamlit Page Configuration
st.set_page_config(page_title="MediAid - Prescription Analysis")

# Sidebar for file upload and language selection
with st.sidebar:
    st.title("MediAid Menu")
    uploaded_file = st.file_uploader("Upload Prescription (PDF or Image)", type=["pdf", "jpg", "jpeg", "png"])
    selected_lang = st.selectbox("Select Language", ["English", "Telugu", "Hindi", "Tamil"])
    phone_number = st.text_input("Enter WhatsApp Number (with country code)", placeholder="+91XXXXXXXXXX")
    process_file_button = st.button("Process Prescription")

# App Title
st.title("MediAid - Medication Management System")
st.markdown("### Upload a prescription to receive a detailed analysis and WhatsApp alerts.")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_reader = PdfReader(pdf_file)
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

# Function to extract text from images using OCR
def extract_text_from_image(image_file):
    image = Image.open(image_file)
    return pytesseract.image_to_string(image, lang="eng+tel+hin+tam")

# Function to translate extracted text
def translate_text(text, target_lang):
    return GoogleTranslator(source="auto", target=target_lang).translate(text)

# Function to generate audio output
def generate_audio(text, lang):
    tts = gTTS(text=text, lang=lang)
    audio_file = "output.mp3"
    tts.save(audio_file)
    with open(audio_file, "rb") as audio:
        audio_base64 = base64.b64encode(audio.read()).decode()
    return f'<audio autoplay><source src="data:audio/mp3;base64,{audio_base64}" type="audio/mpeg"></audio>'

# Process the uploaded file
if process_file_button and uploaded_file:
    if not phone_number or not phone_number.startswith("+"):
        st.error("📱 Please enter a valid WhatsApp number with country code (e.g., +91XXXXXXXXXX).")
    else:
        with st.spinner("Processing..."):
            try:
                if uploaded_file.name.endswith(".pdf"):
                    extracted_text = extract_text_from_pdf(uploaded_file)
                else:
                    extracted_text = extract_text_from_image(uploaded_file)

                if extracted_text:
                    st.subheader("Extracted Prescription Text:")
                    st.write(extracted_text)

                    # Translate text if a different language is selected
                    if selected_lang != "English":
                        translated_text = translate_text(extracted_text, selected_lang[:2].lower())
                        st.subheader(f"Translated Text ({selected_lang}):")
                        st.write(translated_text)
                    else:
                        translated_text = extracted_text  # Keep original text

                    # Generate and play audio response
                    audio_html = generate_audio(translated_text, selected_lang[:2].lower())
                    st.markdown(audio_html, unsafe_allow_html=True)

                    # Send WhatsApp alert with number
                    response = requests.post(BACKEND_URL, json={
                        "prescription_text": extracted_text if selected_lang == "English" else translated_text,
                        "phone_number": phone_number
                })
                    if response.status_code == 200:
                        st.success("WhatsApp alert sent successfully!")
                    else:
                        st.error("Failed to send WhatsApp alert. Try again.")

                    # Success popup
                    st.toast("✅ Prescription processed successfully!", icon="✅")  
                    st.success("🎉 Success: The prescription was processed successfully!")

                else:
                    st.warning("⚠️ Could not extract text. Please upload a clearer file.")
                    st.toast("⚠️ Warning: Could not extract text. Try a clearer file!", icon="⚠️")  

            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.toast("❌ Error processing the file. Please try again.", icon="❌")
