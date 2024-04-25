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
    """Extract the total calories from the API response."""
    
    pattern = r"\*\*Total Calories:\*\*\s*(\d+)\s*calories"
    calories_info = api_response.get("response", "")
    calories_info = calories_info.replace('**','')

    calories_info = calories_info.replace('//n','')
    match = re.search(r"Total Calories:\s*(\d+)\s*calories", calories_info)
    return int(match.group(1)) if match else 996




def process_additional_action(calories):
    """Function to be called when the text box is clicked."""
    st.write(f"Processing with {calories} calories...")  # Placeholder function


def upload_page():
    st.title("Upload and Send Image")
    uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'png'])
    labels = ""

    if uploaded_file is not None:
        # Display the uploaded image
        image = backend.resize_image(uploaded_file)
        st.image(image, caption='Uploaded Image.')
    calorie , dish_name = "",""
    if uploaded_file is not None:
        # Display the image
        if st.button("Calorie Capture"):
            ## 
            # store image to bucket 
            ##
            # status, response1 = backend.get_calorie_type(uploaded_file)
            # if status:
            #     print(status, response1 )
            #     data = response1
            #     # Create a list to store only the labels
            #     labels = ' ,'.join([item['label'] for item in data[:3]])
            #     st.write("Detected items:", labels)
            # else:
            #     st.error("Failed to process image. Please re-upload the image -->" + response1)
            # print('part2 in calorie count')
            status, response2 = backend.get_calorie(uploaded_file.getvalue(),"labels")
            # st.write("calculated calories:", response2)

            if status:
                st.markdown(response2['response'.replace('\\n','\n')], unsafe_allow_html=True)
                calorie = extract_calories(response2)
                dish_name = extract_name(response2)
                # Create a text input for editing calorie count
        calories = st.text_input("Enter Calories", value=f"{calorie}")
        dish_name =st.text_input("Name of the dish", value=f"{dish_name}") 
        if st.button("Confirm"):
            try:
                print('2')
                print(dish_name)
                gcplink = "https://"
                print('3')
                status, response = backend.insert_calories(st.session_state.auth_token ,dish_name,calories,gcplink )
                if status: 
                    st.write('Calories successfully updated')
                else:
                    print('error')
                    st.write(response)
            except Exception as e:
                print(str(e))
            # process_confirmation(edited_calories)
            # --> storage link --> get markdown  --> parse calorie --> make calories editable  --> submit it to weekly user

            

if auth_user[0]:
    st.title("Capture Calories")
    # implement here
    upload_page()
    
else:
    st.warning('Access Denied! Please Sign In to your account.', icon="⚠️")
