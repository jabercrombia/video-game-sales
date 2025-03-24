from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from routes import allsales
from routes import platform
from routes import highestselling

app = FastAPI(
    title="Video Game API",
    description="This is the documentation for my API endpoints.",
    version="1.0.0"
)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(allsales.router, prefix="/api", tags=["allsales"])
app.include_router(platform.router, prefix="/api", tags=["platform"])
app.include_router(highestselling.router, prefix="/api", tags=["highestselling"])

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html", "r") as file:
        return file.read()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
