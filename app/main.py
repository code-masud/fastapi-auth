
from fastapi import FastAPI
from .routers import auth_router, post_router, user_router
from . import __models 
from .database import engine
from .config import settings

__models.Base.metadata.create_all(bind=engine)

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

app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(post_router.router)