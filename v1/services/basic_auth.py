from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound

from core.postgresdb.database import Database
from core.postgresdb.user_information import UserInformation

class BasicAuthentication:
    def __init__(self):
        self.sessiondb = Database.get_session()

    def validate_basic_auth(self, username, password):
        try:
            user = self.sessiondb.query(UserInformation).filter(
                UserInformation.username == username
            ).one()
            if(user.password != password):
                return False
            else:
                return True
        except NoResultFound:
            return False