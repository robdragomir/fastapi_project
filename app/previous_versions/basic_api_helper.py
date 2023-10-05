from fastapi import status, HTTPException


my_posts = [{"title": "title1", "content": "content1", "id": 1},
            {"title": "favourite foods", "content": "pizza", "id": 2}]


def find_post(id: int):
    for post in my_posts:
        if post['id'] == id:
            return post
    raise HTTPException(status.HTTP_404_NOT_FOUND,
                        detail=f'post with id: {id} not found')


def find_index_post(id: int):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
    raise HTTPException(status.HTTP_404_NOT_FOUND,
                        detail=f'post with id: {id} not found')