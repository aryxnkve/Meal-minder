import streamlit as st
from dotenv import load_dotenv
from services import backend

load_dotenv()

st.set_page_config(
    page_title="Nutribuddy",
    page_icon="🌱",
)

st.title("Register")

# Initialization
if 'auth_token' not in st.session_state:
    st.session_state.auth_token = None

def register_user():
    response = backend.create_user(username, password, firstname, lastname)
    return response

st.subheader("Create an Account")

firstname = st.text_input('First Name')
lastname = st.text_input('Last Name')
username = st.text_input('Email')
password = st.text_input('Password', type='password', placeholder="Password must be between 8 and 50 characters")
cnf_password = st.text_input('Confirm Password', type='password', placeholder="Password must be between 8 and 50 characters")
if password != cnf_password:
    st.error(f'Passwords do no match', icon="🚨")
    submit = False
else:
    submit = True

if st.button("Sign Up") and submit:
    response = register_user()
    if response[0]:
        st.success(f'User {response[1]} Registered Successfully!', icon="✅")
    else:
        st.error(f'There was an error. Details: {response[1]}', icon="🚨")

# Run the app
# streamlit run main.py
