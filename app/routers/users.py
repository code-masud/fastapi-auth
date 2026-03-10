from fastapi import APIRouter, HTTPException, status, Response
from typing import List, Optional
import random
from ..schemas import UserResponse, User

router = APIRouter(
    prefix='/users',
    tags=['User']
)

user_list = [{'id':1, 'email':'bob@gmail.com', 'password': 'asdf'}]

def get_user(id: int) -> Optional[dict]:
    return next((user for user in user_list if user['id'] == id), None)

def get_user_index(id: int) -> Optional[int]:
    return next((i for i, user in enumerate(user_list) if user['id'] == id), None)

@router.get('/', response_model=List[UserResponse])
def read_users():
    return user_list

@router.get('/{id}')
def read_user(id: int, response_model=UserResponse):
    user = get_user(id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User id: {id} not found')
    return  user

@router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    user_data = user.dict()
    user_data['id'] = random.randint(1, 100)
    user_list.append(user_data)
    return user_data

@router.put('/{id}', response_model=UserResponse)
def update_user(id: int, user_data: User):
    index = get_user_index(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User id: {id} not found')
    
    user = user_data.dict()
    user['id'] = id
    user_list[index] = user
    
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    index = get_user_index(user_id)

    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    user_list.pop(index)