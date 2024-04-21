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
    dishes: str
    ingredients: str
    allergies: str
