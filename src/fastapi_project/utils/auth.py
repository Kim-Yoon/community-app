from fastapi import Header, HTTPException

def get_current_user_id(user_id: int = Header(alias="X-User-ID")) -> int:
    if user_id <= 0:
        raise HTTPException(status_code=400, detail="invalid_user_id")
    return user_id