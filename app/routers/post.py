from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

# the prefix is the api path starting point
# the tags represent the group these routes are assigned to in the documentation
router = APIRouter(prefix='/posts', tags=['posts'])


@router.get("/", response_model=List[schemas.Response])
def get_posts(db: Session = Depends(get_db), limit: int = 10, search: Optional[str] = ""):
    """
    Get all rows from the database.

    :param db: Session
        Database dependency. Returns the database the data is fetched from.
    :param limit: int
        Maximum amount of posts to show.
    :param search: str
        String to be contained in the post title
    :return: List[schemas.Response]
        All the rows in the database
    """
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()

    # results = db.query(models.Post, func.count(models.Vote.post_id).label('votes'))\
    #     .outerjoin(models.Vote, models.Post.id == models.Vote.post_id).group_by(models.Post.id).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Response)
def create_posts(post: schemas.Post, db: Session = Depends(get_db), user_id=Depends(oauth2.get_current_user)):
    """ First entry in the decorator represents the api endpoint (starting from the prefix mentioned in the router),
    second represents the status code to be sent upon successful completion of the request,
    third represents the schema for the response returned to the user.

    Create a new row using the information provided in the post request (called the payload),
    add it to the SQL database and return it.

    Parameters
    -------
    post: schemas.Post
        Data to be used for creating the new database entry.
    db: Session
        Database dependency. Returns current database.
    user_id
        User authentication dependency. Returns ID of authenticated user

    Returns
    ------
    new_post: schemas.Response
        The row that has just been added to the database.

    """
    post.user_id = user_id.id
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    # retrieve new_post from database and store it back in the variable
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.Response)
def get_post(id: int, db: Session = Depends(get_db)):
    """ Get an individual row from the database using its id.

    Parameters
    -------
    id: int
        Id of the row to be fetched.
    db: Session
        Database the data is fetched from.

    Returns
    ------
    post: schemas.Response
        The requested row.
    """
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} not found')
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), user_id=Depends(oauth2.get_current_user)):
    """
    Remove a row from the database using its id.
    :param post_id: int
        ID of the row to be removed.
    :param db: Session
        Database dependency. Returns the database to delete from.
    :param user_id:
        User authentication dependency. Returns id of user.
    """

    post = db.query(models.Post).filter(models.Post.id == post_id)
    if not post.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {post_id} not found')
    if int(user_id.id) != post.first().user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail=f"Deleting another user's post is not permitted.")
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{post_id}", response_model=schemas.Response)
def update_post(post_id: int, updated_post: schemas.Post, db: Session = Depends(get_db),
                user_id=Depends(oauth2.get_current_user)):
    """
    Get an individual row from the database using its id.

    :param post_id: int
        ID of the row to be updated.
    :param updated_post: schemas.Post
        Data to be used for updating the database entry.
    :param db: Session
        The database dependency.
    :param user_id:
        The user authentication dependency. Returns user id from payload.
    :return: post: schemas.Response
        The updated row.
    """
    post = db.query(models.Post).filter(models.Post.id == post_id)

    if not post.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {post_id} not found')
    if int(user_id.id) != post.first().user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail="Modifying another user's post is not permitted.")
    updated_post.user_id = user_id.id
    post.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return post.first()
