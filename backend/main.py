from fastapi import FastAPI
from routers import auth_service
from routers import hf_service
from routers import preferences_service
from routers import meal_suggestion_service
from routers import weekly_report_service


from db_utils import models, engine 


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(hf_service.router)
app.include_router(auth_service.router)
app.include_router(preferences_service.router)
app.include_router(meal_suggestion_service.router)
app.include_router(weekly_report_service.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

