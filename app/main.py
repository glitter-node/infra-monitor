from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.metrics import router as metrics_router
from app.api.monitor import router as monitor_router
from app.services.status_service import refresh_status_cache

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@asynccontextmanager
async def lifespan(_: FastAPI):
    await refresh_status_cache()
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.include_router(monitor_router)
app.include_router(metrics_router)


@app.get("/")
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
