
from ctypes import util

from fastapi import APIRouter, HTTPException, status, Response, Depends
from typing import List, Optional
from ..schemas import UserResponse, User
from ..database import get_db
from .. import models, utils, oauth2
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

router = APIRouter(
    prefix='/users',
    tags=['User']
)

@router.get('/', response_model=List[UserResponse])
def read_users(db: Session = Depends(get_db), current_user: UserResponse = Depends(oauth2.get_current_user)):
    users = db.query(models.User).all()
    return users

@router.get('/{user_id}', response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User id: {user_id} not found')
    return  user

@router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: User, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user.password = utils.get_password_hash(user.password)
    db_user = models.User(**user.model_dump())

    db.add(db_user)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')
    db.refresh(db_user)
    return db_user

@router.put('/{user_id}', response_model=UserResponse)
def update_user(user_id: int, user_data: User, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    db_user = db.get(models.User, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User id: {user_id} not found')
    
    for field, value in user_data.model_dump().items():
        if field == 'password':
            setattr(db_user, field, utils.get_password_hash(value))
        else:
            setattr(db_user, field, value)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user = db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User id: {user_id} not found')
    
    db.delete(user)
    db.commit()