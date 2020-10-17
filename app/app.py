import os

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette_prometheus import metrics, PrometheusMiddleware
from app.exceptions.errors import (
    BadImage,
    BadUrl,
    FileLarge,
    ManipulationError,
    NoImageFound,
    ParameterError,
    ServerTimeout,
)
from app.middleware import add_process_time_header, auth_check
from app.routes import image_routes

sentry = os.getenv("SENTRY")
sentry_sdk.init(dsn=sentry)

app = FastAPI()
asgi_app = SentryAsgiMiddleware(app)
app.add_middleware(PrometheusMiddleware)
app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)
app.include_router(image_routes.router)
app.add_middleware(BaseHTTPMiddleware, dispatch=auth_check)
app.add_route("/metrics/", metrics)


@app.exception_handler(NoImageFound)
async def no_image_found(_request: Request, _exc: NoImageFound):
    return JSONResponse(
        status_code=415, content={"message": "No image found at your destination"}
    )


@app.exception_handler(BadUrl)
async def bad_url(_request: Request, _exc: BadUrl):
    return JSONResponse(
        status_code=400, content={"message": "Your ImageUrl is badly frames"}
    )


@app.exception_handler(ParameterError)
async def param_error(_request: Request, _exc: ParameterError):
    return JSONResponse(status_code=400, content={"message": f"{str(ParameterError)}"})


@app.exception_handler(ManipulationError)
async def manipulation_error(_request: Request, _exc: ManipulationError):
    return JSONResponse(
        status_code=422,
        content={"message": "Unable to process the image due to an Error"},
    )


@app.exception_handler(FileLarge)
async def size_error(_request: Request, _exc: FileLarge):
    return JSONResponse(
        status_code=413,
        content={"message": "Image supplied was too large to be processed"},
    )


@app.exception_handler(BadImage)
async def bad_image(_request: Request, _exc: BadImage):
    return JSONResponse(
        status_code=415,
        content={"message": "File found was not of the Appropriate image type"},
    )


@app.exception_handler(ServerTimeout)
async def timeout_error(_request: Request, _exc: ServerTimeout):
    return JSONResponse(
        status_code=400,
        content={"message": "Unable to connect to image url within timeout"},
    )


@app.get("/")
async def root():
    return {"message": "Hello World"}
