from sqlalchemy.orm import Session
import db_utils.models as models
import db_utils.schemas as schemas
from fastapi import HTTPException
from datetime import datetime
import os
import logging
from utils import util
from sqlalchemy.sql import func

def create_user(db: Session, user: schemas.UserCreate):
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code = 404, detail = r"Username already in use!")
    db_user = models.User(username=user.username,
                          first_name=user.firstname,
                          last_name=user.lastname,
                          password=user.password,
                          age=user.age,
                          gender=user.gender,
                          height=user.height,
                          weight=user.weight,
                          activity_level=user.activity_level,
                          calorie_goal=user.calorie_goal,
                          bmi=user.bmi)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return dict(db_user)

def get_user_by_username(db: Session, username):
    result_user = db.query(models.User).filter(models.User.username == username).first()
    print("FOUND IN DB", result_user)
    return result_user

def get_user_by_userid(db: Session, user_id):
    result_user = db.query(models.User).filter(models.User.id == user_id).first()
    print("FOUND IN DB", result_user)
    return result_user

def authenticate_user(db: Session, credentials: schemas.UserAuthentication):
    result_user = db.query(models.User).filter(models.User.username == credentials.username).first()
    if not result_user: # username doesn't exists
        raise HTTPException(status_code = 403, detail = r"Forbidden! Please check your username and password")
    if result_user.check_password(credentials.password):
        return {"auth_token": generate_jwt_token(credentials.username, credentials.password, result_user.id)}
    else:
        raise HTTPException(status_code = 403, detail = r"Forbidden! Please check your username and password")
    
def generate_jwt_token(username, password, user_id):
    if not (username and password):
        raise HTTPException(
            status_code=404, detail=r"Username and password cannot be empty")
    data_to_encode = {
        "username": username,
        "password": util.get_hashed_password(password).decode('utf-8'),
        "user_id": user_id
    }
    access_token = util.create_access_token(data_to_encode)
    return access_token

def validate_access_token(db: Session, user_input: schemas.UserAccessToken):
    access_token = user_input.access_token
    if not access_token:
        raise HTTPException("No access token found!")
    decoded_data = util.decode_token(access_token)
    util.compare_time(decoded_data["exp"])
    username = decoded_data["username"]
    hashed_password = decoded_data["password"]
    result_user = db.query(models.User).filter(
            models.User.username == username and
            models.User.hashed_password == hashed_password).first()
    if not result_user:
        raise HTTPException("Invalid access token!")
    return {"username": result_user.username,
            "name": result_user.first_name + " " + result_user.last_name
            }

def get_pref_by_userid(db: Session, user_id):
    result_user = db.query(models.Preferences).filter(models.Preferences.user_id == user_id)
    if result_user.first():
        print("FOUND IN DB", result_user.first())
        return result_user
    else:
        return None

def set_user_preferences(db: Session, user_input: schemas.UserPreferences):
    try:
        # decode token and get user id
        decoded_info = util.decode_token(user_input.access_token)
        user_id = decoded_info.get("user_id")
        print("Got user id", user_id)

        # create model
        db_pref = models.Preferences( user_id=user_id,
                                     cuisine = user_input.cuisine,
                                    dishes=user_input.dishes,
                                    is_vegetarian=user_input.is_vegetarian,
                                    ingredients=user_input.ingredients,
                                    allergies=user_input.allergies
                                    )

        #check if preferences already in db
        existing_pref = get_pref_by_userid(db, user_id)
        if existing_pref:
            # update
            pref = existing_pref.first()
            pref = dict(pref)
            db_pref.set_preference_id(pref["preference_id"])
            print(dict(db_pref))
            existing_pref.update(dict(db_pref), synchronize_session = False)
            print("Updated exisiting preference")
            db.commit()
        else:
            db.add(db_pref)
            print("Added preference")
            db.commit()
            db.refresh(db_pref)
        return True
    except Exception as e:
        print("Error occurred ", str(e))
        raise Exception


def get_total_cal_by_userid(db: Session, user_id):
    result_user = db.query(func.count(models.WeeklyCalories.calories).filter(models.WeeklyCalories.user_id == user_id))
    print(result_user)
    if result_user.first():
        print("FOUND IN DB", result_user.first())
        return result_user.first()[0]
    else:
        return None

