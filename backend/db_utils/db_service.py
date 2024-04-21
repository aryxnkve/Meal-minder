from sqlalchemy.orm import Session
import db_utils.models as models
import db_utils.schemas as schemas
from fastapi import HTTPException
from datetime import datetime
import os
import logging
from utils import util

def create_user(db: Session, user: schemas.UserCreate):
    # if get_user_by_username(db, user.username):
    #     raise HTTPException(status_code = 404, detail = r"Username already in use!")
    db_user = models.User(username=user.username,
                          first_name=user.firstname,
                          last_name=user.lastname,
                          password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return dict(db_user)

def get_user_by_username(db: Session, username):
    result_user = db.query(models.User).filter(models.User.username == username).first()
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

def validate_access_token(db: Session, access_token):
    # access_token = user_input.access_token
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

