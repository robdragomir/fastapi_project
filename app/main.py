"""
CRUD:
    Create - POST  /posts
    Read - GET  /posts/:id
    Update - PUT (for changing the whole entry)  /posts/:id
           - PATCH (for changing some parts of the entry) /posts/:id
    Delete - DELETE  /posts/:id

Go to url/docs for api documentation
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote


# create tables if they don't already exist, not needed if you're using alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]
# set access permissions for domains, methods and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World!"}
