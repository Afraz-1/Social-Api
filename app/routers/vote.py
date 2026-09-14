from typing import List, Optional
from fastapi import Body, Depends, FastAPI,status,HTTPException,APIRouter
from sqlalchemy.orm import Session
from app import models, oauth2,schema,utils
from app.database import  get_db

router = APIRouter(
    prefix='/vote',
    tags=['Vote']
)

@router.post('/',status_code=status.HTTP_201_CREATED)
def vote(vote : schema.vote, db : Session = Depends(get_db),
         current_user : models.User = Depends(oauth2.get_current_user)):



    post = db.query(models.Post).filter(
        models.Post.id == vote.post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post does not exist"
        )


    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                              models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="already voted post")
        new_vote = models.Vote(post_id = vote.post_id,user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Voted succesfully"}

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="never voted before")

        db.delete(found_vote)
        db.commit()
        return {"message" : "downvoted succesfully"}