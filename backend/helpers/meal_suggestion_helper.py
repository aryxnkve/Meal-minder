from sqlalchemy.orm import Session
import db_utils.models as models
import db_utils.schemas as schemas

from utils import util
from db_utils import db_service
from helpers import pinecone_helper, snowflake_helper, gemini_helper


def suggest_dish(db: Session, user_input: schemas.UserAccessToken):
    try:
        # decode token and get user id
        decoded_info = util.decode_token(user_input.access_token)
        user_id = decoded_info.get("user_id")
        print("Got user id", user_id)

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

            print("Final list of dishes", dish_names)
            print("final list of ingredients", ingredients)
            # prompt gemini to generate similar dishes
            response = gemini_helper.prompt_gemini(user_preferences.cuisine, user_preferences.dishes, dish_names, ingredients)
            
        return response
    except Exception as e:
        print("Error occurred ", str(e))
        raise Exception

