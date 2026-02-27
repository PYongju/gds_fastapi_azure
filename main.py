from fastapi import FastAPI, Request, Depends
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

# 우리가 만든 파일들 불러오기
from database import get_db, engine
import models

# 서버 시작 시 테이블 생성 (이미 있다면 무시됨)
# models.Base.metadata.create_all(bind=engine) 

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Pydantic 모델: 프론트엔드에서 보내는 데이터 형식
class ContentRequest(BaseModel):
    content: str
    user: str  # 현재는 이름으로 받지만, DB 저장 시에는 user_id가 필요합니다.
    post_id: Optional[int] = None  # DBML에 따라 int로 변경

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    # DB에서 최신순으로 게시글을 가져오고, 연관된 댓글도 함께 가져옵니다.
    # models.py에 relationship을 설정했기 때문에 자동으로 불러올 수 있습니다.
    posts = db.query(models.Post).order_by(models.Post.id.desc()).all()
    return posts

@app.post("/comments")
async def handle_request(item: ContentRequest, db: Session = Depends(get_db)):
    # [중요] DBML 제약조건 때문에 users 테이블에 id=1인 유저가 반드시 있어야 합니다.
    # 만약 유저가 없다면 아래 로직은 에러가 납니다.
    test_user_id = 1 

    # 1. 댓글 작성 로직 (post_id가 있을 때)
    if item.post_id:
        new_comment = models.Comment(
            post_id=item.post_id,
            user_id=test_user_id,
            content=item.content,
            created_at=datetime.now(),
            label="safe" # 기본값
        )
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        return {"status": "success", "type": "comment", "comment": new_comment}
    
    # 2. 게시글 작성 로직 (post_id가 없을 때)
    new_post = models.Post(
        title="새로운 게시글", # DBML에 title이 필수이므로 추가
        body=item.content,    # DBML의 body 컬럼에 매칭
        user_id=test_user_id,
        status="active",
        created_at=datetime.now()
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    # 프론트엔드 형식을 맞추기 위해 딕셔너리로 반환
    return {
        "status": "success", 
        "type": "post", 
        "post": {
            "id": new_post.id,
            "user": item.user,
            "content": new_post.body,
            "comments": []
        }
    }