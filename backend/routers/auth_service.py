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

@router.post("/api/v1/register_user")
async def register_user(user_input: schemas.UserCreate, db: Session = Depends(get_db)):
    if not (user_input.username and
            user_input.password and
            user_input.firstname and
            user_input.lastname):
        raise HTTPException(
            status_code=404, detail=r"Username and password cannot be empty")
    try:
        result = db_service.create_user(db, user_input)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
                status_code=500, detail=f"{str(e)}")
    return JSONResponse(content=result)


@router.post("/api/v1/user/authenticate")
async def authenticate_user(user_input: schemas.UserAuthentication, db: Session = Depends(get_db)):
    try:
        result = db_service.authenticate_user(db, user_input)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
                status_code=500, detail=f"{str(e)}")
    return JSONResponse(content=result)

@router.get("/api/v1/user/access_token")
async def validate_access_token(user_input: str, db: Session = Depends(get_db)):
    try:
        result = db_service.validate_access_token(db, user_input)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
                status_code=500, detail=f"{str(e)}")
    return JSONResponse(content=result)
