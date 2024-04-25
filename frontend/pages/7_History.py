import streamlit as st
# import numpy as np
# import io
# from datetime import datetime
# from services import backend
# import uuid
# from dotenv import load_dotenv

# load_dotenv()

# st.set_page_config(
#     page_title="Nutribuddy",
#     page_icon="🌱",
# )

# # Initialization
# if 'auth_token' not in st.session_state:
#     st.session_state.auth_token = None

# def authentication():
#     response = backend.validate_access_token(st.session_state.auth_token)
#     return response

# auth_user = authentication()

# if auth_user[0]:
#     st.title("History")
#     # implement here

#     timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

# else:
#     st.warning('Access Denied! Please Sign In to your account.', icon="⚠️")

import requests
import json

url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
headers = {
    'Content-Type': 'application/json',
    'x-app-id': 'ce9b049e',  # Replace 'YOUR_APP_ID' with your actual app ID
    'x-app-key': 'b0794a6f7cd29f8fcda92667395524d8'  # Replace 'YOUR_APP_KEY' with your actual app key
}
data = {
    "query": "2 large eggs"
}

response = requests.post(url, headers=headers, json=data)
st.markdown(json.loads(response.text))
