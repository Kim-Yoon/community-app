# controllers/post_controller.py
from fastapi import HTTPException
from models import user_model, post_model
from datetime import datetime

#게시글 목록 조회
def get_posts():
    posts=post_model.get_posts()
    if not posts:
        raise HTTPException(status_code=404, detail="no_posts_found")
    return {"data" : posts}

#특정 게시물 상세 조회
def get_post(post_id:int):
    if post_id <= 0:
        raise HTTPException(status_code=400, detail="invalid_post_id")
        
    post=post_model.get_post_by_id(post_id)  
    if not post:
        raise HTTPException(status_code=404, detail="no_post_found")
    return {"data": post}

#게시물 작성
def upload_post(data : dict, user_id: int):
    title  =  data.get("title")
    content = data.get("content")
    img =  data.get("img")

    # user_id 유효성 검증
    if not user_id or user_id <= 0:
        raise HTTPException(status_code=400, detail="invalid_user_id")

    # 필수 필드 검증
    if not title or not content:
        raise HTTPException(status_code=400, detail="missing_required_fields")

    # 사용자 존재 확인
    user = user_model.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user_not_found")

    posts = post_model.get_posts()
    new_id = max([p["id"] for p in posts], default=0) + 1

    new_post = {
        "id" : new_id,
        "user_id" : user["id"],
        "user_name":  user["name"], 
        "title" : title, 
        "content": content, 
        "img" : img,
        "count" : 0,
        "created_at" : datetime.now().isoformat(),
        "updated_at" : datetime.now().isoformat()
               }  
    post_model.upload_post(new_post)

    return {"data":new_post, "message":"uploade_new_post"}

# 게시물 수정
def update_post(post_id: int, data: dict, user_id: int):
    updates = {}

    # post_id 유효성 검증
    if not post_id or post_id <= 0:
        raise HTTPException(status_code=400, detail="invalid_post_id")

    # 2. 사용자 존재 확인 ⭐ 권장
    print(user_id)
    user = user_model.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user_not_found")

    # 권한 확인
    post = post_model.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="post_not_found")
    
    if post["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="forbidden")

    title  =  data.get("title")
    content = data.get("content")
    img =  data.get("img")

    # 5. 최소 하나의 필드있는지 확인
    if not title and not content and img is None:
        raise HTTPException(status_code=400, detail="no_fields_to_update")

    if title is not None:  # title이 제공된 경우만
        title = title.strip()
        updates["title"] = title

    if content is not None:  # content가 제공된 경우만
        content = content.strip()
        updates["content"] = content

    if img is not None: # img가 제공된 경우만
        if img and not img.startswith(("http://", "https://")):
            raise HTTPException(status_code=400, detail="invalid_image_url")
        updates["img"] = img

    # 7. 수정 시간 추가
    updates["updated_at"] = datetime.now().isoformat() 
    updates_post = post_model.update_post(updates, post_id)
    if not updates_post:
        raise HTTPException(status_code=500, detail="update_failed")

    return {"message" : "post_updateed_succesfully", "data": updates_post}

def delete_post(post_id: int, user_id: int):
    # post_id 유효성 검증
    if not post_id or post_id <= 0:
        raise HTTPException(status_code=400, detail="invalid_post_id")

    # 권한 확인
    post = post_model.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="post_not_found")
    
    if post["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="forbidden")

    del_user = post_model.delete_post(post_id)
    if not del_user:
        raise HTTPException(status_code=500, detail="delete_failed")

    return {"message": "post_deleted_successfully"}
    




    