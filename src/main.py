import logging
from time import perf_counter

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers.category import router as category_router
from src.api.routers.task import router as task_router
from src.core.logging import configure_logging

"""Создание БД"""
configure_logging()
app = FastAPI()
requesting = 0
logger = logging.getLogger("app.middleware")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_credentials=True,
)


@app.middleware("http")
async def middleware(request: Request, call_next):
    global requesting
    start_time = perf_counter()
    try:
        response: Response = await call_next(request)
    except Exception:
        duration_ms = (perf_counter() - start_time) * 1000
        logger.exception(
            "Request failed: %s %s completed_in=%.2fms",
            request.method,
            request.url.path,
            duration_ms,
        )
        raise
    requesting += 1
    duration_ms = (perf_counter() - start_time) * 1000
    response.headers["x-request-number"] = str(requesting)
    logger.info(
        "%s %s -> %s (%.2f ms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


app.include_router(router=task_router)
app.include_router(router=category_router)
