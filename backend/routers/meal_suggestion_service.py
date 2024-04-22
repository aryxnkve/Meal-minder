from fastapi import APIRouter
from dotenv import dotenv_values
from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from fastapi.responses import JSONResponse
import db_utils.models as models
from helpers import meal_suggestion_helper

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

@router.post("/api/v1/user/suggest-dish")
async def suggest_dish(user_input: schemas.UserAccessToken, db: Session = Depends(get_db)):
    try:
        result = meal_suggestion_helper.suggest_dish(db, user_input)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
                status_code=500, detail=f"{str(e)}")
    return JSONResponse(content=result)

