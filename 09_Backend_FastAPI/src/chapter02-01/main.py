import logging

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field, field_validator, model_validator, ValidationError
from typing import Optional, Self, Generic, TypeVar

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("book_api")

T = TypeVar("T", int, str)

app = FastAPI(
    title="도서 API 학습",
    description="요청 검증, 업무 규칙, 응답 모델 실습",
    version="0.1.0",
)


# ── 요청 모델 ──────────────────────────────

class BookCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=100,
        description="등록할 도서 제목",
    )
    author: str = Field(
        min_length=1,
        max_length=50,
        description="도서 저자",
    )
    price : Optional[int] = Field(
        min=0,
        description="도서의 값"
    )

    @field_validator("title", "author")
    @classmethod
    def trim_and_validate(cls, value: str) -> str:
        trimed_text = value.strip()
        if len(trimed_text) < 2:
            raise ValueError("공백없이 2자 이상 입력하세요.")

        return trimed_text

    @model_validator(mode="before")
    def before_validate(self) -> Self:
        logger.info(f"[BEFORE] : {self}")
        return self

    @model_validator(mode="after")
    def after_validate(self) -> Self:
        logger.info(f"[after] : {self}")
        return self

class QuantityRequest(BaseModel):
    quantity: int = Field(
        ge=0,
        description="요청할 상품 수량",
    )


# ── 응답 모델 ──────────────────────────────

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    price : Optional[int]


class QuantityResponse(BaseModel):
    quantity: int = Field(description="검사를 통과한 상품 수량")


# ── 임시 저장소: 서버 재시작 시 초기화 ──────────

books: dict[int, dict] = {}


# ── 도서 등록 ──────────────────────────────

@app.post(
    "/books",
    status_code=status.HTTP_201_CREATED,
    response_model=BookResponse,
    tags=["books"],
    summary="도서 등록",
)
async def create_book(request: BookCreate) -> dict:
    logger.info(f"BookCreate:{request}")
    book = request.model_dump()
    logger.info(f"book={book}, type: {type(book)}, wpahr: {book["title"]}")

    book_id = max(books, default=0) + 1

    book = {
        "id": book_id,
        "title": request.title,
        "author": request.author,
        "price" : request.price,
        "internal_note": "관리자용 메모",
    }

    books[book_id] = book
    logger.info("도서 등록: id=%s, title=%s", book_id, request.title)

    # internal_note는 BookResponse에 없으므로 응답에서 제외됨
    return book


# ── 도서 목록 조회 ──────────────────────────

@app.get(
    "/books",
    response_model=list[BookResponse],
    tags=["books"],
    summary="도서 목록 조회",
)
async def list_books(
    limit: int = Query(default=10, ge=1, le=100),
) -> list[dict]:
    return list(books.values())[:limit]


# ── 도서 단건 조회 ──────────────────────────

@app.get(
    "/books/{book_id}",
    response_model=BookResponse,
    tags=["books"],
    summary="도서 한 권 조회",
)
async def get_book(book_id: int) -> dict:
    book = books.get(book_id)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="도서를 찾을 수 없습니다.",
        )

    return book


# ── 수량 검사: 재고를 차감하지 않는 별도 실습 ─────

@app.post(
    "/quantities",
    response_model=QuantityResponse,
    tags=["quantities"],
    summary="요청 수량 검사",
)
async def check_quantity(request: QuantityRequest) -> dict:
    stock = 5

    # ge=0 검증을 통과한 뒤 실행되는 업무 규칙
    if request.quantity > stock:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="재고가 부족합니다.",
        )

    logger.info("수량 검사 통과: quantity=%s", request.quantity)

    return {"quantity": request.quantity}