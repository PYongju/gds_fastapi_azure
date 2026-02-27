from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 허용할 주소 목록
origins = [
    "http://localhost:3000", # 로컬 테스트용
    "https://proud-ocean-029307b00.1.azurestaticapps.net", # 배포된 리액트 주소 (반드시 본인 것으로 수정!)
]

# 중요: UI(Static Web Apps)에서 요청을 보낼 때 차단되지 않도록 CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # 모든 방식(GET, POST 등) 허용
    allow_headers=["*"], # 모든 헤더 허용
)

class Comment(BaseModel):
    content: str
    user: str

@app.post("/comments")
async def create_comment(comment: Comment):
    print(f"받은 데이터: {comment}") # 서버 로그에서 확인 가능
    return {"status": "success", "received": comment.content}