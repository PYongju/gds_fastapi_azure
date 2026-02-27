from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실습 중에는 모두 허용, 나중에는 UI 주소만!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/test-data")
async def recive_data(data:dict):
    print(f"받은 데이터: {data}")
    return {"status": "success", "received": data}

@app.get("/")
def read_root():
    return {"message": "Hello Azure! Our FastAPI is running!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}