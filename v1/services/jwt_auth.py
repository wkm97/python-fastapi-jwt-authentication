from datetime import datetime, timedelta
from typing import Optional
import json

# from jose import JWTError, ExpiredSignatureError, jwt, jws
import jwt
import base64
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from cryptography.hazmat.primitives import serialization
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
import rsa

from fastapi import HTTPException, status

from core.postgresdb.client_information import ClientInformation
from core.postgresdb.database import Database
from core.exceptions import CustomInvalidClientIdException

ACCESS_TOKEN_EXPIRE_MINUTES = 30
# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "RS256"

with open('../keysets/server.key', mode='rb') as private_file:
    pem_bytes = private_file.read()
    PRIVATE_KEY = serialization.load_pem_private_key(pem_bytes, password=b'Globe123#', backend=default_backend())
    

with open('../keysets/server.crt', mode='rb') as public_file:
    pem_bytes = public_file.read()
    PUBLIC_KEY = load_pem_x509_certificate(pem_bytes, backend=default_backend())
    PUBLIC_KEY = PUBLIC_KEY.public_key()

class JwtAuthentication:
    def __init__(self):
        self.issuer = "GlobeOSS"
        self.aud = "http://apiserver/api/oauth/token"
    
    def create_jwt_token(self, data: dict = {}, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"iss": self.issuer, "aud": self.aud, "exp": expire, "iat": datetime.utcnow()})

        encoded_jwt = jwt.encode(to_encode, PRIVATE_KEY, algorithm=ALGORITHM)

        return encoded_jwt

    def get_issuer_from_token(self, token:str):
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload['iss']

    def validate_jwt_token(self, token: str):
        try:
            session = Database.get_session()

            issuer = self.get_issuer_from_token(token)
            clients = session.query(ClientInformation).filter(ClientInformation.client_id == issuer)
            if(clients.count() == 0):
                raise CustomInvalidClientIdException(requestId=None, client_id=issuer)

            public_key = clients.first().public_key.encode('utf-8')
            
            
            public_cert = load_pem_x509_certificate(public_key, backend=default_backend())
            payload = jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM], audience=self.aud)
            return True
        except ExpiredSignatureError:
            raise ExpiredSignatureError()
        except InvalidTokenError:
            raise InvalidTokenError()
        finally:
            session.close()
