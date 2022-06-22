from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.encoders import jsonable_encoder
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .config import settings as s

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = s.SECRET_KEY
ALGORITHM = s.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = s.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):
    to_encode = data.copy()
    exp = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": exp})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get('user_id')
    except JWTError:
        raise credentials_exception

    token_data = schemas.TokenData(id=id)
    return token_data


def get_current_user(token: str = Depends(oauth2_schema)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
     detail='could not validate credentials', headers={'WWW-Authenticate':'Bearer'})    
    return verify_access_token(token, credentials_exception)

 



