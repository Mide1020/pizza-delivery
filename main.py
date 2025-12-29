from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.openapi.utils import get_openapi

from routers.auth_routes import auth_router
from routers.order_routes import order_router

from fastapi_jwt_auth2 import AuthJWT
from schema import settings

from database import engine

import inspect
import re


app = FastAPI()


@app.on_event("startup")
def startup():
    try:
        with engine.connect() as conn:
            print("✅ Database connection successful")
    except Exception as e:
        print("❌ Database connection failed:", e)


@app.get("/")
def root():
    return {"message": "Pizza Delivery API is running"}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Pizza Delivery API",
        version="1.0",
        description="An API for a Pizza Delivery Service",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Enter: **'Bearer <JWT>'**, where JWT is the access token"
        }
    }

    api_routes = [route for route in app.routes if isinstance(route, APIRoute)]

    for route in api_routes:
        path = route.path
        endpoint = route.endpoint
        methods = [method.lower() for method in route.methods]

        for method in methods:
            if (
                re.search("jwt_required", inspect.getsource(endpoint)) or
                re.search("fresh_jwt_required", inspect.getsource(endpoint)) or
                re.search("jwt_optional", inspect.getsource(endpoint))
            ):
                openapi_schema["paths"][path][method]["security"] = [
                    {"Bearer Auth": []}
                ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@AuthJWT.load_config
def get_config():
    return settings()


app.include_router(auth_router)
app.include_router(order_router)
