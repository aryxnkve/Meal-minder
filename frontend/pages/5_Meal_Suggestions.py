import streamlit as st
import numpy as np
import io
from datetime import datetime
from services import backend
import uuid
from dotenv import load_dotenv
from streamlit_extras.sandbox import sandbox


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

if 'dish_names' not in st.session_state:
    st.session_state.dish_names = None

if 'description' not in st.session_state:
    st.session_state.description = None

if 'dishes' not in st.session_state:
    st.session_state.dishes = None

def authentication():
    response = backend.validate_access_token(st.session_state.auth_token)
    return response

auth_user = authentication()

def get_dishes():
    status, response = backend.get_suggested_dishes(st.session_state.auth_token)
    if status:
        # print(response)
        st.session_state.dishes = response["response_list"]
        dish_names = []
        description = []
        for dish in response["response_list"]:
            dish_names.append(dish["Name"])
            description.append(dish["Description"])
        st.session_state.dish_names = dish_names
        st.session_state.description = description
        return dish_names, description
    else:
        print("Some error occurred", response)
        return None
    
def get_remaining_calories():
    status, response = backend.get_remaining_calories(st.session_state.auth_token)
    if status:
        return response
    else:
        print("Some error occurred", response)
        return 0
    
def set_stage(stage):
    if stage == 'suggest_dish_start':
        st.session_state.history += "  \n                                         💬 Yes please!  \n  \n"
    if stage == 'get_method':
        st.session_state.history += "  \n                                            💬 Looks Yummy!  \n  \n"
    if stage == 'end_convo':
        st.session_state.history += "  \n                                         💬 I'll order for myself.  \n  \n"
    if stage == 'show_recipe':
        st.session_state.history += f"👨🏻‍🍳 Based on your preferences, here are some dishes that you might like.  \n"
        st.session_state.history += f"  \n                                         💬 {st.session_state.selected_dish}  \n  \n"
    if stage == 'reset':
        st.session_state.history = "👨🏻‍🍳 Welcome! Need some suggestions for your next meal?  \n"
    st.session_state.stage = stage
    
if 'stage' not in st.session_state:
    st.session_state.stage = 'start'

print(st.session_state.stage)

if auth_user[0]:
    container = st.container()
    container.title("🥗 Meal Suggestions")

    remaining_calories = get_remaining_calories()
    container.markdown(f'**You are still left with {remaining_calories} calories for the day!**')

    convo_container = st.container()
    convo_container.markdown(st.session_state.history)
    
    # Start of conversation
    if st.session_state.stage == 'start' or st.session_state.stage == 'reset':
        st.button("Yes please!", on_click=set_stage, args=('suggest_dish_start',))
        print(st.session_state.stage)

    if st.session_state.stage == 'suggest_dish' or st.session_state.stage == 'suggest_dish_start' or st.session_state.stage == 'suggest_dish_radio':
        
        if st.session_state.stage != 'suggest_dish_radio':
        # call api
            with st.spinner("🍲 Cooking up some best dishes for you ..."):
                (dish_names, description) = get_dishes()
            if not dish_names:
                with st.spinner("🍲 Hang in tight ..."):
                    (dish_names, description) = get_dishes()

        if st.session_state.dish_names:
            question = f"👨🏻‍🍳 Based on your preferences, here are some dishes that you might like.  \n"
            st.markdown(question)
            select = "Select a dish to see the recipe."
            st.session_state.selected_dish = st.radio(select, options=st.session_state.dish_names, captions=st.session_state.description)
            st.session_state.stage = 'suggest_dish_radio'

        if st.session_state.stage != 'suggest_dish_radio':
            st.session_state.history += question

        col1, col2 = st.columns(2)
        with col1:
            st.button("Suggest something else", on_click=set_stage, args=('suggest_dish',))
        with col2:
            st.button("Show recipe", on_click=set_stage, args=('show_recipe',))

    if st.session_state.stage == 'show_recipe':
        question = f"👨🏻‍🍳 Great! Below is the recipe:  \n  \n"
        all_dishes = st.session_state.dishes
        for dish in all_dishes:
            if dish["Name"] == st.session_state.selected_dish:
                question += f'**Name:** {dish["Name"]}  \n  \n'
                question += f'**Description:** {dish["Description"]}  \n  \n'
                question += f'**Calories per serving:** {dish["Calories per serving"]}  \n  \n'
                question += f'**Recipe Ingredients:** {dish["Recipe Ingredients"]}  \n  \n'
                question += f'**How to Cook:** {dish["How to Cook"]}  \n  \n'
                question += f'📸 Have a great meal and do not forget to capture the calories!  \n  \n'
                break
        convo_container.markdown(question)
        st.session_state.history += question
        col1, col2 = st.columns(2)
        with col1:
            st.button("Suggest something else", on_click=set_stage, args=('suggest_dish',))
        with col2:
            st.button("Reset", on_click=set_stage, args=('reset',))
        
else:
    st.warning('Access Denied! Please Sign In to your account.', icon="⚠️")




