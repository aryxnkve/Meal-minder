from fastapi import APIRouter
from dotenv import dotenv_values
from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from fastapi.responses import JSONResponse
import db_utils.models as models
from fastapi import FastAPI, File, Form, UploadFile
from helpers import gemini_helper
from helpers import calorie_count_helper


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



@router.post("/api/v1/user/calorie_count")
async def calorie_count(description: str , file: UploadFile = File(...) ):
    print('in get_calorie_count')
    print(description,file)
    try:
        result = gemini_helper.vision_calorie(description, file)
        print(result)

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
                status_code=500, detail=f"{str(e)}")
    return JSONResponse(content=result)

@router.post("/api/v1/user/insert_calorie")
async def insert_calorie(user_input: schemas.WeeklyCalories, db: Session = Depends(get_db) ):
    print('in insert calorie')
    try:
        result = db_service.set_weekly_calorie(db, user_input)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
                status_code=500, detail=f"{str(e)}")
    return JSONResponse(content=result)

