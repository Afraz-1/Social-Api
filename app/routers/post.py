from traceback import print_tb
from typing import List
from fastapi import Body, Depends, FastAPI,status,HTTPException,APIRouter
from sqlalchemy.orm import Session
from app import models, oauth2,schema,utils
from app.database import  engine, get_db


Router = APIRouter(
     prefix="/posts",
     tags=['Posts']
)



@Router.post("/",status_code=status.HTTP_201_CREATED,response_model=schema.Post)
def create(post : schema.CreatePost, db : Session = Depends(get_db),
           current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING *""",
    #               (post.title,post.content,post.published))
    # my_post = cursor.fetchone()

    # conn.commit()
    print(current_user)
    new_post = models.Post(owner_id = current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
  
    return new_post


@Router.get("/", response_model=List[schema.Post])
def posts(db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts



@Router.get("/{id}",response_model=schema.Post,)
def get_id(id : int,db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts where id = %s""",(id,))
    # post = cursor.fetchone()

    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "post not found")

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "post not found")


    return post

@Router.delete("/{id}")
def delete(id : int,db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(id,))
    # deleted_post = cursor.fetchone

    # conn.commit()
    # if not deleted_post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found ")

    deleted_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not deleted_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found ")
    if deleted_post.owner_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not accesible ")
    db.delete(deleted_post)
    db.commit()




@Router.put("/{id}",response_model=schema.Post)
def update(id : int, post : schema.PostBase,db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s,content = %s,published = %s WHERE id = %s RETURNING *""",
    #                (post.title,post.content,post.published,id))

    # updated_post = cursor.fetchone()

    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    Post = post_query.first()
    if not Post:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="post not found ")
    if Post.owner_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not accesible ")
    post_query.update(post.model_dump(),synchronize_session=False)
    db.commit()
    return post_query.first()