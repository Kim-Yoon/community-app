# controllers/user_controller.py
from fastapi import HTTPException
from models import user_model
from utils.password import hash_password
from datetime import datetime
import bcrypt
import asyncio
import uuid


#사용자 목록 조회
def get_users():
    users=user_model.get_users()
    if not users:
        raise HTTPException(staus_code=404, detail="no_users_found")
    return {"data" : users}

#특정 사용자 조회
def get_user(user_id:int):
    if user_id <= 0:
        raise HTTPException(staus_code=400, detail="invalid_user_id")
        
    user = user_model.get_user_by_id(user_id)  
    if not user:
        raise HTTPException(staus_code=404, detail="no_user_found")
    return {"data": user}

#사용자 생성 - 회원가입
def create_user(data : dict):
    name = data.get("name")
    email = data.get("email")
    pwd = data.get("password")
    img = data.get("img")
    saltRounds = 10

    if not name or not email or not pwd:
        raise HTTPException(status_code=400, detail="missing_required_fields")

    if user_model.get_user_by_email(email):
        raise HTTPException(status_code=409, detail="email_already_exists")

    #비밀번호 암호화
    hashed_pwd = hash_password(pwd, saltRounds)

    users = user_model.get_users()
    new_id = max([u["id"] for u in users], default=0) + 1

    #사용자 정보 저장
    new_user = {"id" : new_id,
                "name" : name,
                "email" : email,
                "password": hashed_pwd,
                "created_at" : datetime.now().isoformat(),
                "updated_at" : datetime.now().isoformat(),
               }
    
    user_model.add_user(new_user)
    return {"data":new_user}

def login(data : dict):
    email = data.get("email")
    pwd = str(data.get("password"))
    
    if not email or not pwd:
        raise HTTPException(status_code=400, detail="missing_required_fields")

    user = user_model.get_user_by_email(email)

    #이메일로 사용자 검색
    if not user:
        raise HTTPException(status_code=401, detail="unauthorized")

    #비밀번호 검증
    match = bcrypt.checkpw(pwd.encode("utf-8"), user["password"].encode("utf-8"))     
    if not match:
        raise HTTPException(status_code=401, detail="unauthorized")

    #로그인 성공 시
    return {"data": {"user_id": user["id"], "user_name": user["name"]}}

# 회원정보 수정
def update_my_info(data: dict, user_id: int):
    updates = {}
    name = data.get("name")
    img = data.get("img")

    
    # 아무것도 안보내면 에러 발생
    if not name and not img:
        raise HTTPException(status_code=400, detail="no_fields_to_update")

    # 사용자 존재 확인
    user = user_model.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="no_user_found")

    if name:
        if len(name.strip()) == 0:
            raise HTTPException(status_code=400, detail="name_cannot_be_empty")

        existing_user = user_model.get_user_by_name(name)
        if existing_user and existing_user["id"] != user_id:
            raise HTTPException(status_code=409, detail="name_already_exists")
                
        updates["name"] = name.strip()

    if img:
        updates["img"] = img

    updates["updated_at"] = datetime.now().isoformat()
    updates_user = user_model.update_user(user_id, updates)
    if not updates_user:
        raise HTTPException(status_code=400, detail="update_failed")
        
    return {"message": "update_user_info_successfully"}

# 회원 비밀번호 수정
def change_pwd(data: dict, user_id: int):
    new_pwd = data.get("new_password")
    updates= {}

    # 아무것도 안보내면 에러 발생
    if not new_pwd:
        raise HTTPException(status_code=400, detail="no_fields_to_update")

    # 사용자 존재 확인
    user = user_model.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="no_user_found")

    # 비밀번호 암호화
    hashed_password = hash_password(new_pwd)
    
    updates["password"] = hashed_password
    updates_user = user_model.update_user(user_id, updates)
    if not updates_user:
        raise HTTPException(status_code=400, detail="update_fail")
    return {"message": "change_pwd_successfully"}

# 회원정보 탈퇴
def delete_user(user_id: int):
    # 사용자 존재 확인
    user = user_model.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="no_user_found")

    del_user = user_model.delete_user(user_id)
    if not del_user:
        raise HTTPException(status_code=500, detail="delete_failed")
    
    return {"message": "account_deleted_successfully"}

    
                


    

        
    