
from fastapi import FastAPI
from .routers import auth_router, post_router, user_router
from .database import engine, Base
from .config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
def root():
    return {'message': 'hello world!'}

app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(post_router.router)