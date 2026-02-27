from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 중요: UI(Static Web Apps)에서 요청을 보낼 때 차단되지 않도록 CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://zealous-tree-0db734d00.6.azurestaticapps.net"], # UI 주소 입력
    allow_methods=["*"],
    allow_headers=["*"],
)

class Comment(BaseModel):
    content: str
    user: str

@app.post("/comments")
async def create_comment(comment: Comment):
    print(f"받은 데이터: {comment}") # 서버 로그에서 확인 가능
    return {"status": "success", "received": comment.content}