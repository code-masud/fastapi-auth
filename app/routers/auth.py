from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas import User
from ..database import get_db
from .. import models, utils

router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(credentials: User, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email==credentials.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials"
        )
    
    if not utils.verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials"
        )
    return {'message': 'login successfully.'}
    