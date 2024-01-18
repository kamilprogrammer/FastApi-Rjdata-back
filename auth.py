from datetime import timedelta , datetime
from typing import Annotated
from fastapi import APIRouter , Depends , HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from db import SessionLocal
from models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm , OAuth2PasswordBearer
from jose import jwt , JWTError

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = 'kamIl044'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'] , deprecated = 'auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


class CreateUserRequest(BaseModel):
    username: str
    password : str
    company: str
    phone : str
   

class Token(BaseModel):
    access_token : str
    token_type : str  

def get_db():
    db = SessionLocal()
    try:
        yield db

    finally :
        db.close()  


db_depend = Annotated[Session , Depends(get_db)]

@router.post("/api" , status_code=status.HTTP_201_CREATED)
def create_user(db : db_depend , create_user_request : CreateUserRequest):
    create_user_model = User(username = create_user_request.username,
                             password = create_user_request.password,
                             phone = create_user_request.phone,
                             )
    
    db.add(create_user_model)
    db.commit()
 

@router.post("/token" , response_model=Token)

async def Acces_Token(form_data : Annotated[OAuth2PasswordRequestForm , Depends() , ],
                db: db_depend
                ):

    user  = auth_user(form_data.username  , form_data.password , db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Couldn't validate user")
    
    token = create_access_token(user.username , user.id )

    return {'access_token': token , 'token_type':'bearer'}
    


def auth_user(username : str , password : str , db):
        user = db.query(User).filter(User.username == username).first()

        if not user:
            return False
        
        if not password == user.password :
            return False
        
        return user

def create_access_token(username : str , user_id : int):
        encode = {'sub' : username , 'id': user_id}
        return jwt.encode(encode , SECRET_KEY , algorithm=ALGORITHM)


def get_current_user(token : Annotated[str , Depends(oauth2_bearer)]):
     try:
          payload  = jwt.decode(token , SECRET_KEY , algorithms=ALGORITHM)
          username: str = payload.get('sub')
          user_id : int = payload.get('id')
          if username is None or user_id is None:
               raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Could not Validate User!")
          return {'username': username , 'id':user_id}
            
     
     except JWTError:
          raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail='Could not Validate User!')