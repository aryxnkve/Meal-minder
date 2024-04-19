from fastapi import FastAPI
from routers import airflow_service
from routers import aws_service
from routers import snowflake_service
from dotenv import dotenv_values

app = FastAPI()
config = dotenv_values(".env")
app.include_router(airflow_service.router)
app.include_router(aws_service.router)
app.include_router(snowflake_service.router)
@app.get("/")
async def root():
    return {"message": "Hello World"}
