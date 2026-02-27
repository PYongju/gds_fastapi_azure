from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uuid # 게시글에 고유 ID를 부여하기 위해 필요

app = FastAPI()

# 1. CORS 설정 (혹시 모를 브라우저 차단 방지)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 모든 주소 허용 (시연용)
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

# 2. 임시 데이터 저장소 (서버 꺼지기 전까지 유지)
# 시연 중에 글이 바로 사라지지 않게 리스트에 담아둡니다.
posts_db = []

class Comment(BaseModel):
    content: str
    user: str

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/comments")
async def create_comment(comment: Comment):
    # 3. 받은 데이터를 실제 게시글 객체로 변환
    new_post = {
        "id": str(uuid.uuid4())[:8], # 랜덤 ID 생성
        "content": comment.content,
        "user": comment.user,
        "likes": 0
    }
    
    # 서버 로그에 출력
    print(f"✅ 새 게시글 수신: {new_post}")
    
    # DB(리스트)에 저장
    posts_db.insert(0, new_post) 
    
    # 4. 프런트엔드가 바로 화면에 그릴 수 있게 'post' 객체를 포함해서 반환
    return {
        "status": "success", 
        "post": new_post
    }