# from fastapi import FastAPI
# from  routers.auth_routes  import auth_router
# from  routers.order_routes  import order_router
# from fastapi_jwt_auth2 import AuthJWT
# from fastapi_jwt_auth2.exceptions import AuthJWTException
# from fastapi.responses import JSONResponse
# from schema import settings
# import inspect, re
# from database import Base, engine
# from fastapi import FastAPI
# from fastapi.routing import APIRoute
# from fastapi.openapi.utils import get_openapi



# app = FastAPI()


# @app.on_event("startup")
# def startup():
#     Base.metadata.create_all(bind=engine)


# @app.get("/")
# def root():
#     return {"message": "Pizza Delivery API is running"}

# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema

#     openapi_schema = get_openapi(
#         title = "Pizza Delivery API",
#         version = "1.0",
#         description = "An API for a Pizza Delivery Service",
#         routes = app.routes,
#     )

#     openapi_schema["components"]["securitySchemes"] = {
#         "Bearer Auth": {
#             "type": "apiKey",
#             "in": "header",
#             "name": "Authorization",
#             "description": "Enter: **'Bearer &lt;JWT&gt;'**, where JWT is the access token"
#         }
#     }

#     # Get all routes where jwt_optional() or jwt_required
#     api_router = [route for route in app.routes if isinstance(route, APIRoute)]

#     for route in api_router:
#         path = getattr(route, "path")
#         endpoint = getattr(route,"endpoint")
#         methods = [method.lower() for method in getattr(route, "methods")]

#         for method in methods:
#             # access_token
#             if (
#                 re.search("jwt_required", inspect.getsource(endpoint)) or
#                 re.search("fresh_jwt_required", inspect.getsource(endpoint)) or
#                 re.search("jwt_optional", inspect.getsource(endpoint))
#             ):
#                 openapi_schema["paths"][path][method]["security"] = [
#                     {
#                         "Bearer Auth": []
#                     }
#                 ]

#     app.openapi_schema = openapi_schema
#     return app.openapi_schema


# app.openapi = custom_openapi

# @AuthJWT.load_config
# def get_config():
#     return settings()

    
# app.include_router(auth_router)
# app.include_router(order_router)


from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.openapi.utils import get_openapi

from routers.auth_routes import auth_router
from routers.order_routes import order_router

from fastapi_jwt_auth2 import AuthJWT
from schema import settings

from database import Base, engine

import inspect
import re


app = FastAPI()


@app.on_event("startup")
def startup():
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database connected successfully")
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

