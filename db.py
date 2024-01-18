from sqlalchemy import Column, Integer, String, DateTime,Boolean , create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import  declarative_base

URL_DATABASE = 'mysql+pymysql://root@localhost:3306/rjdata'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit = False , autoflush = False , bind=engine)

Base = declarative_base()

