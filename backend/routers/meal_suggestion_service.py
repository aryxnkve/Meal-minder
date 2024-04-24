from fastapi import APIRouter
from dotenv import dotenv_values
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from helpers import meal_suggestion_helper

from db_utils import SessionLocal, schemas, db_service
from utils import util

router = APIRouter()

config = dotenv_values(".env")

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/api/v1/user/get-remaining-calories")
async def get_remaining_calories(user_input: schemas.UserAccessToken, db: Session = Depends(get_db)):
    try:
        access_token = user_input.access_token
        # decode token and get user id
        decoded_info = util.decode_token(access_token)
        user_id = decoded_info.get("user_id")
        print("Got user id", user_id)
        #get calories
        result = meal_suggestion_helper.get_remaining_calories(db, user_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
                status_code=500, detail=f"{str(e)}")
    return JSONResponse(content=result)

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

