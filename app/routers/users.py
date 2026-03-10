from fastapi import APIRouter, HTTPException, status, Response
from typing import List, Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from ..schemas import UserResponse, User

router = APIRouter(
    prefix='/users',
    tags=['User']
)

# Connect to your postgres DB
conn = psycopg2.connect(
    database='fastapi',
    user='postgres',
    password='root',
    host='localhost',
    port=5432,
    cursor_factory=RealDictCursor
)

# Open a cursor to perform database operations
cur = conn.cursor()

@router.get('/', response_model=List[UserResponse])
def read_users():
    cur.execute("""SELECT * FROM users""")
    users = cur.fetchall()
    return users

@router.get('/{id}')
def read_user(id: int, response_model=UserResponse):
    cur.execute("""SELECT * FROM users WHERE id = %s """, (str(id),))
    user = cur.fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User id: {id} not found')
    return  user

@router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    cur.execute("""INSERT INTO users(email, password) VALUES (%s, %s) RETURNING * """, (user.email,  user.password))
    user = cur.fetchone()
    conn.commit()
    return user

@router.put('/{id}', response_model=UserResponse)
def update_user(id: int, user_data: User):
    cur.execute("""SELECT * FROM users WHERE id = %s """, (str(id),))
    user = cur.fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User id: {id} not found')
    
    cur.execute("""UPDATE users SET email=%s, password=%s WHERE id=%s RETURNING * """, (user_data.email,  user_data.password, id))
    user = cur.fetchone()
    conn.commit()
    return user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int):

    cur.execute(
        """DELETE FROM users WHERE id = %s RETURNING *""",
        (id,)
    )

    deleted_user = cur.fetchone()

    if not deleted_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User id: {id} not found"
        )

    conn.commit()