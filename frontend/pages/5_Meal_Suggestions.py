import streamlit as st
import numpy as np
import io
from datetime import datetime
from services import backend
import uuid
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Nutribuddy",
    page_icon="🌱",
)

# Initialization
if 'auth_token' not in st.session_state:
    st.session_state.auth_token = None

if 'history' not in st.session_state:
    st.session_state.history = []


def authentication():
    response = backend.validate_access_token(st.session_state.auth_token)
    return response

auth_user = authentication()

def get_dishes():
    status, response = backend.get_suggested_dishes(st.session_state.auth_token)
    if status:
        print(response)
        return response
    else:
        print("Some error occurred", response)
        return None
    
def start():
    
    st.write("Welcome! Need some suggestions for your next meal?")
    st.session_state.history.append(("Welcome message", "Need some suggestions for your next meal?"))
    st.button("Yes please!", on_click=suggest_dish)

def suggest_recipe():
    # call api
    with st.spinner("🍲 Consulting our chef. Hang on tight ..."):
        response = get_dishes()
    if response:
        question = f"Based on your preferences, here are some dishes that you might like:\n{response}"
        st.markdown(question)
        col1, col2 = st.columns(2)
        with col1:
            st.button("Suggest something else", on_click=suggest_dish)
        with col2:
            st.button("Looks Yummy!", on_click=get_method)
    else:
        st.error('Failed to generate suggestions. Please try again!', icon="🚨")
    
def end_convo():
    question = "Have a great meal and don't forget to post capture your calories!"
    st.write(question)
    st.button("Restart", on_click=start)

def get_method():
    question = "Great! What's the plan now?"
    st.write(question)
    col1, col2 = st.columns(2)
    with col1:
        st.button("I'll order for myself.", on_click=end_convo)
    with col2:
        st.button("I'm cooking", on_click=suggest_recipe)

def suggest_dish():
    # call api
    with st.spinner("🍲 Cooking up some best dishes for you ..."):
        response = get_dishes()
    if response:
        question = f"Based on your preferences, here are some dishes that you might like:\n{response}"
        st.markdown(question)
        col1, col2 = st.columns(2)
        with col1:
            st.button("Suggest something else", on_click=suggest_dish)
        with col2:
            st.button("Looks Yummy!", on_click=get_method)
    else:
        st.error('Failed to generate suggestions. Please try again!', icon="🚨")

#-----------------------------------------------------------------------------------

if auth_user[0]:
    container = st.container()
    container.title("🥗 Meal Suggestions")
    # implement here
    remaining_calories = 500
    container.markdown(f'**You are still left with {remaining_calories} calories for the day!**')
    
    # Display conversation history
    # st.write("Conversation History:")
    # for i, (q, a) in enumerate(st.session_state.history):
    #     st.write(f"{i + 1}. {q} — Selected: {a}")

    # Start of conversation
    start()
    
else:
    st.warning('Access Denied! Please Sign In to your account.', icon="⚠️")




