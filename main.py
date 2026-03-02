from fastapi import FastAPI, Request, Depends, HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

# 우리가 만든 파일들 불러오기
from database import get_db, engine
import models

# 서버 시작 시 테이블 생성 (이미 있다면 무시됨)
# models.Base.metadata.create_all(bind=engine) 

app = FastAPI()

# 아래 설정을 추가해야 프론트엔드(브라우저)에서 서버로 데이터를 보낼 수 있습니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 곳에서 접속 허용 (테스트용)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# 게시글 전용 Pydantic 모델
class PostCreate(BaseModel):
    content: str
    user: str

# 1. 게시글 생성 전용 길 (/posts)
@app.post("/posts")
@app.post("/posts")
async def create_post(item: PostCreate, db: Session = Depends(get_db)):
    # ⭐️ 아까 SELECT * FROM users; 로 확인한 실제 ID 번호를 넣으세요.
    actual_user_id = 4 

    try:
        new_post = models.Post(
            title="테스트 제목",     # posts 테이블 구조상 NULL 불가일 수 있음
            body=item.content,
            user_id=actual_user_id, # 이 번호가 DB에 없으면 500 에러 발생!
            status="active"
        )
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return {"status": "success", "post": new_post}
    except Exception as e:
        db.rollback()
        print(f"❌ 저장 실패 원인: {str(e)}") # Azure 로그 스트림에 찍힙니다.
        raise HTTPException(status_code=500, detail=str(e))


# 2. 댓글 생성 전용 길 (/comments)
class CommentCreate(BaseModel):
    content: str
    user: str
    post_id: int

@app.post("/comments")
async def create_comment(item: CommentCreate, db: Session = Depends(get_db)):
    test_user_id = 6
    
    new_comment = models.Comment(
        post_id=item.post_id,
        user_id=test_user_id,
        content=item.content,
        toxicity_score=0.0,
        label="safe"
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return {"status": "success", "comment": new_comment}