from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

# the prefix is the api path starting point
# the tags represent the group these routes are assigned to in the documentation
router = APIRouter(prefix='/vote', tags=['votes'])


@router.get("/{post_id}")
def get_post_votes(post_id: int, db: Session = Depends(get_db)):
    """
    Get total number of likes for a post.
    :param post_id: int
        The ID of post to get the likes for.
    :param db: Session
        Database dependency
    :return: dict
        Dictionary with one key called 'votes' containing the number of votes for the post.
    """
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} not found')
    votes = db.query(models.Vote).filter(models.Vote.post_id == post_id).count()
    return {"votes": votes}


@router.post("/{post_id}", status_code=status.HTTP_201_CREATED)
def like_post(post_id: int, db: Session = Depends(get_db), user_id=Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} not found')

    current_vote = db.query(models.Vote).filter(models.Vote.user_id == int(user_id.id),
                                                models.Vote.post_id == post_id).first()
    if current_vote:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail=f'You already liked this post.')

    new_vote = models.Vote(post_id=post_id, user_id=user_id.id)
    db.add(new_vote)
    db.commit()
    # retrieve new_post from database and store it back in the variable
    db.refresh(new_vote)

    return new_vote


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def unlike_post(post_id: int, db: Session = Depends(get_db), user_id=Depends(oauth2.get_current_user)):
    """
    Remove the like from a post you liked.
    :param post_id: int
        ID of the post to be unliked.
    :param db: Session
        Database dependency.
    :param user_id:
        User authentication dependency. Returns id of user.
    """

    post = db.query(models.Post).filter(models.Post.id == post_id)
    if not post.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {post_id} not found')

    current_vote = db.query(models.Vote).filter(models.Vote.user_id == int(user_id.id),
                                                models.Vote.post_id == post_id)
    if not current_vote.first():
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail=f'You have not liked this post.')

    current_vote.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
