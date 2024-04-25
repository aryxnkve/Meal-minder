from fastapi import APIRouter
from dotenv import dotenv_values
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from helpers import weekly_report_helper

from db_utils import SessionLocal, schemas

router = APIRouter()

config = dotenv_values(".env")

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/api/v1/user/get-report-data")
async def get_report_data(user_input: schemas.UserAccessToken, db: Session = Depends(get_db)):
    try:
        #get calories
        result = weekly_report_helper.fetch_calories_by_day(db, user_input)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
                status_code=500, detail=f"{str(e)}")
    return JSONResponse(content=result)

@router.post("/api/v1/user/get-user-calorie-goal")
async def get_user_calorie_goal(user_input: schemas.UserAccessToken, db: Session = Depends(get_db)):
    try:
        #get calories
        result = weekly_report_helper.get_user_calorie_goal(db, user_input)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
                status_code=500, detail=f"{str(e)}")
    return JSONResponse(content=result)
