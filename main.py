import uuid
import logging

from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from v1.routers import oauth, basic_auth
from core.exceptions import CustomInvalidTokenException, CustomExpiredTokenException, CustomInvalidClientIdException, CustomInvalidBasicAuthException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from logging_config import LOGGING_CONFIG
app = FastAPI()

# logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


app.include_router(oauth.router, prefix="/oauth")
app.include_router(basic_auth.router, prefix="/basic_auth")

# @app.exception_handlers(RequestValidationError)
# def request_exception_handler(request, exc):
#     return JSONResponse(
#         status_code=418,
#         content={"message": "LOL"},
#     )


@app.exception_handler(CustomInvalidTokenException)
def custom_invalid_token_exception_handler(request: Request, exc: CustomInvalidTokenException):
    return JSONResponse(
        status_code=401,
        headers={"WWW-Authenticate": f'Bearer realm="DefaultRealm", error="invalid_token", error_description="Unable to find the {exc.token_type} in persistent storage."'},
        content={
            "requestId": f"{exc.requestId}",
            "status": "error",
            "result": {
                "isValid": False
            },
            "errors":[{
                "code":"401",
                "message": f"Invalid {exc.token_type}"
            }]
        }
    )

@app.exception_handler(CustomExpiredTokenException)
def custom_expired_token_exception_handler(request: Request, exc: CustomExpiredTokenException):
    return JSONResponse(
        status_code=401,
        headers={"WWW-Authenticate": f'Bearer realm="DefaultRealm", error="invalid_token", error_description="The {exc.token_type} expired."'},
        content={
            "requestId": f"{exc.requestId}",
            "status": "error",
            "result": {
                "isValid": False
            },
            "errors":[{
                "code":"401",
                "message": f"Expired {exc.token_type}"
            }]
        }
    )

@app.exception_handler(CustomInvalidClientIdException)
def custom_invalid_client_id_exception_handler(request: Request, exc: CustomInvalidClientIdException):
    return JSONResponse(
        status_code=401,
        headers={"WWW-Authenticate": f'Bearer realm="DefaultRealm", error="invalid_token", error_description=""The client app was not found or is disabled."'},
        content={
            "requestId": f"{exc.requestId}",
            "status": "error",
            "result": {
                "isValid": False
            },
            "errors":[{
                "code":"401",
                "message": f"Invalid Client ID: {exc.client_id}"
            }]
        }
    )

@app.exception_handler(CustomInvalidBasicAuthException)
def custom_invalid_basic_auth_exception_handler(request: Request, exc: CustomInvalidBasicAuthException):
    return JSONResponse(
        status_code=401,
        headers={"WWW-Authenticate": f'Bearer realm="DefaultRealm", error="invalid_basic_auth", error_description=""Incorrect username or password."'},
        content={
            "requestId": f"{exc.requestId}",
            "status": "error",
            "result": {
                "isValid": False
            },
            "errors":[{
                "code":"401",
                "message": f"Invalid username or password"
            }]
        }
    )

@app.middleware("http")
async def log_request(request: Request, call_next):
    request.state.requestId = uuid.uuid4()
    logger.info(f"rid={request.state.requestId} start request path={request.url.path}")
    response = await call_next(request)
    return response