import logging
from typing import Dict, Generic, TypeVar, Annotated, Optional
from datetime import date
from fastapi import FastAPI, Path, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI(title="흐 흐 흐")

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    message: str
    data: T


class BookResponse(BaseModel):
    id: int
    title: str

class BookNotFoundError(Exception):
    pass

@app.exception_handler(BookNotFoundError)
async def handle_book_not_found(request: Request, exc: BookNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "message" : str(exc),
            "data": None,
        }
    )

# ApiResponse에 목록을 전달하고싶으면 list[BookResponse]로하면될거같다. 경매장에서 많이쓸듯?
@app.get("/books/{book_di}", response_model=ApiResponse[BookResponse])
async def get_book(book_id: int):
    if book_id != 1:
        raise BookNotFoundError(f"{book_id}번 도서를 찾을 수 없습니다.")

    return {
        "message": "조회 성공",
        "data": {
            "id": 1,
            "title": "FastAPI 입문",
            "internal_note": "관리자 메모",
        },
    }
