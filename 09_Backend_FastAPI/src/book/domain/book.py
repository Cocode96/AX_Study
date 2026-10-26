"""
1. 도서 대여점의 도서는 2가지 상태로 관리가 된다.
    (대출중(RENTED), 대출가능(AVAILABLE))
2. 대출중인 도서는 대여가 불가능
3. 소규모 대여점이라서 도서별 재고는 1개씩만 있어서 관리를 하지 않는다.
4. 도서 번호, 제목, 저자의 정보를 확인할 수 있고...
"""

import datetime

class Book:
    def __init__(self, book_id: int, title: str, author: str, status: str = "AVAILABLE"):
        # 도서의 대여 상태값 유효성 검사
        if status not in ["AVAILABLE", "RENTED"]:
            raise ValueError("허용되지 않은 도서 상태입니다. ('AVAILABLE' 또는 'RENTED'만 유효)")

        # 제목이나 저자 이름이 공백인 경우를 차단
        if not title or not title.strip():
            raise ValueError("도서의 제목은 공백일 수 없습니다.")
        if not author or not author.strip():
            raise ValueError("도서의 저자는 공백일 수 없습니다.")

        self.id = book_id
        self.title = title.strip()
        self.author = author.strip()
        self.status = status
        self.created_at = datetime.datetime.now()

    def update_details(self, title: str, author: str, status: str) -> None:
        """
        기존 도서 정보를 새로운 내용으로 갱신하는 비즈니스 메서드입니다.
        """
        if status not in ["AVAILABLE", "RENTED"]:
            raise ValueError("허용되지 않은 도서 상태로 변경을 시도했습니다.")
        if not title or not title.strip():
            raise ValueError("수정할 도서 제목은 비어 있을 수 없습니다.")
        if not author or not author.strip():
            raise ValueError("수정할 도서 저자는 비어 있을 수 없습니다.")

        self.title = title.strip()
        self.author = author.strip()
        self.status = status

    def to_dict(self) -> dict:
        """
        네트워크로 전송할 수 있도록 도메인 객체를 기본 딕셔너리로 가공합니다.
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }
