import os
from typing import Optional
import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette_prometheus import PrometheusMiddleware, metrics

from app.exceptions.errors import (BadImage, BadUrl, FileLarge,
                                   ManipulationError, NoImageFound,
                                   ParameterError, RateLimit, ServerTimeout,
                                   Unauthorised)
from app.middleware import add_process_time_header, auth_check
from app.routes import image_routes, special_routes
from sentry_sdk import capture_exception

sentry: Optional[str] = os.getenv("SENTRY")
sentry_sdk.init(dsn=sentry,
                release="dagpi-image@1.3.0",
                traces_sample_rate=0.5)
app: FastAPI = FastAPI(docs_url=None, redoc_url=None)
asgi_app: SentryAsgiMiddleware = SentryAsgiMiddleware(app)
app.add_middleware(PrometheusMiddleware)
app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)
app.include_router(image_routes.router)
app.include_router(special_routes.router)
# app.add_middleware(BaseHTTPMiddleware, dispatch=auth_check)
app.add_route("/metrics/", metrics)


@app.get("/playground", include_in_schema=False)
def overridden_swagger():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="Dagpi Playground",
        swagger_favicon_url="https://cdn.dagpi.xyz/dagpib.png")


@app.get("/docs", include_in_schema=False)
def overridden_redoc():
    return get_redoc_html(openapi_url="/openapi.json",
                          title="Dagpi Image Docs",
                          redoc_favicon_url="https://cdn.dagpi.xyz/dagpib.png")


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
async def param_error(_request: Request, exc: ParameterError):
    return JSONResponse(status_code=400, content={"message": f"{str(exc)}"})


@app.exception_handler(ManipulationError)
async def manipulation_error(_request: Request, exc: ManipulationError):
    return JSONResponse(
        status_code=422,
        content={"message": f"Unable to manipulate image: {str(exc)}"},
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


@app.exception_handler(500)
async def internal_server_error(req, exc):
    e_str = str(exc)
    capture_exception(exc)
    return JSONResponse(status_code=500,
                        content={
                            "message": "Internal Server Error",
                            "error": e_str
                        })


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Hello World"}


@app.get("/image/openapi.json", include_in_schema=False)
async def openapi():
    return RedirectResponse("/openapi.json")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Dagpi",
        version="1.0",
        description="The Number 1 Image generation api",
        routes=app.routes)
    print("got openapi")
    openapi_schema["components"] = {
        "securitySchemes": {
            "Token": {
                "type":
                "apiKey",
                "in":
                "header",
                "name":
                "Authorization",
                "description":
                "Dagpi tokens are extremely important and crucial in the way dagpi functions."
                +
                "You can get a token from visiting the website at https://dagpi.xyz. "
                +
                "For a detailed explanation and a step-by-step guide visit https://dagpi.docs.apiary.io"
            }
        }
    }
    openapi_schema["externalDocs"] = {
        "url": "https://dagpi.docs.apiary.io",
        "description": "Main Documentation"
    }

    openapi_schema["info"] = {
        "title": "Dagpi",
        "description": " A fast and powerful image manipulation api",
        "servers": [{
            "url": "https://api.dagpi.xyz/image"
        }],
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
            "url": "https://cdn.dagpi.xyz/dagpib.png"
        }
    }
    print("so far so good")
    for endpoint in openapi_schema["paths"].keys():
        if endpoint not in ["/", "/image/openapi.json"]:
            openapi_schema["paths"][endpoint]["get"]["security"] = [{
                "Token": ["Required"]
            }]
    print("nice")
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
