from fastapi import APIRouter
from dotenv import dotenv_values
import time
import logging

from fastapi import FastAPI, HTTPException, Query
import requests

from pydantic import BaseModel
import snowflake.connector
from typing import List, Any

router = APIRouter()
config = dotenv_values(".env")


class QueryRequest(BaseModel):
    query: str


def execute_snowflake_query(query: str) -> List[Any]:
    # Snowflake connection parameters
    conn_params = {
        "account":config['SNOWFLAKE_ACCOUNT'],
        "user": config['SNOWFLAKE_USER'],
        "password": config['SNOWFLAKE_PASSWORD'],
        "warehouse": config['SNOWFLAKE_WAREHOUSE'],
        "database": config['SNOWFLAKE_DATABASE']
    }
    conn = snowflake.connector.connect(**conn_params)
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        # Fetch results
        result = cursor.fetchall()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.post("/execute_query/")
async def execute_query(request: QueryRequest):
    result = execute_snowflake_query(request.query)
    return {"result": result}