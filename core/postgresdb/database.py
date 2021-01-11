from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import PostgresdbConfig

class Database(object):
    host = PostgresdbConfig.host
    port = str(PostgresdbConfig.port)
    database = PostgresdbConfig.database
    user = PostgresdbConfig.user
    password = PostgresdbConfig.password
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
    Session = sessionmaker(bind=engine)
    
    @staticmethod
    def get_session():
        return Database.Session()
