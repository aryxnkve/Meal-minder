from pydantic import BaseModel
from datetime import datetime, date
from fastapi import UploadFile, File


class UserCreate(BaseModel):
    username: str
    password: str
    firstname: str
    lastname: str

class UserAuthentication(BaseModel):
    username: str
    password: str
