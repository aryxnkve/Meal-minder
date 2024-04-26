from fastapi import APIRouter
from dotenv import dotenv_values
from fastapi import HTTPException, Depends, File, UploadFile
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
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
async def calorie_count(file: UploadFile = File(...) ):
    try:
        result = calorie_count_helper.count_calories(file)
        # result = gemini_helper.vision_calorie(file)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
                status_code=500, detail=f"{str(e)}")
    return JSONResponse(content=result)

@router.post("/api/v1/user/insert_calorie")
async def insert_calorie(user_input: schemas.WeeklyCalories, db: Session = Depends(get_db) ):
    try:
        result = db_service.set_weekly_calorie(db, user_input)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
                status_code=500, detail=f"{str(e)}")
    return JSONResponse(content=result)

