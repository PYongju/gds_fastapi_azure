from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

# UI에서 보내는 데이터 구조와 똑같이 만듭니다.
class PostData(BaseModel):
    content: str
    author: str = "익명"  # 기본값 설정 가능
    nudge_level: str = "safe"
    probability: float = 0.0

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실습 중에는 모두 허용, 나중에는 UI 주소만!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/posts")
async def create_post(data: PostData):
    # ==========================================
    # 여기가 터미널에 출력하는 부분입니다!
    # ==========================================
    print("\n" + "="*50)
    print("📢 UI에서 새로운 댓글이 도착했습니다!")
    print(f"📝 내용: {data.content}")
    print(f"👤 작성자: {data.author}")
    print(f"🚨 넛지 레벨: {data.nudge_level}")
    print(f"📊 확률: {data.probability}")
    print("="*50 + "\n")
    
    # 나중에 여기서 Azure SQL 저장 로직을 넣으면 됩니다.
    return {"status": "success", "received_content": data.content}

@app.get("/")
def read_root():
    return {"message": "Hello Azure! Our FastAPI is running!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}