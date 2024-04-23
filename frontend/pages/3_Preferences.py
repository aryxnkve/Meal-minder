import streamlit as st
import numpy as np
import io
from datetime import datetime
from services import backend
import uuid
from dotenv import load_dotenv
from services.backend import set_user_preferences

load_dotenv()

st.set_page_config(
    page_title="Nutribuddy",
    page_icon="🌱",
)

# Initialization
if 'auth_token' not in st.session_state:
    st.session_state.auth_token = None

# Initialize the session state for food preferences if not already defined
if 'food_preferences' not in st.session_state:
    st.session_state.food_preferences = {
        'access_token': None,
        'is_vegetarian': False,
        'cuisine': [],
        'dishes': [],
        'ingredients': [],
        'allergies': []
    }

def authentication():
    response = backend.validate_access_token(st.session_state.auth_token)
    return response

auth_user = authentication()
# auth_user = ("sayali")

cuisine_options = ['Indian', 'American', 'Chinese', 'Italian', 'Thai', 'Korean', 'Mexican']
dish_options = ['Pizza', 'Pasta', 'Burger', 'Salad', 'Sushi', 'Tacos', 'Curry', 'Biryani', 'Soup', 'Grilled Cheese']
ingredient_options = ['Tomatoes', 'Cheese', 'Chicken', 'Beef', 'Mushrooms', 'Onions', 'Peppers', 'Garlic', 'Basil', 'Cilantro']
allergy_options = ['Nuts', 'Dairy', 'Gluten', 'Shellfish', 'Eggs', 'Soy', 'Wheat', 'Peanuts', 'Tree Nuts', 'Fish']


def get_user_preferences():
    exists, pref = backend.get_user_preferences(st.session_state.auth_token)
    if exists:
        print("Got exisitng preferences", pref)
        print(pref["is_vegetarian"])
        st.session_state.food_preferences['is_vegetarian'] = pref["is_vegetarian"]
        st.session_state.food_preferences['cuisine'] = map(str.strip, pref["cuisine"].split(',')) if (len(pref["cuisine"]) > 0) else None
        st.session_state.food_preferences['dishes'] = map(str.strip, pref["dishes"].split(',')) if (len(pref["dishes"]) > 0) else None
        st.session_state.food_preferences['ingredients'] = map(str.strip, pref["ingredients"].split(',')) if (len(pref["ingredients"]) > 0) else None
        st.session_state.food_preferences['allergies'] = map(str.strip, pref["allergies"].split(',')) if (len(pref["allergies"]) > 0) else None



# Function to display food preferences form
def display_food_preferences():
    # Checkbox for vegetarian selection
    st.session_state.food_preferences['is_vegetarian'] = st.checkbox("Are you a vegetarian?", value=st.session_state.food_preferences['is_vegetarian'])

    # Multiselect for cuisine
    st.subheader("Cuisine")
    st.session_state.food_preferences['cuisine'] = st.multiselect("Select your favorite cuisine:", options=cuisine_options, default=st.session_state.food_preferences['cuisine'])

    # Multiselect for dishes
    st.subheader("Dishes")
    st.session_state.food_preferences['dishes'] = st.multiselect("Select your favorite dishes:", options=dish_options, default=st.session_state.food_preferences['dishes'])

    # Multiselect for ingredients
    st.subheader("Ingredients")
    st.session_state.food_preferences['ingredients'] = st.multiselect("Select your favorite ingredients:", options=ingredient_options, default=st.session_state.food_preferences['ingredients'])

    # Multiselect for allergies
    st.subheader("Allergies")
    st.session_state.food_preferences['allergies'] = st.multiselect("Select your allergies (if any):", options=allergy_options, default=st.session_state.food_preferences['allergies'])

    # Submit button
    if st.button("Submit Preferences"):
        st.session_state.food_preferences['access_token'] = st.session_state.auth_token
        response = set_user_preferences(st.session_state.food_preferences)
        if response:
            st.success("Your food preferences have been saved!", icon="✅")
            # st.write(st.session_state.food_preferences)
            st.write("Vegetarian:", "Yes" if st.session_state.food_preferences['is_vegetarian'] else "No")
            st.write("Favorite Cuisines:", ', '.join(st.session_state.food_preferences['cuisine']))
            st.write("Favorite Dishes:", ', '.join(st.session_state.food_preferences['dishes']))
            st.write("Favorite Ingredients:", ', '.join(st.session_state.food_preferences['ingredients']))
            st.write("Allergies:", ', '.join(st.session_state.food_preferences['allergies']))
        else:
            st.error(f'There was an error. Details: {response[1]}', icon="🚨")
        


if auth_user[0]:
    st.title("Preferences")
    # get exisitn user pref if any
    get_user_preferences()
    # Call the function to display the form
    display_food_preferences()  



    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

else:
    st.warning('Access Denied! Please Sign In to your account.', icon="⚠️")

