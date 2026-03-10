
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..database import get_db
from .. import models, schemas, oauth2

router = APIRouter(
    prefix='/posts',
    tags=['Post']
)

@router.get('/', response_model=List[schemas.PostResponse])
def read_posts(db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).all()
    return posts

@router.get('/{post_id}', response_model=schemas.PostResponse)
def read_post(post_id: int, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    db_post = db.get(models.Post, post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post id: {post_id} not found')
    return db_post

@router.post('/', response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post_data: schemas.Post, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    db_post = models.Post(
        **post_data.model_dump(),
        author=current_user.id
    )

    db.add(db_post)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')
    
    db.refresh(db_post)
    return db_post

@router.put('/{post_id}', response_model=schemas.PostResponse)
def update_post(post_id: int, post_data: schemas.Post, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    db_post = db.get(models.Post, post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post id: {post_id} not found')
    
    for field, value in post_data.model_dump().items():
        setattr(db_post, field, value)

    setattr(db_post, 'author', current_user.id)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')
    
    db.refresh(db_post)
    return db_post

@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(oauth2.get_current_user)):
    db_post = db.get(models.Post, post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post id: {post_id} not found')
    
    db.delete(db_post)
    db.commit()
