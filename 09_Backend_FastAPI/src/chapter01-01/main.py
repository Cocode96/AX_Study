import logging
from fastapi import FastAPI, HTTPException, Body, status
from pydantic import BaseModel
from book.domain.book import Book

# 기본 로깅 설정

logging.basicConfig(
    level=logging.INFO, #INFO 레벨 이상의 로그만 콘솔에 출력하도록 기준선 지정
    format="%(asctime)s [%(levelname)s] (%(name)s) - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# 로거 인스턴스 생성
logger = logging.getLogger("app")

#FastAPI 핵심 인스턴스 초기화
app = FastAPI()

books = [
    {"id": 1, "title": "Python 기초"},
    {"id": 2, "title": "FastAPI 입문"},
]

class BookCreate(BaseModel):
    title : str

# 기본 엔드포인터 - "/" 설정
@app.get("/hello")
async def hello_world() -> dict:
    # pring 대신 표준 logger를 활용해 정보를 기록합니다.
    logger.info("로깅 연습, Hello World")

    # fastapi가 json문자열로 바꿔간다.
    return {
        "message" : "Hello World"
    }

@app.get("/books/{book_id}")
async def get_books(book_id : int) -> dict:
    for book in books:
        if book["id"] == book_id:
            return book

    # 못찾았을때 예외 던지기
    raise HTTPException(status_code=404, detail="도서를 찾을 수 없습니다.")

@app.post("/books", status_code=201)
async def create_book(new_book : BookCreate) -> dict:
    new_id = max((book["id"] for book in books), default=0) + 1

    book = {
        "id" : new_id,
        "title" : new_book.title,
    }
    books.append(book)
    return book
