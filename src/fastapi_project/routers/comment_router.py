# router/comment_router.py
from fastapi import APIRouter, Depends, Query
from controllers import comment_controller
from utils.auth import get_current_user_id

router = APIRouter(prefix="/comments")

# @router.get("")
# def get_comments(
#     post_id: int = Query(None, description="특정 게시글 댓글만"),  # ✅ Query 명시
#     page: int = Query(None, ge=1, description="페이지 번호 (생략 시 전체)"),
#     limit: int = Query(None, ge=1, le=100, description="페이지당 개수 (생략 시 전체)") 
# ):
#     return comment_controller.get_comments_by_post(post_id, page, limit)

# 댓글 작성
@router.post("", status_code=201)
def create_comment(data: dict, user_id: int = Depends(get_current_user_id)):
    return comment_controller.create_comment(data, user_id)

# 댓글 수정
@router.patch("/{comment_id}")
def update_comment(
    comment_id: int,
    data: dict,
    user_id: int = Depends(get_current_user_id)
):
    return comment_controller.update_comment(comment_id, data, user_id)

# 댓글 삭제
@router.delete("/{comment_id}")
def delete_comment(comment_id: int, user_id: int = Depends(get_current_user_id)):
    return comment_controller.delete_comment(comment_id, user_id)

