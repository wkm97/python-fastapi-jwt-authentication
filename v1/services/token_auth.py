from datetime import datetime, timedelta
from typing import Optional
import secrets

from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from fastapi import HTTPException, status

from core.postgresdb.active_sessions import ActiveSessions
from core.postgresdb.database import Database
from core.exceptions import CustomInvalidTokenException, CustomExpiredTokenException

class TokenAuthentication:
    def __init__(self):
        self.expires_delta_access_token = 20
        self.expires_delta_refresh_token = 10*365
        self.sessiondb = Database.get_session()

    def create_access_token(self):
        token_type = "access_token"
        token = secrets.token_urlsafe(22)
        iat = int(datetime.utcnow().timestamp())
        exp = int((datetime.utcnow() + timedelta(minutes=self.expires_delta_access_token)).timestamp())
        active_session = ActiveSessions(token_type=token_type, token=token, iat=iat, exp=exp)
        self.sessiondb.add(active_session)
        self.sessiondb.commit()
        return token
    
    def create_refresh_token(self):
        token_type = "refresh_token"
        token = secrets.token_urlsafe(22)
        iat = int(datetime.utcnow().timestamp())
        exp = int((datetime.utcnow() + timedelta(minutes=self.expires_delta_access_token)).timestamp())
        active_session = ActiveSessions(token_type=token_type, token=token, iat=iat, exp=exp)
        self.sessiondb.add(active_session)
        self.sessiondb.commit()
        return token
    
    def get_expires_delta_access_token(self):
        return self.expires_delta_access_token

    def get_expires_delta_refresh_token(self):
        return self.expires_delta_refresh_token
    
    def validate_token(self, access_token, token_type):
        timenow = iat = int(datetime.utcnow().timestamp())
        try:
            token = self.sessiondb.query(ActiveSessions).filter(
                ActiveSessions.token_type == token_type, 
                ActiveSessions.token == access_token
                ).one()
            if(token.exp < timenow): # Expired
                raise CustomExpiredTokenException()
            return True
        except MultipleResultsFound:
            raise CustomInvalidTokenException()
        except NoResultFound:
            raise CustomInvalidTokenException()
    
    def refresh_token(self, refresh_token):
        if(self.validate_token(refresh_token, "refresh_token")):
            return self.create_access_token()
        else:
            return None
    
    # Clean expired token in database
    def clean_tokens(self):
        timenow = iat = int(datetime.utcnow().timestamp())
        self.sessiondb.query(ActiveSessions).filter(ActiveSessions.exp < timenow).delete()
        self.sessiondb.commit()
    



