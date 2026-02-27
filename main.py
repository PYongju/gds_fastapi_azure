from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Optional
import uuid

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 임시 DB: 게시글 안에 댓글 리스트가 포함된 구조
posts_db = []

class ContentRequest(BaseModel):
    content: str
    user: str
    post_id: Optional[str] = None  # post_id가 있으면 '댓글', 없으면 '게시글'

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/comments")
async def handle_request(item: ContentRequest):
    # 1. 댓글 작성 로직
    if item.post_id:
        for post in posts_db:
            if post["id"] == item.post_id:
                new_comment = {"user": item.user, "content": item.content}
                post["comments"].append(new_comment)
                return {"status": "success", "type": "comment", "comment": new_comment}
    
    # 2. 게시글 작성 로직
    new_post = {
        "id": str(uuid.uuid4())[:8],
        "user": item.user,
        "content": item.content,
        "comments": []
    }
    posts_db.insert(0, new_post)
    return {"status": "success", "type": "post", "post": new_post}