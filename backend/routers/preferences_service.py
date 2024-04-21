from fastapi import APIRouter
from dotenv import dotenv_values
from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from fastapi.responses import JSONResponse
import logging
import json
import db_utils.models as models

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
async def authenticate_user(user_input: schemas.UserPreferences, db: Session = Depends(get_db)):
    try:
        print("Got input", user_input)
        result = db_service.set_user_preferences(db, user_input)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
                status_code=500, detail=f"{str(e)}")
    return JSONResponse(content=result)
