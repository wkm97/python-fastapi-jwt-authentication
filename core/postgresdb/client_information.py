from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ClientInformation(Base):
    __tablename__ = 'client_information'
    client_id = Column(String(255), primary_key=True)
    public_key =  Column(Text, nullable=False)
