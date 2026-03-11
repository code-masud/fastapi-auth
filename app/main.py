
from fastapi import FastAPI
from .routers import users, auth, posts
from . import models 
from .database import engine
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/info")
def get_info():
    return {
        "database_url": settings.DATABASE_URL,
        "debug": settings.DEBUG
    }

@app.get('/')
def root():
    return {'message': 'hello world!'}

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(posts.router)