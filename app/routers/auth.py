from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import  schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm



router = APIRouter(tags=["Authentication"])


#QUESTION: WHAT STOPS ME FROM SHARING MY TOKEN?


@router.post("/login", response_model=schemas.Token)
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    cred_check = db.query(models.User).filter(models.User.email == credentials.username).first()

    if cred_check is None or not utils.verify_passwd(credentials.password, cred_check.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid email or password")    

    token = oauth2.create_access_token({"user_id": cred_check.id})

    return {"access_token": token, "token_type": "bearer"}
    
