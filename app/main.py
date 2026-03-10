
from fastapi import FastAPI
from .routers import users, auth, posts
from . import models 
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
def root():
    return {'message': 'hello world!'}

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(posts.router)