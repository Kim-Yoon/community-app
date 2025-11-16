from fastapi import APIRouter, Depends, Query
from controllers import post_controller, comment_controller
from utils.auth import get_current_user_id


router = APIRouter(prefix="/posts")

##전체 게시글 목록 조회
@router.get("")
def get_posts():
    return post_controller.get_posts()

# 특정 게시물 조회
@router.get("/{post_id}")
def get_user(post_id: int):
    return post_controller.get_post(post_id)

#게시글 생성(201 Created)
@router.post("", status_code=201)
def upload_post(data:dict, user_id: int = Depends(get_current_user_id)):    
    return post_controller.upload_post(data, user_id)

#게시글 수정
@router.patch("/{post_id}")
def update_post(post_id: int, data: dict, user_id: int = Depends(get_current_user_id)):
    return post_controller.update_post(post_id, data, user_id)

@router.get("/{post_id}/comments")
def get_post_comments(
    post_id: int, # ✅ Query 명시
    page: int = Query(None, ge=1, description="페이지 번호 (생략 시 전체)"),
    limit: int = Query(None, ge=1, le=100, description="페이지당 개수 (생략 시 전체)") 
):
    return comment_controller.get_comments_by_post(post_id, page, limit)

#게시글 삭제
@router.delete("/{post_id}")
def delete_post(post_id: int, user_id: int = Depends(get_current_user_id)):
    return post_controller.delete_post(post_id, user_id)
    

