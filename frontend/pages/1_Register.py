import streamlit as st
from dotenv import load_dotenv
from services import backend

load_dotenv()

st.set_page_config(
    page_title="Nutribuddy",
    page_icon="🌱",
)

st.title("Welcome to Nutribuddy !")

# Initialization
if 'auth_token' not in st.session_state:
    st.session_state.auth_token = None

if 'info' not in st.session_state:
    st.session_state.info = {
        "firstname": None,
        "lastname": None,
        "username": None,
        "password": None,
        "age": 0,
        "gender": None,
        "height": 0,
        "weight": 0,
        "activity_level": None,
        "goal": None,
        "bmi": 0,
        "calorie_goal": 0
    }
    

def register_user():
    response = backend.create_user(st.session_state.info)
    return response

# st.subheader("Create an Account")


def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def calculate_bmi(height, weight):
    ht_meters = height / 100
    bmi = weight / (ht_meters ** 2)
    st.markdown(f"**Your BMI is {round(bmi, ndigits=2)}, which falls under {bmi_category(bmi)} category.**")
    st.session_state.info["bmi"] = bmi
    

def calculate_daily_calorie(sex, height, weight, age, activity_level, goal):
    # Calculate BMR
    if sex == "male":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    # Adjust BMR based on activity level
    activity_factors = {"Sedentary": 1.2, 
                        "Lightly active": 1.375, 
                        "Moderately active": 1.55, 
                        "Very active": 1.725, 
                        "Extra active": 1.9}
    calories = bmr * activity_factors[activity_level]

    # Adjust calories based on goal
    if goal == "Lose weight":
        calories -= 500  # Assuming a deficit of 500 calories for weight loss
    elif goal == "Gain weight":
        calories += 500  # Assuming a surplus of 500 calories for weight gain

    st.session_state.info["calorie_goal"] = round(calories)
    return round(calories)

def show_bmi():
    info = st.session_state.info

    suggested_daily_calorie = calculate_daily_calorie(info["gender"], 
                                                info["height"], 
                                                info["weight"], 
                                                info["age"], 
                                                info["activity_level"], 
                                                info["goal"])
    
    st.subheader(f"Your ideal daily calorie intake should be {suggested_daily_calorie}")
    calculate_bmi(info["height"], info["weight"])
    calorie_goal = st.slider('Feel free to set your calorie goal below:', 0, 2000, suggested_daily_calorie)
    st.session_state.info["calorie_goal"] = calorie_goal
    submitted = st.button("Register")
    if submitted:
        st.session_state.show_register = True


def basic_register():
    if 'info' not in st.session_state:
        st.session_state.info = None
    st.markdown("**Create an Account**")
    col1, col2 = st.columns(2)
    with col1:
        firstname = st.text_input('First Name', "Sayali")
        username = st.text_input('Email', "sayali@gmail.com")

    with col2:
        lastname = st.text_input('Last Name', "Dalvi")
        password = st.text_input('Password', value="sayali123", type='password', placeholder="Password must be between 8 and 50 characters")

    st.markdown("**Personal Information**")
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input('Age',value=26, min_value=0, max_value=100, format='%d')
        height = st.number_input('Height (cm)',value=138, min_value=0)

        goal = st.radio("What's your fitness goal?", 
                        ["Lose weight", "Maintain weight", "Gain weight"])
        
    with col2:
        gender = st.selectbox("Gender", ["Female", "Male", "Other"])
        weight = st.number_input('Weight (kgs)', value=69, min_value=0)
        activity_level = st.radio("Activity level",
                                    options=["Sedentary",
                                    "Lightly active",
                                    "Moderately active",
                                    "Very active",
                                    "Extra active"],
                                    captions=[
                                        "little or no exercise",
                                        "light exercise/sports 1-3 days/week",
                                        "moderate exercise/sports 3-5 days/week",
                                        "hard exercise/sports 6-7 days a week",
                                        "physical job & exercise 2x/day"
                                    ])
        
    ## Next
    is_next = st.button("Next")
    info = {
        "firstname": firstname,
        "lastname": lastname,
        "username": username,
        "password": password,
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight,
        "activity_level": activity_level,
        "goal": goal,
        "bmi": 0,
        "calorie_goal": 0
    }
    st.session_state.info = info
    if is_next:
        st.session_state.show_bmi = True
    


def show_register():
    info = st.session_state.info
    # st.write(info)
    response = register_user()
    if response[0]:
        st.success(f'User {response[1]} Registered Successfully!', icon="✅")
    else:
        st.error(f'There was an error. Details: {response[1]}', icon="🚨")

###########################################

# Initialize additional session states to manage visibility
if 'show_bmi' not in st.session_state:
    st.session_state.show_bmi = False
if 'show_register' not in st.session_state:
    st.session_state.show_register = False



basic_register()
if st.session_state.show_bmi:
    st.divider()
    show_bmi()

if st.session_state.show_register:
    show_register()

# Run the app
# streamlit run main.py
