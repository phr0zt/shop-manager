from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.database import init_db
from app.routes.main import router as main_router

BASE_DIR = Path(__file__).parent.parent

app = FastAPI(title="Shop Manager")

app.mount("/static", StaticFiles(directory=BASE_DIR / "app" / "static"), name="static")
app.templates = Jinja2Templates(directory=BASE_DIR / "app" / "templates")

app.include_router(main_router)

@app.on_event("startup")
def startup():
    init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
