from datetime import datetime
from typing import Optional


from pydantic import BaseModel,ConfigDict,EmailStr

class Userout(BaseModel):
    id : int
    name : str
    email : str
    created_at : datetime
    model_config = ConfigDict(from_attributes=True)

class PostBase(BaseModel):
    title : str
    content : str
    published : bool = False

class CreatePost(PostBase):
    pass

class Post(PostBase):
    id : int
    created_at : datetime
    owner : Userout
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email : EmailStr
    password : str
    name : str



class Userlogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str    

class Tokenout(BaseModel):
    id : Optional[int] = None