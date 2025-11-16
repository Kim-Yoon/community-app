# controllers/comment_controller.py
from fastapi import HTTPException
from models import comment_model, post_model, user_model
from datetime import datetime
    
#특정 게시글의 댓글 목록 
def get_comments_by_post(post_id, page: int = None, limit: int = None):
    
    # 게시글 존재 확인
    post = post_model.get_post_by_id(post_id)
    if not post:
        raise HTTPException(404, detail= "post_not_found")
    
    comments = comment_model.get_comments_by_post_id(post_id)
    
    return {
        "data": {
            "comments": comments["comments"],
            "total": comments["total"],
            "page": page,
            "limit": limit,
            "post_id": post_id
        }
    }

# 댓글 작성
def create_comment(data: dict, user_id: int):

    post_id = data.get("post_id")
    content = data.get("content")
    
    
    if not post_id or not content:
        raise HTTPException(status_code=400, detail="missing_required_fields")
    
    # 게시글 존재 확인
    post = post_model.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="post_not_found")
    
    # 내용 검증
    content = content.strip()
    comments = comment_model.get_comments_by_post_id(post_id)["comments"]
    new_id = max([c["id"] for c in comments], default=0) + 1
    
    new_comment = {
        "id": new_id,
        "post_id": post_id,
        "user_id": user_id,
        "content": content,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    created_comment = comment_model.add_comment(new_comment)
    if not created_comment:
        raise HTTPException(status_code=500, detail="update_failed")
    return {"data": new_comment}


# 댓글 수정
def update_comment(comment_id: int, data: dict, user_id: int):
    post_id = data.get("post_id")
    if not post_id:
        raise HTTPException(status_code=400, detail="missing_required_fields")

    # 댓글 존재 확인
    comment = comment_model.get_comment_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="comment_not_found")
    
    # 권한 확인
    if comment["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="forbidden")
    
    content = data.get("content")
    if not content:
        raise HTTPException(status_code=400, detail="content_required")
    
    content = content.strip()
    
    comment["content"] = content
    comment["updated_at"] = datetime.now().isoformat()
    
    updated_comment = comment_model.update_comment(comment_id, comment)
    if not updated_comment:
        raise HTTPException(status_code=500, detail="update_failed")
    return {"message": "comment_updated_successfully", "data": updated_comment}


# 댓글 삭제
def delete_comment(comment_id: int, user_id: int):
    """댓글 삭제"""
    comment = comment_model.get_comment_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="comment_not_found")
    
    if comment["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="forbidden")
    
    del_comment = comment_model.delete_comment(comment_id)
    if not del_comment:
        raise HTTPException(status_code=500, detail="delete_failed")
    return {"message": "comment_deleted_successfully"}