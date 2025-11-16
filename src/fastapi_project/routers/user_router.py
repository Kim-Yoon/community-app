#router/user_router.py
from fastapi import APIRouter, Depends
from controllers import user_controller
from utils.auth import get_current_user_id

router = APIRouter(prefix="/users")

##전체 사용자 목록 조회
@router.get("")
def get_users():
    return user_controller.get_users()

# # 특정 사용자 조회 - 모든 유저에게 보여지는 공개 프로필
# @router.get("/{user_id}")
# def get_user(user_id: int):
#     return user_controller.get_user(user_id)

#사용자 생성(201 Created) - 회원가입
@router.post("", status_code=201)
def create_user(data:dict):
    return user_controller.create_user(data)

#login
@router.post("/login")
def login(data:dict):
    return user_controller.login(data)

# 회원정보 불러오기 - 개인 프로필 : 추후에 JWT 도입 예정//
@router.get("/me")
def get_user_info(user_id: int = Depends(get_current_user_id)):
    return user_controller.get_user(user_id)

# 회원정보 수정
@router.patch("/me")
def update_my_info(data: dict, user_id: int = Depends(get_current_user_id)):
    return user_controller.update_my_info(data, user_id)

# 비밀번호 수정
@router.patch("/me/password")
def change_pwd(data:dict, user_id = Depends(get_current_user_id)):
    return user_controller.change_pwd(data, user_id)

# 회원탈퇴
@router.delete("/me")
def delete_user(user_id: int = Depends(get_current_user_id)):
    return user_controller.delete_user(user_id)

