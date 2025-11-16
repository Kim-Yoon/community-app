#model/comment_model.py
from fastapi import APIRouter, Depends
from controllers import comment_controller
from utils.auth import get_current_user_id

_comments = [
    {"id":1 ,"post_id": 1, "user_id": 2, "content": "good"}
]

#댓글 작성
def add_comment(new_comment: dict):
    _comments.append(new_comment)
    return _comments

#특정 댓글 조회
def get_comment_by_id(comment_id : int):
    return next((c for c in _comments if c["id"] == comment_id), None)

#댓글 업데이트
def update_comment(comment_id:int, updated_comment: dict):
    for i, comment in enumerate(_comments):
        if comment["id"] == comment_id:
            _comments[i] = updated_comment
            return _comments[i]
    return None
    

#댓글 삭제
def delete_comment(comment_id: int):
    for i, comment in enumerate(_comments):
        if comment["id"] == comment_id:
            return _comments.pop(i)
    return None

# 특정 게시글의 댓글 목록 (페이징)
def get_comments_by_post_id(post_id: int, page: int = None, limit: int = None):
    post_comments = [c for c in _comments if c["post_id"] == post_id]
    
    # 최신순 정렬
    post_comments.sort(key=lambda x: x["created_at"], reverse=True)

    # 페이징 여부 확인
    if page is None or limit is None:
        # 전체 반환
        return {
            "comments": post_comments,
            "total": len(post_comments),
            "page": None,
            "limit": None
        }
    
    # 페이징
    start = (page - 1) * limit
    end = start + limit
    
    return {
        "comments": post_comments[start:end],  # ✅ dict로 감싸기
    }
    
