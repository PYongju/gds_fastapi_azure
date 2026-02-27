from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()


# templates 폴더를 만들어서 HTML 파일을 넣을 겁니다.
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    # 접속 시 templates/index.html 파일을 보여줍니다.
    return templates.TemplateResponse("index.html", {"request": request})

class Comment(BaseModel):
    content: str
    user: str

@app.post("/comments")
async def create_comment(comment: Comment):
    print(f"받은 데이터: {comment}") # 서버 로그에서 확인 가능
    return {"status": "success", "received": comment.content}