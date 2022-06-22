from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint

from app.models import Post 


class PostIn(BaseModel):
    title: str
    content: str
    published: bool = True

class UserIn(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
 
 
class BasePost(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    created_at: datetime
    user_id: int
    owner: UserOut

    class Config: 
        orm_mode = True

class PostOut(BaseModel):
    Post: BasePost
    votes: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int
 

class VoteIn(BaseModel):
    dir: bool
    post_id: int
    
    class Config:
        orm_mode =  True