import jwt
from datetime import datetime,timedelta,timezone
from app import schema,database,models
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
from .config import settings



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def verify_access_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id = payload.get("user_id")
        if not id:
            raise credentials_exception
        token_data = schema.Tokenout(id = id)
    except InvalidTokenError:
        raise credentials_exception

    return token_data

def get_current_user(token : str = Depends(oauth2_scheme),db : Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid credentials",
                                         headers={"WWW-Authenticate" : "Bearer"})

    tokenn = verify_access_token(token,credential_exception)
    user = db.query(models.User).filter(models.User.id == tokenn.id).first()
    return user


