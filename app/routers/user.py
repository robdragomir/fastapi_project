from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix='/users', tags=['users'])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserRequest)
def create_user(user_data: schemas.UserPost, db: Session = Depends(get_db)):
    """ Create a new user using the information provided in the post request, add it to the SQL database and return it.

    Parameters
    -------
    user_data: schemas.UserCreate
        ID and password of the new user.
    db: Session
        Database to be updated.

    Returns
    ------
    new_user: schemas.UserRequest
        The user that has just been created.

    """
    hashed_password = utils.hash_pwd(user_data.password)
    user_data.password = hashed_password

    new_user = models.User(**user_data.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserRequest)
def get_user(id:int, db: Session = Depends(get_db)):
    """ Get a user based on its id.

    Parameters
    -------
    id: int
        Id of user.
    db: Session
        Database the data is fetched from.

    Returns
    ------
    requested_user: schemas.UserRequest
        The user data

    """
    requested_user = db.query(models.User).filter(models.User.id == id).first()
    if not requested_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f'User with id: {id} not found')
    return requested_user

