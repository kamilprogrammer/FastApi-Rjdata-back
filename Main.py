from fastapi import FastAPI , HTTPException , Depends , status
from pydantic import BaseModel
from typing import Annotated
import models
from db import engine  , SessionLocal
from sqlalchemy.orm import Session
import auth
from auth import get_current_user

app = FastAPI()
app.include_router(auth.router)

models.Base.metadata.create_all(bind = engine)

class PostBase(BaseModel):
    Title: str
    Kind : str
    place : str
    user_id: int
    Other : str
    
class UserBase(BaseModel):
    username : str 
    password : str
    company : str
    phone : str


def get_db():
    db = SessionLocal()
    try:
        yield db

    finally :
        db.close()        
        

db_depend = Annotated[Session , Depends(get_db)]
user_depend = Annotated[dict , Depends(get_current_user)]


@app.get("/api" , status_code=status.HTTP_200_OK)
def User(user: user_depend , db:db_depend):
    if user is None:
        raise HTTPException(status_code=401 , detail="Authentication Failed!")
    return {'User':user}

@app.post('/api/register' , status_code=status.HTTP_201_CREATED)
def add_user(user : UserBase , db : db_depend):
    user = models.User(**user.__dict__)
    if user.username is '' or user.password is '' or user.phone is '' or user.company is '':
        raise HTTPException(status_code=401 , detail="Please fill all the gaps :)")
    db.add(user)
    db.commit()
    return {'user_data' : {"username":user.username, "password":user.password}}

@app.get('/api/user/{username}' , status_code=status.HTTP_200_OK)
def user(username: str , db : db_depend):
    user=db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise HTTPException(status_code=404 , detail='User is not Found')
    return user

@app.post('/api/add_post' , status_code=status.HTTP_201_CREATED)
def add_post(post : PostBase , db : db_depend):
    post = models.Post(**post.__dict__)
    db.add(post)
    db.commit()
    return {"Post_Details" : {"Title" : post.Title , "kind" : post.Kind , "place": post.place , "other":post.Other , "user_id":post.user_id}}

@app.get('/api/post/{post_id}' , status_code=status.HTTP_200_OK)
def post(post_id: int , db : db_depend):
    post=db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404 , detail='Post is not Found')
    return post


@app.get('/api/post/delete/{post_id}' , status_code=status.HTTP_200_OK)
def del_post(post_id: int , db : db_depend):
    post=db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404 , detail='Post is not Found')
    db.delete(post)
    db.commit()
    return "Done"

@app.get('/api/user/delete/{user_id}' , status_code=status.HTTP_200_OK)
def del_user(user_id: int , db : db_depend):
    user=db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404 , detail='User is not Found')
    db.delete(user)
    db.commit()
    return "Done"


@app.post("/api/users" , status_code=status.HTTP_200_OK)
def Show_Users(db:db_depend):
    users=db.query(models.User).all()
    if users is None:
        raise HTTPException(status_code=404 , detail='There is No users!')
    
    return users

@app.put("/api/user/company/{user_id}")
def Company(db:db_depend , user_id : int , user:UserBase):
    user_model=db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404 , detail='User is not Found')
    
    user_model.company = user.company
    db.add(user_model)
    db.commit()
    return "Done"
    