import streamlit as st
from dotenv import load_dotenv
from services import backend
# from streamlit import switch_page

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

def user_login():
    response = backend.authenticate_user(username, password)
    return response

auth_user = authentication()

if auth_user[0]:
    st.title(f"Welcome {auth_user[1].capitalize()}!!")
    
else:
    st.title("Sign In")
    username = st.text_input('Email', "sayali@gmail.com")
    password = st.text_input('Password',"sayali123", type='password')
    if st.button("Sign In"):
        response = user_login()
        if response[0]:
            st.session_state.auth_token = response[1]
            st.success('User Logged in Successfully!', icon="✅")
            
        else:
            st.error(f'{response[1]}', icon="🚨")

# Run the app
# streamlit run main.py
