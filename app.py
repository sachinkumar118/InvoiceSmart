from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure Google Generative AI with API key from environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load Gemini Pro Vision model
model = genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input_text, image_data, user_prompt):
    # Generate response using Gemini Pro Vision model
    response = model.generate_content([input_text, image_data[0], user_prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="InvoiceSmart")
st.header("InvoiceSmart")
input_prompt = st.text_input("Input Prompt:", key="input")
uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the invoice")

default_prompt = """
You are an expert in understanding invoices. We will upload an image of an invoice,
and you will provide insights based on the uploaded invoice image.
"""

# Display default input prompt if none provided
if not input_prompt:
    st.info("Provide a prompt to describe what you want to know about the invoice.")
    input_prompt = default_prompt

# Handle submit button click
if submit:
    try:
        image_data = input_image_details(uploaded_file)
        response = get_gemini_response(default_prompt, image_data, input_prompt)
        st.subheader("The Response is:")
        st.write(response)
    except FileNotFoundError as e:
        st.error(str(e))
