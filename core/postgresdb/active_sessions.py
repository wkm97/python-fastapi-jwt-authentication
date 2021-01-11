from sqlalchemy import Column, BigInteger, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ActiveSessions(Base):
    __tablename__ = 'active_sessions'
    token_type = Column(String(255), primary_key=True)
    token = Column(String(255), primary_key=True)
    exp = Column(BigInteger, nullable=False)
    iat = Column(BigInteger, nullable=False)
