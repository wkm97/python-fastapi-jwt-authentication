from fastapi import BackgroundTasks, APIRouter, Request
from pydantic import BaseModel
from fastapi.responses import Response, JSONResponse

from core.postgresdb.active_sessions import ActiveSessions
from core.postgresdb.database import Database
from core.exceptions import CustomInvalidBasicAuthException
from v1.services.basic_auth import BasicAuthentication

router = APIRouter()
basicAuthentication = BasicAuthentication()

class basicAuthRequest(BaseModel):
    username: str = 'JDoe'
    password: str = '123456'

@router.post("/verification", tags=["basic_auth"])
def basic_auth_verification(form_data: basicAuthRequest, request: Request):
    requestId = request.state.requestId
    result = basicAuthentication.validate_basic_auth(form_data.username, form_data.password)
    if(result == False):
        raise CustomInvalidBasicAuthException(requestId=requestId)
    else:
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