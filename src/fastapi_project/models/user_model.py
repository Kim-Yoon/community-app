# model/user_model.py
from pydantic import BaseModel

class User(BaseModel):
    id: str
    name: str
    email: str

_users = [
    {"id": 1, "name": "Alice", "email": "alice@test.com", "password" : "1234", "img": None},
    {"id": 2, "name": "Bob", "email": "bob@test.com", "password" : "1234", "img": None},
    {"id": 3, "name": "Carol", "email": "carol@test.com", "password" : "1234", "img": None},
]


# 모든 사용자 조회
def get_users():
    return _users.copy() # 외부에서 수정 방지

def get_user_by_id(user_id: int):
    return next((u for u in _users if u["id"] == user_id), None)

def get_user_by_name(name:str):
    return next((u for u in _users if u["name"]==name), None)

def get_user_by_email(email:str):
    return next((u for u in _users if u["email"]==email), None)

def add_user(user: dict):
    _users.append(user)
    return user

def get_user_pwd(email: str):
    user  = next((u for u in _users if u["email"]==email), None)
    if user:
        return user["password"]
    return None

def update_user(user_id: int, updates: dict):
    for i, user in enumerate(_users):
        if user["id"] == user_id:
            _users[i].update(updates)
            return _users[i]
    return None

def delete_user(user_id: int):
    for i, user in enumerate(_users):
        if user["id"] == user_id:
            del_user = _users.pop(i)
            return del_user
    return None
    
                 