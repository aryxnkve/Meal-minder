from fastapi import APIRouter
from dotenv import dotenv_values
import time
import logging

from fastapi import FastAPI, HTTPException, Query
import requests

from typing import List, Any

router = APIRouter()
config = dotenv_values(".env")




@router.post("/inference/")
async def execute_query():
    print('in hugging face service')
    pass