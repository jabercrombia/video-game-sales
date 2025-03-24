from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import allsales
from routes import platform

app = FastAPI()

app.include_router(allsales.router, prefix="/api", tags=["allsales"])
app.include_router(platform.router, prefix="/api", tags=["platform"])

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

@app.get("/api/data")
def get_data():
    return {"data": "This is data from FastAPI"}
