
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean
from datetime import datetime
from utils.util import get_hashed_password
import bcrypt
from sqlalchemy.orm import validates, relationship
import re
from fastapi import HTTPException
from db_utils import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True)
    enc_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    height = Column(Integer, nullable=False)
    weight = Column(Integer, nullable=False)
    activity_level = Column(String, nullable=False)
    calorie_goal = Column(Integer, nullable=False)
    bmi = Column(Float, nullable=False)

    def __init__(self, username, first_name, last_name, password, age, gender, height, weight, activity_level, calorie_goal, bmi):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.set_password(password)
        self.age = age
        self.gender = gender
        self.height = height
        self.weight = weight
        self.activity_level = activity_level
        self.calorie_goal = calorie_goal
        self.bmi = bmi

    def __iter__(self):
        for key in ["id", "first_name", "last_name", "username", "age", "gender", "height", "weight", "activity_level", "calorie_goal", "bmi"]:
            yield key, getattr(self, key)

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.enc_password.encode('utf-8'))
    
    def set_password(self, password):
        if not password:
            raise HTTPException('Password not provided')

        if not isinstance(password, str):
            raise HTTPException('password should be a string')

        if len(password) < 8 or len(password) > 50:
            raise HTTPException(status_code=500, detail=
                'Password must be between 8 and 50 characters')
        self.enc_password = get_hashed_password(password).decode('utf-8')

class WeeklyCalories(Base):
    __tablename__ = "weekly_calories"

    weekly_calories_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.now())
    dish_name = Column(String, nullable=False)
    file_link = Column(String, nullable=False, unique=True)
    calories = Column(Integer, nullable=False)

    def __init__(self, user_id, timestamp, dish_name,file_link, calories) -> None:
        self.user_id = user_id
        self.dish_name = dish_name
        self.file_link = file_link
        self.calories = calories
        self.timestamp = timestamp

    def __iter__(self):
        for key in ["weekly_calories_id", "user_id", "timestamp","dish_name", "file_link", "calories"]:
            yield key, getattr(self, key)


class Preferences(Base):
    __tablename__ = "preferences"

    preference_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    is_vegetarian = Column(Boolean)
    cuisine = Column(String)
    dishes = Column(String)
    ingredients = Column(String)
    allergies = Column(String)

    def __init__(self, user_id, is_vegetarian, cuisine, dishes, ingredients, allergies) -> None:
        self.user_id = user_id
        self.is_vegetarian = is_vegetarian
        self.cuisine = cuisine
        self.dishes = dishes
        self.ingredients = ingredients
        self.allergies = allergies

    def __iter__(self):
        for key in ["preference_id", "user_id", "is_vegetarian","cuisine", "dishes", "ingredients", "allergies"]:
            yield key, getattr(self, key)
    
    def set_preference_id(self, id):
        self.preference_id = id
