from typing import List

from fastapi import Body, Depends, status,HTTPException,APIRouter
from sqlalchemy.orm import Session
from app import models,schema,utils
from app.database import get_db


Router = APIRouter(
     prefix="/users",
     tags=['Users']
)


@Router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.Userout)
def usercreate(user : schema.UserCreate,db:Session = Depends(get_db)):
    hashedpass = utils.hash(user.password)
    user.password = hashedpass


    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
       
    return new_user

@Router.get("/",response_model=List[schema.Userout])
def get_all(db:Session = Depends(get_db)):
     
     posts = db.query(models.User).all()
     return posts

@Router.get("/{id}" ,response_model=schema.Userout)
def get_user(id : int, db : Session = Depends(get_db)):
     user = db.query(models.User).filter(models.User.id == id).first()
     if not user:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found ")

     return user 