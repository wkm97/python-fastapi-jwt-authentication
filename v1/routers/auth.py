from datetime import timedelta

from fastapi import APIRouter
from fastapi import HTTPException, status
from pydantic import BaseModel

from core.jwt_auth import JwtAuthentication, Token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()
jwtAuthentication = JwtAuthentication()


class LoginCredential(BaseModel):
    username: str = 'johndoe'
    password: str = 'secret'

@router.post("/login", tags=["auth"], response_model=Token)
def login(form_data: LoginCredential):
    user = jwtAuthentication.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = jwtAuthentication.create_access_token(
        data={"sub": user.username}
    )
    refresh_token = jwtAuthentication.create_refresh_token(
        data={"sub": user.username}
    )

    return {"access_token": access_token, "token_type": "bearer", "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES*60, "refresh_token": refresh_token}

@router.post("/refresh_token", tags=["auth"], response_model=Token)
def refresh_access_token(form_data:Token):
    access_token = jwtAuthentication.refresh_access_token(form_data.refresh_token)
    print(form_data.access_token)
    form_data.access_token = access_token
    return form_data

@router.post("/validation", tags=["auth"])
def validate_access_token(form_data:Token):
    payload = jwtAuthentication.validate_access_token(form_data.access_token)
    return {"result": "valid token"}
