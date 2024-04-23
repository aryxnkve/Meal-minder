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
    st.session_state.history = "👨🏻‍🍳 Welcome! Need some suggestions for your next meal?  \n"

def authentication():
    response = backend.validate_access_token(st.session_state.auth_token)
    return response

auth_user = authentication()

def get_dishes():
    status, response = backend.get_suggested_dishes(st.session_state.auth_token)
    if status:
        # print(response)
        return response
    else:
        print("Some error occurred", response)
        return None
    
def set_stage(stage):
    if stage == 'suggest_dish_start':
        st.session_state.history += "  \n                                         💬 Yes please!  \n  \n"
    if stage == 'suggest_dish':
        st.session_state.history += "  \n                                         💬 Suggest something else  \n  \n"
    if stage == 'get_method':
        st.session_state.history += "  \n                                         💬 Looks Yummy!  \n  \n"
    if stage == 'end_convo':
        st.session_state.history += "  \n                                         💬 I'll order for myself.  \n  \n"
    if stage == 'suggest_recipe':
        st.session_state.history += "  \n                                         💬 I'm cooking  \n  \n"
    if stage == 'reset':
        st.session_state.history = "👨🏻‍🍳 Welcome! Need some suggestions for your next meal?  \n"
    st.session_state.stage = stage
    
if 'stage' not in st.session_state:
    st.session_state.stage = 'start'

print(st.session_state.stage)

if auth_user[0]:
    container = st.container()
    container.title("🥗 Meal Suggestions")
    # implement here
    remaining_calories = 500
    container.markdown(f'**You are still left with {remaining_calories} calories for the day!**')

    convo_container = st.container()
    convo_container.markdown(st.session_state.history)
    
    # Start of conversation
    if st.session_state.stage == 'start' or st.session_state.stage == 'reset':
        # if st.session_state.stage == 'reset':
            # st.write("👨🏻‍🍳 Welcome! Need some suggestions for your next meal?")
            # st.session_state.history = "👨🏻‍🍳 Welcome! Need some suggestions for your next meal?  \n"
        st.button("Yes please!", on_click=set_stage, args=('suggest_dish_start',))
        print(st.session_state.stage)

    if st.session_state.stage == 'suggest_dish' or st.session_state.stage == 'suggest_dish_start':
        # call api
        with st.spinner("🍲 Cooking up some best dishes for you ..."):
            response = get_dishes()
        if response:
            question = f"👨🏻‍🍳 Based on your preferences, here are some dishes that you might like:  \n{response}  \n"
            st.markdown(question)
            st.session_state.history += question
            col1, col2 = st.columns(2)
            with col1:
                st.button("Suggest something else", on_click=set_stage, args=('suggest_dish',))
            with col2:
                st.button("Looks Yummy!", on_click=set_stage, args=('get_method',))
        else:
            st.error('Failed to generate suggestions. Please try again!', icon="🚨")
    
    if st.session_state.stage == 'get_method':
        question = "👨🏻‍🍳 Great! What's the plan now?  \n"
        st.write(question)
        st.session_state.history += question
        col1, col2 = st.columns(2)
        with col1:
            pressed3 = st.button("I'll order for myself.", on_click=set_stage, args=('end_convo',))
        with col2:
            pressed4 = st.button("I'm cooking", on_click=set_stage, args=('suggest_recipe',))

    if st.session_state.stage == 'end_convo':
        question = "👨🏻‍🍳 Have a great meal and don't forget to post capture your calories!  \n"
        st.write(question)
        st.session_state.history += question
        st.button("Reset", on_click=set_stage, args=('reset',))

    if st.session_state.stage == 'suggest_recipe':
        # call api
        with st.spinner("🍲 Cooking up some best dishes for you ..."):
            response = get_dishes()
        if response:
            question = f"👨🏻‍🍳 Based on your preferences, here are some dishes that you might like:  \n{response}  \n"
            st.markdown(question)
            st.session_state.history += question
            col1, col2 = st.columns(2)
            with col1:
                st.button("Suggest something else", on_click=set_stage, args=('suggest_dish',))
            with col2:
                st.button("Looks Yummy!", on_click=set_stage, args=('get_method',))
        else:
            st.error('Failed to generate suggestions. Please try again!', icon="🚨")

    
else:
    st.warning('Access Denied! Please Sign In to your account.', icon="⚠️")

# def suggest_recipe():
#     # call api

#     with st.spinner("🍲 Consulting our chef. Hang on tight ..."):
#         response = get_dishes()
#     if response:
#         question = f"Based on your preferences, here are some dishes that you might like:\n{response}"
#         st.markdown(question)
#         col1, col2 = st.columns(2)
#         with col1:
#             st.button("Suggest something else", on_click=suggest_dish)
#         with col2:
#             st.button("Looks Yummy!", on_click=get_method)
#     else:
#         st.error('Failed to generate suggestions. Please try again!', icon="🚨")
    
# def end_convo():
#     question = "Have a great meal and don't forget to post capture your calories!"
#     st.write(question)
#     st.button("Restart", on_click=start)

# def get_method():
#     question = "Great! What's the plan now?"
#     st.write(question)
#     col1, col2 = st.columns(2)
#     with col1:
#         st.button("I'll order for myself.", on_click=end_convo)
#     with col2:
#         st.button("I'm cooking", on_click=suggest_recipe)

# def suggest_dish():
#     # call api
#     with st.spinner("🍲 Cooking up some best dishes for you ..."):
#         response = get_dishes()
#     if response:
#         question = f"Based on your preferences, here are some dishes that you might like:\n{response}"
#         st.markdown(question)
#         col1, col2 = st.columns(2)
#         with col1:
#             st.button("Suggest something else", on_click=suggest_dish)
#         with col2:
#             st.button("Looks Yummy!", on_click=get_method)
#     else:
#         st.error('Failed to generate suggestions. Please try again!', icon="🚨")

# #-----------------------------------------------------------------------------------






