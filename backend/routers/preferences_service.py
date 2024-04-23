from fastapi import APIRouter
from dotenv import dotenv_values
from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from fastapi.responses import JSONResponse
import logging
import json
import db_utils.models as models
from utils import util

from db_utils import SessionLocal, schemas, db_service

router = APIRouter()

config = dotenv_values(".env")

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/api/v1/user/preferences")
async def set_user_preferences(user_input: schemas.UserPreferences, db: Session = Depends(get_db)):
    try:
        print("Got input", user_input)
        result = db_service.set_user_preferences(db, user_input)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
                status_code=500, detail=f"{str(e)}")
    return JSONResponse(content=result)

@router.post("/api/v1/user/get-preferences")
async def get_user_preferences(user_input: schemas.UserAccessToken, db: Session = Depends(get_db)):
    try:
        print("Got input", user_input)
        access_token = user_input.access_token
        # decode token and get user id
        decoded_info = util.decode_token(access_token)
        user_id = decoded_info.get("user_id")
        print("Got user id", user_id)
        #check if preferences already in db
        existing_pref = db_service.get_pref_by_userid(db, user_id)
        if existing_pref:
            result = dict(existing_pref.first())
        else:
            raise HTTPException(status_code = 204, detail = r"User preferences not found")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
                status_code=500, detail=f"{str(e)}")
    return JSONResponse(content=result)
