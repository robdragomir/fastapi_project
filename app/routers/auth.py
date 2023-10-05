from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, utils, oauth2, schemas
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=['authentication'])


@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm returns username and password.
    # Expects user credentials to be in form-data, not raw
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail=f'Invalid credentials')

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail=f'Invalid credentials')

    # create a JWT token
    token = oauth2.create_access_token({"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}
