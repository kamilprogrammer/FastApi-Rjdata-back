from sqlalchemy import Boolean , Integer , String , Column
from db import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True , index=True)
    username = Column(String(50),  nullable=False , )
    phone = Column(String(11), nullable=False)
    company = Column(String(255))
    password = Column(String(100), nullable=False)


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True , index=True)
    Title = Column(String(50), nullable=False)
    Kind = Column(String(100), nullable=False)
    place = Column(String(255), nullable=False)
    user_id = Column(Integer)
    Other = Column(String(100), nullable=False)
