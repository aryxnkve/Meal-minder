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


if 'stage' not in st.session_state:
        st.session_state.stage = 'start'
        st.session_state.history = []

# Define a function to manage the conversation flow
def manage_conversation():
    
    # Display conversation history
    st.write("Conversation History:")
    for i, (q, a) in enumerate(st.session_state.history):
        st.write(f"{i + 1}. {q} — Selected: {a}")

    # Start of conversation
    if st.session_state.stage == 'start':
        st.write("Welcome! Need some suggestions for your next meal?")
        st.session_state.history.append(("Welcome message", "Need some suggestions for your next meal?"))
        if st.button("Yes please!"):
            st.session_state.stage = 'suggest_dish'
            st.rerun()

    # Suggest recipe
    elif st.session_state.stage == 'suggest_dish':
        # call api
        with st.spinner("Fetching the best dishes for you ..."):
            response = get_dishes()
        if response:
            question = f"Based on your preferences, here are some dishes that you might like:\n{response}"
            st.markdown(question)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Suggest something else"):
                    st.session_state.history.append((question, "Suggest something else"))
                    st.session_state.stage = 'suggest_dish'
                    st.experimental_rerun()
            with col2:
                if st.button("Looks Yummy!"):
                    st.session_state.history.append((question, "Looks Yummy!"))
                    st.session_state.stage = 'get_method'
                    st.rerun()
        else:
            st.error('Failed to generate suggestions. Please try again!', icon="🚨")

    elif st.session_state.stage == 'get_method':
        question = "Great! What's the plan now?"
        st.write(question)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("I'll order for myself."):
                st.session_state.history.append((question, "I'll order for myself."))
                st.session_state.stage = 'end_convo'
                st.experimental_rerun()
        with col2:
            if st.button("I'm cooking"):
                st.session_state.history.append((question, "I'm cooking"))
                st.session_state.stage = 'suggest_recipe'
                st.experimental_rerun()
    
    elif st.session_state.stage == 'end_convo':
        question = "Have a great meal and don't forget to post capture your calories!"
        st.write(question)
        if st.button("Restart"):
            st.session_state.history.append((question, "Restart"))
            st.session_state.stage = 'start'
            st.experimental_rerun()

    elif st.session_state.stage == 'suggest_recipe':
        question = "Below are recipes for the dishes you just loved:"
        st.write(question)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Suggest something else"):
                st.session_state.history.append((question, "Suggest something else"))
                st.session_state.stage = 'suggest_dish'
                st.experimental_rerun()
        with col2:
            if st.button("Restart"):
                st.session_state.history.append((question, "Restart"))
                st.session_state.stage = 'start'
                st.experimental_rerun()
        

    

################################################################################
auth_user = ("sayali")
if auth_user[0]:
    st.title("Meal Suggestions")
    # implement here
    remaining_calories = 500
    st.markdown(f'** You are still left with {remaining_calories} calories for the day!**')
    # Call the conversation manager function
    manage_conversation()

else:
    st.warning('Access Denied! Please Sign In to your account.', icon="⚠️")


