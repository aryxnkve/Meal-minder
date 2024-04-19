from fastapi import APIRouter

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import httpx
from dotenv import load_dotenv
from fastapi import Query
import requests

import time
import logging
import os

from typing import List, Any

router = APIRouter()
config = load_dotenv("../config/.env")

HF_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
HF_DISH_TYPE_URL = os.getenv("HUGGINGFACE_DISH_TYPE_END_POINT")


async def query(file: bytes):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    async with httpx.AsyncClient() as client:
        response = await client.post(HF_DISH_TYPE_URL, headers=headers, content=file)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Error from Hugging Face API")

@router.post("/capture_calorie/")
async def capture_calorie(file: UploadFile = File(...)):
    try:
        print('------------------------------')
        print(HF_API_KEY,HF_DISH_TYPE_URL)
        print('------------------------------')
        file_data = await file.read()
        result = await query(file_data)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
