import os

import sentry_sdk
from fastapi import FastAPI
from fastapi import Request
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette_prometheus import PrometheusMiddleware
from starlette_prometheus import metrics

from app.exceptions.errors import BadImage
from app.exceptions.errors import BadUrl
from app.exceptions.errors import FileLarge
from app.exceptions.errors import ManipulationError
from app.exceptions.errors import NoImageFound
from app.exceptions.errors import ParameterError
from app.exceptions.errors import RateLimit
from app.exceptions.errors import ServerTimeout
from app.exceptions.errors import Unauthorised
from app.middleware import add_process_time_header
from app.middleware import auth_check
from app.routes import image_routes

sentry = os.getenv("SENTRY")
sentry_sdk.init(dsn=sentry)

app = FastAPI(docs_url="/playground", redoc_url="/docs",root_path="/image")
asgi_app = SentryAsgiMiddleware(app)
app.add_middleware(PrometheusMiddleware)
app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)
app.include_router(image_routes.router)
app.add_middleware(BaseHTTPMiddleware, dispatch=auth_check)
app.add_route("/metrics/", metrics)


@app.exception_handler(NoImageFound)
async def no_image_found(_request: Request, _exc: NoImageFound):
    return JSONResponse(
        status_code=415,
        content={"message": "No image found at your destination"})


@app.exception_handler(BadUrl)
async def bad_url(_request: Request, _exc: BadUrl):
    return JSONResponse(status_code=400,
                        content={"message": "Your ImageUrl is badly frames"})


@app.exception_handler(ParameterError)
async def param_error(_request: Request, _exc: ParameterError):
    return JSONResponse(status_code=400,
                        content={"message": f"{str(ParameterError)}"})


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
        content={
            "message": "File found was not of the Appropriate image type"
        },
    )


@app.exception_handler(ServerTimeout)
async def timeout_error(_request: Request, _exc: ServerTimeout):
    return JSONResponse(
        status_code=400,
        content={"message": "Unable to connect to image url within timeout"},
    )


@app.exception_handler(Unauthorised)
async def unauth_error(_request: Request, exc: Unauthorised):
    return JSONResponse(
        status_code=403,
        content={"message": str(exc)},
    )


@app.exception_handler(RateLimit)
async def rate_error(_request: Request, _exc: RateLimit):
    return JSONResponse(
        status_code=429,
        content={"message": "Ratelimited"},
    )


@app.get("/")
async def root():
    return {"message": "Hello World"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Dagpi",
        version="1.0",
        description="The Number 1 Image generation api",
        routes=app.routes
    )
    openapi_schema["info"] = {
        "title": "Dagpi",
        "description": " A fast and powerful image manipulation api",
        "version": "1.0.0",
        "contact": {
            "name": "Daggy1234",
            "url": "https://dagpi.xyz",
            "email": "contact@dagpi.xyz"
        },
        "license": {
            "name": "AGPLv3",
            "url": "https://www.gnu.org/licenses/agpl-3.0.en.html"
        },
        "x-logo": {
            "url": "https://asyncdagpi.readthedocs.io/en/latest/_static/"
                   "dagpib.png"}}
    for endpoint in openapi_schema["paths"].keys():
        if not endpoint == "/":
            openapi_schema["paths"][endpoint]["get"]["parameters"].append(
                {"required": True,
                 "schema": {"title": "Authorization", "type": "string"},
                 "name": "Authorization", "in": "header"})
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
