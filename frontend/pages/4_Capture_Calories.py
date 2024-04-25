import streamlit as st
import numpy as np
import io
from datetime import datetime
from services import backend
import uuid
from dotenv import load_dotenv
import requests
import os as os
from PIL import Image
import re

load_dotenv()

st.set_page_config(
    page_title="Nutribuddy",
    page_icon="🌱",
)

# Initialization
if 'auth_token' not in st.session_state:
    st.session_state.auth_token = None

if 'capture_pressed' not in st.session_state:
    st.session_state.capture_pressed = False

if 'calorie_response' not in st.session_state:
    st.session_state.calorie_response = None


def authentication():
    response = backend.validate_access_token(st.session_state.auth_token)
    return response

auth_user = authentication()

def extract_name(api_response):
    # Split the response text into lines
    calories_info = api_response.get("response", "")
    t = calories_info.split('**')
    return t[2]

def extract_calories(api_response):
    calories_info = api_response.get("response", "")
    calories_info = calories_info.replace('**','')

    calories_info = calories_info.replace('//n','')
    match = re.search(r"Total Calories:\s*(\d+)\s*calories", calories_info)
    return int(match.group(1)) if match else 996


def upload_page():
    uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'png'])

    if uploaded_file is not None:
        # Display the uploaded image
        image = backend.resize_image(uploaded_file)
        st.image(image, caption='Uploaded Image.')

        calorie , dish_name = "",""
        if st.button("Capture Calories"):
            with st.spinner("Calculating calories ... "):
                status, response2 = backend.get_calorie(uploaded_file.getvalue())

            st.session_state.capture_pressed = True
            if status:
                st.session_state.calorie_response = response2

        if  st.session_state.calorie_response and st.session_state.capture_pressed:
            st.subheader("Caloric Details :")
            st.markdown(st.session_state.calorie_response['response'.replace('\\n','\n')], unsafe_allow_html=True)

            if st.session_state.capture_pressed:
                st.divider()
                st.write("Feel free to edit the details below:")
                final_dish_name =st.text_input("Name of the dish", value=f"{extract_name(st.session_state.calorie_response)}") 
                final_calories = st.text_input("Enter Calories", value=f"{extract_calories(st.session_state.calorie_response)}")

                if st.button("Confirm"):
                    print("Clicked confirm")

                    with st.spinner("Recording your calories ..."):
                        file_link = ''
                        if uploaded_file:
                            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                            file_name = f"{timestamp}_{str(uuid.uuid4())}.png"
                            # upload to gcp
                            file_link = backend.upload_image_to_gcs(uploaded_file, file_name)
                            print("GCP file link = ",file_link)
                        status2 = backend.insert_calories(st.session_state.auth_token ,final_dish_name, final_calories, file_link )
                    
                    if status2: 
                        st.success('Captured your Calories!', icon="🎉")
                    else:
                        st.error('Somthing went wrong. Please try again', icon="🚨")
    
            
def insert_page():
    st.write("What did you have today?")
    final_dish_name =st.text_input("Name of the dish") 
    final_calories = st.text_input("Enter Calories")

    if st.button("Confirm Insert"):
        with st.spinner("Recording your calories ..."):
            status2 = backend.insert_calories(st.session_state.auth_token ,final_dish_name, final_calories, '' )
        if status2: 
            st.success('Captured your Calories!', icon="🎉")
        else:
            st.error('Somthing went wrong. Please try again', icon="🚨")            

if auth_user[0]:
    st.title("Capture Calories")
    # implement here
    tab1, tab2 = st.tabs(["Upload", "Insert"])
    with tab1:
        upload_page()
    with tab2:
        insert_page()
   
else:
    st.warning('Access Denied! Please Sign In to your account.', icon="⚠️")
