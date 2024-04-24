from sqlalchemy.orm import Session
import db_utils.schemas as schemas

from utils import util
from db_utils import db_service
from helpers import pinecone_helper, snowflake_helper, gemini_helper

import re

def suggest_dish(db: Session, user_input: schemas.UserAccessToken):
    try:
        # decode token and get user id
        decoded_info = util.decode_token(user_input.access_token)
        user_id = decoded_info.get("user_id")
        print("Got user id", user_id)

        # get the remaining calories for the day
        user_data = db_service.get_user_by_userid(db, user_id)
        total_calories = user_data.calorie_goal
        consumed_calories = db_service.get_total_cal_by_userid(db, user_id)
        if consumed_calories:
            calorie_limit = total_calories - consumed_calories
        else:
            calorie_limit = total_calories

        # get preferences for this user
        existing_pref = db_service.get_pref_by_userid(db, user_id)
        if existing_pref:
            user_preferences = existing_pref.first()
            print(user_preferences.dishes)
            # get most similar dishes to user preferences dishes
            id_list = pinecone_helper.get_similar_dish_ids(user_preferences.dishes)
            # print("Got these similar ids from pinecone = ", id_list)

            # get dish names from snowflake database
            dishes = snowflake_helper.get_recipe_data(','.join(id_list))
            dish_names = []
            ingredients = []
            for row in range(len(dishes)):
                dish_names.append(dishes[row][1])
                ingredients.append(dishes[row][2])
            # dish_names.append(user_preferences.dishes)
            ingredients.append(user_preferences.ingredients)

            # print("Final list of dishes", dish_names)
            # print("final list of ingredients", ingredients)

            # prompt gemini to generate similar dishes
            response = gemini_helper.prompt_gemini(calorie_limit, user_preferences.cuisine, user_preferences.dishes, dish_names, ingredients)
        else:
            print("No preferences found for this user.")
            response = gemini_helper.prompt_gemini_general(calorie_limit)
        dish_details = parse_dish_details(response)
        response_obj = {
            "response_text": response,
            "response_list": dish_details
        }
        return response_obj
    except Exception as e:
        print("Error occurred ", str(e))
        raise Exception


def parse_dish_details(response):
    # Split the response into sections for each dish using a regular expression that detects the dish name pattern
    dishes_data = re.split(r'\*\*Name:\*\* ', response)
    print(len(dishes_data))
    
    # List to hold dictionaries of each dish
    dishes = []
    
    # Iterate through each section and extract details
    for dish in dishes_data[1:]:  # Skip the first split since it will be empty
        dish_details = {}
        # print(" ----------------- parsing ", dish)
        
        # Use flexible regex to extract each component, allowing for optional asterisks
        name_match = re.search(r'(.+?)\n', dish)
        description_match = re.search(r'(?i)(?:\*\*)?\bDescription\b(?:\*\*)?:\s*(.+?)\n', dish)
        calories_match = re.search(r'(?i)(?:\*\*)?\bCalories per serving\b(?:\*\*)?:\s*([\s\S]+?)\n(?i)(?:\*\*)?\bRecipe Ingredients\b(?:\*\*)?:', dish)
        # Calories per serving:
        ingredients_match = re.search(r'(?i)(?:\*\*)?\bRecipe Ingredients\b(?:\*\*)?:\s*([\s\S]+?)\n(?i)(?:\*\*)?\bHow to Cook\b(?:\*\*)?:', dish)
        cooking_instructions_match = re.search(r'(?i)(?:\*\*)?\bHow to Cook\b(?:\*\*)?:\s*([\s\S]+)', dish)

        print(name_match)
        print(description_match.group(1))
        print(calories_match)
        print(ingredients_match)
        print(cooking_instructions_match)

        if name_match and description_match and calories_match and ingredients_match and cooking_instructions_match:
            dish_details['Name'] = name_match.group(1).replace("**", "").strip()
            dish_details['Description'] = description_match.group(1).replace("**", "").strip()
            dish_details['Calories per serving'] = calories_match.group(1).replace("**", "").strip()
            dish_details['Recipe Ingredients'] = ingredients_match.group(1).replace("**", "").strip()
            dish_details['How to Cook'] = cooking_instructions_match.group(1).replace("**", "").strip()
        else:
            print(" -------- Could not parse this entry and hence Skipping this entry :-----------")
            print(dish)
            continue  # Skip if any information is missing

        # Append the dictionary to the list
        dishes.append(dish_details)

    return dishes
 

def get_remaining_calories(db, user_id):
    user_data = db_service.get_user_by_userid(db, user_id)
    total_calories = user_data.calorie_goal
    consumed_calories = db_service.get_total_cal_by_userid(db, user_id)
    if consumed_calories:
        calorie_limit = total_calories - consumed_calories
    else:
        calorie_limit = total_calories
    return calorie_limit
