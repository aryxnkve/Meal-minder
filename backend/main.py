from fastapi import FastAPI
from routers import auth_service
from routers import hf_service
from routers import preferences_service
from dotenv import dotenv_values

# from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(hf_service.router)
app.include_router(auth_service.router)
app.include_router(preferences_service.router)


# # CORS middleware setup
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.get("/")
async def root():
    return {"message": "Hello World"}


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)
