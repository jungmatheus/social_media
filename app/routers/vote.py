from .. import schemas, utils, models
from fastapi import Response, status, HTTPException, APIRouter, Depends
from ..database import get_db
from sqlalchemy.orm import Session
from .. import oauth2

router = APIRouter(prefix='/vote', tags=['Vote'])


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.VoteIn, db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):

    post_check = db.query(models.Post).filter(vote.post_id == models.Post.id).first()
    if not post_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Could not find a post with the given id')

    query  = db.query(models.Vote).filter(vote.post_id == models.Vote.post_id, models.Vote.user_id == user.id)

    if vote.dir is True:
       if not query.first():
        new_row = models.Vote(user_id=user.id, post_id=vote.post_id)
        db.add(new_row)
        db.commit()
        return Response(status_code=status.HTTP_201_CREATED)
       else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have already liked this post")
    if not query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


