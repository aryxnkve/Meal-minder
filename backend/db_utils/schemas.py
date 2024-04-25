from pydantic import BaseModel
from datetime import datetime, date
from fastapi import UploadFile, File


class UserCreate(BaseModel):
    username: str
    password: str
    firstname: str
    lastname: str
    age: int
    gender: str
    height: int
    weight: int
    activity_level: str
    calorie_goal: int
    bmi: float

class UserAuthentication(BaseModel):
    username: str
    password: str

class UserAccessToken(BaseModel):
    access_token: str

class UserPreferences(UserAccessToken):
    is_vegetarian: bool
    cuisine: str
    dishes: str
    ingredients: str
    allergies: str

class WeeklyCalories(UserAccessToken):
    dish_name : str
    file_link : str
    calories : str
    timestamp : datetime
