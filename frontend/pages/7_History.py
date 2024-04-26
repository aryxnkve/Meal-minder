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

import re

# Define the string containing the dish name, ingredients, calorie details, and other data
recipe_text = """
**Name:** Creamy Chicken Pasta with Broccoli

**Ingredients:**
- 8 oz. (about 2 cups) penne pasta
- 2 boneless, skinless chicken breasts cooked and shredded (Chicken can be from a rotisserie chicken, or you can pan fry/oven roast your own)
- 2 cups broccoli florets
- 1 cup heavy cream
- ½ cup grated Parmesan cheese
- 2 cloves garlic, minced
- 1 teaspoon dried Italian seasoning (or a mix of dried basil, oregano, and thyme)
- Salt and pepper, to taste

**Calories Per Ingredient:**
- 8 oz. (about 2 cups) penne pasta: 440 calories
- 2 boneless, skinless chicken breasts cooked and shredded: 280 calories
- 2 cups broccoli florets: 50 calories
- 1 cup heavy cream: 400 calories
- ½ cup grated Parmesan cheese: 200 calories
- 2 cloves garlic, minced: 10 calories
- 1 teaspoon dried Italian seasoning: 5 calories
- Salt and pepper, to taste: 0 calories

**Total Calories:** 1385 calories

**Calculation:** 
(440 calories + 280 calories + 50 calories + 400 calories + 200 calories + 10 calories + 5 calories + 0 calories) = 1385 calories
"""

# Regular expression to extract the name after "Name:**"
name = re.search(r"\*\*Name:\*\*\s*(.*?)\s*\n", recipe_text)

# Check if a match is found and print the result
if name:
    st.write("Name extracted:", name.group(1))

