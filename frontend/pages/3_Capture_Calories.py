import streamlit as st
import numpy as np
import io
from datetime import datetime
from services import backend
import uuid
from dotenv import load_dotenv
import requests

load_dotenv()

st.set_page_config(
    page_title="Nutribuddy",
    page_icon="🌱",
)

# Initialization
if 'auth_token' not in st.session_state:
    st.session_state.auth_token = None

def authentication():
    response = backend.validate_access_token(st.session_state.auth_token)
    return response

auth_user = authentication()

def upload_page():
    st.title("Upload and Send Image")
    uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'png'])
    if uploaded_file is not None:
        # Display the image
        st.image(uploaded_file)
        if st.button("Send Image"):
            # Prepare the file to send
            files = {'file': uploaded_file.getvalue()}
            # Assuming the FastAPI server runs on localhost port 8000
            response = requests.post("http://localhost:8000/upload/", files=files)
            st.write(response.json())

        if st.button("Send Image to Calorie Capture Service"):
            files = {'file': uploaded_file.getvalue()}
            response = requests.post("http://localhost:8000/capture_calorie/", files=files)
            retryIndicator = True
            retryCount = 2
            while retryIndicator and retryCount>0:
                if response.status_code == 200:
                    st.success("Image processed successfully!")
                    retryIndicator = False
                    retryCount -=1
                    # Parse and display labels from the response
                    data = response.json()
                    # Create a list to store only the labels
                    labels = [item['label'] for item in data]
                    st.write("Detected items:", labels)
                else:
                    st.error("Failed to process image.")


if auth_user[0]:
    st.title("Capture Calories")
    # implement here
    upload_page()
    
else:
    st.warning('Access Denied! Please Sign In to your account.', icon="⚠️")
