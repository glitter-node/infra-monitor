from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

from app.services.metrics_service import generate_metrics

router = APIRouter()


@router.get("/metrics", response_class=PlainTextResponse)
async def get_metrics() -> PlainTextResponse:
    return PlainTextResponse(
        await generate_metrics(),
        media_type="text/plain; version=0.0.4",
    )
