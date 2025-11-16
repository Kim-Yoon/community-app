from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from routers.user_router import router as user_router
from routers.post_router import router as post_router
from routers.comment_router import router as comment_router

app = FastAPI()

#사용자 관련 라우트 등록
app.include_router(user_router, tags=["users"])
app.include_router(post_router, tags=["posts"])
app.include_router(comment_router, tags=["comments"])
