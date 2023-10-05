from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

try:
    conn = psycopg2.connect(host='localhost', database='robert', user='robert',
                            password='12KdhEev', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was successful")
except Exception as error:
    print("Connection failed due to the following error:", error)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: Optional[int] = True


@app.get("/")
def root():
    return {"message": "Hello World!"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    return {'data': cursor.fetchall()}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published))
    conn.commit()
    return {'data': cursor.fetchone()}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(f"""SELECT * FROM posts WHERE id=%s""", (str(id)))
    output = cursor.fetchone()
    if not output:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} not found')
    return {"post_detail": output}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()
    if not deleted_post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} not found')
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id=%s RETURNING * """,
                   (post.title, post.content, post.published, str(id)))
    output = cursor.fetchone()
    if not output:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} not found')
    conn.commit()
    return {"data": output}
