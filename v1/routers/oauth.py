from datetime import timedelta
import logging
import json


from fastapi import BackgroundTasks, APIRouter, Request
from fastapi import HTTPException, status
from fastapi.responses import Response, JSONResponse
from pydantic import BaseModel
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from v1.services.jwt_auth import JwtAuthentication
from v1.services.token_auth import TokenAuthentication
from core.exceptions import CustomInvalidTokenException, CustomExpiredTokenException, CustomInvalidClientIdException


router = APIRouter()
jwtAuthentication = JwtAuthentication()
tokenAuthentication = TokenAuthentication()

logger = logging.getLogger(__name__)

class jwtGrantRequest(BaseModel):
    grant_type: str = 'urn:ietf:params:oauth:grant-type:jwt-bearer'
    assertion: str

class accessToken(BaseModel):
    access_token: str

class refreshToken(BaseModel):
    refresh_token: str

class tokenResponse(BaseModel):
    access_token: str = "O91G451HZ0V83opz6udiSEjchP......"
    token_type: str = "bearer"
    expires_in: str = "3600"
    refresh_token: str = "8722gffy2229220002iuueee7GP..........."

class validationResponse(BaseModel):
    requestId: str = ""
    status: str = "ok"
    result: dict = {"isValid": True}
    errors: list = [{"code": "","message": ""}]



@router.get("/get_jwt", tags=["oauth"])
def get_jwt_token():
    jwt_token = jwtAuthentication.create_jwt_token()
    return {"jwt-token": jwt_token}

@router.post("/request_token", tags=["oauth"], response_model=tokenResponse)
async def request_access_token(form_data: jwtGrantRequest, background_tasks: BackgroundTasks, request: Request):
    requestId = request.state.requestId
    body = json.dumps(await request.json())
    logger.info(f"RequestId: {requestId}, Path requested: {request.url.path}, body: {body}")
    
    # Scedule to clean used and expired token.
    background_tasks.add_task(tokenAuthentication.clean_tokens)

    if(form_data.grant_type != 'urn:ietf:params:oauth:grant-type:jwt-bearer'):
        logger.error(f"RequestId: {requestId}, Msg: Invalid Grant Type")
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid Grant Type")
    try:
        if(jwtAuthentication.validate_jwt_token(form_data.assertion)):
            access_token = tokenAuthentication.create_access_token()
            expires_in = str(tokenAuthentication.get_expires_delta_access_token()*60)
            refresh_token = tokenAuthentication.create_refresh_token()
            return {"access_token": access_token, "token_type": "bearer", "expires_in": expires_in, "refresh_token": refresh_token}
    except ExpiredSignatureError:
        logger.error(f"RequestId: {requestId}, Msg: Access Token Expired.")
        raise CustomExpiredTokenException(requestId=requestId, token_type="jwt_token")
    except InvalidTokenError:
        logger.error(f"RequestId: {requestId}, Msg: Access Token Invalid.")
        raise CustomInvalidTokenException(requestId=requestId, token_type="jwt_token")
    except CustomInvalidClientIdException as e:
        print(e.client_id)
        raise CustomInvalidClientIdException(requestId=requestId, client_id=e.client_id)


@router.post("/refresh_token", tags=["oauth"], response_model=tokenResponse)
async def refresh_token(form_data: refreshToken, request: Request):
    requestId = request.state.requestId
    body = json.dumps(await request.json())

    logger.info(f"RequestId: {requestId}, Path requested: {request.url.path}, body: {body}")

    try:
        access_token = tokenAuthentication.refresh_token(form_data.refresh_token)
        expires_in = str(tokenAuthentication.get_expires_delta_access_token()*60)
        refresh_token = form_data.refresh_token

        return {"access_token": access_token, "token_type": "bearer", "expires_in": expires_in, "refresh_token": refresh_token}
    except CustomExpiredTokenException:
        logger.error(f"RequestId: {requestId}, Msg: Refresh Token Expired.")
        raise CustomExpiredTokenException(requestId=requestId, token_type="refresh_token")
    except CustomInvalidTokenException:
        logger.error(f"RequestId: {requestId}, Msg: Refresh Token Invalid.")
        raise CustomInvalidTokenException(requestId=requestId, token_type="refresh_token")

# @router.post("/validate_jwt_token", tags=["oauth"], response_model=validationResponse)
async def validate_jwt_token(form_data:jwtGrantRequest, request: Request):
    requestId = request.state.requestId
    body = json.dumps(await request.json())
    logger.info(f"RequestId: {requestId}, Path requested: {request.url.path}, body: {body}")

    try:
        status = jwtAuthentication.validate_jwt_token(form_data.assertion)
        return JSONResponse(
            status_code=200,
            content={
                "requestId": f"{requestId}",
                "status": "ok",
                "result": {
                    "isValid": True
                },
                "errors":[{
                }]
            }
        )
    except ExpiredSignatureError:
        raise CustomExpiredTokenException(requestId=requestId, token_type="jwt_token")
    except InvalidTokenError:
        raise CustomInvalidTokenException(requestId=requestId, token_type="jwt_token")

@router.post("/validate_access_token", tags=["oauth"], response_model=validationResponse)
async def validate_access_token(form_data: accessToken, request: Request):
    requestId = request.state.requestId
    body = json.dumps(await request.json())
    logger.info(f"RequestId: {requestId}, Path requested: {request.url.path}, body: {body}")

    try:
        status = tokenAuthentication.validate_token(form_data.access_token, "access_token")
        return JSONResponse(
            status_code=200,
            content={
                "requestId": f"{requestId}",
                "status": "ok",
                "result": {
                    "isValid": True
                },
                "errors":[{
                }]
            }
        )
    except CustomExpiredTokenException:
        logger.error(f"RequestId: {requestId}, Msg: Access Token Expired.")
        raise CustomExpiredTokenException(requestId=requestId, token_type="access_token")
    except CustomInvalidTokenException:
        logger.error(f"RequestId: {requestId}, Msg: Access Token Invalid.")
        raise CustomInvalidTokenException(requestId=requestId, token_type="access_token")
    