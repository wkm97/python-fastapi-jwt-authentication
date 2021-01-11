from sqlalchemy import Column, Integer, String, Text, Sequence
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserInformation(Base):
    __tablename__ = 'user_information'
    id = Column('id', Integer, Sequence('user_information_id_seq'), primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password =  Column(String(255), nullable=False)
