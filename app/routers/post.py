
from .. import schemas, models
from ..database import get_db
from fastapi import Response, status, HTTPException, APIRouter, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import oauth2

router = APIRouter(prefix='/posts', tags=['Posts'])


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, offset: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()
    return posts
 
 
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):

    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(
        models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found" )
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.BasePost)
def create_post(post: schemas.PostIn, db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):

    user_info = db.query(models.User).filter(user.id == models.User.id).first()    
    post_dict = post.dict()
    post_dict["user_id"] = user_info.id
    new_post = models.Post(**post_dict)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

 
@router.delete("/{id}",  status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find post with id {id}")
    
    if post.first().user_id == user.id:
        post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only delete your own post")
 
@router.put("/{id}", response_model=schemas.BasePost)
def update_post(id: int, post: schemas.PostIn, db: Session = Depends(get_db), user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not find post with id {id}")
    if post_query.first().user_id == user.id:
        post_query.update(post.dict(), synchronize_session=False)
        db.commit()
        return post_query.first()
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only update your own post")
    
 