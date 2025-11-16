# model/post_model.py

from pydantic import BaseModel

_posts = [
    {"id": 1, "user_id": 2,"user_name" : "Bob", "title" : "title 1", "content": "hello, my name is dd", "img" : None},
    {"id": 2, "user_id": 3, "user_name" : "Carol", "title" : "title 2", "content": "hello, my name is rr", "img" : None},
    {"id": 3, "user_id": 3, "user_name" : "Carol", "title" : "title 3", "content": "hello, my name is ff", "img" : None},
]

def get_posts():
    return _posts.copy()

def get_post_by_id(post_id: int):
    return next((p for p in _posts if p["id"] == post_id), None)

def upload_post(new_post: dict):
    _posts.append(new_post)
    return new_post

def update_post(updates: dict, post_id: int):
    for i, post in enumerate(_posts):
        if post["id"] == post_id:
            _posts[i].update(updates)
            return _posts[i]
    return None

def delete_post(post_id: int):
    for i, post in enumerate(_posts):
        if post["id"] == post_id:
            del_post = _posts.pop(i)
            return del_post
    return None