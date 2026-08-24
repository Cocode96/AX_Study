import datetime as dt
from collections import Counter

from .base_book import Book

# 해당 클래스는 main 함수가 비대해지기 싫어 만든 Book class의 정보를 입력 수정 조회 처리해주는 model을 처리해주는 persenter이다.
# 여담으로 python 반환값이 모호해 명시하는 쪽을 선택했다..(난 c++을 좋아하니까..)
class Library:
    def __init__(self):
        # 딕셔너리는 ISBN으로 도서를 바로 찾기 위해 사용한다.
        self.__books: dict[str, Book] = {}
        # 집합은 ISBN 중복과 대여 상태를 빠르게 검사하기 위해 사용한다.
        self.__isbn_set: set[str] = set()
        self.__rented_isbns: set[str] = set()
        # 이력 한 건은 변경되면 안 되므로 튜플로 만들고 순서를 위해 리스트에 저장한다.
        self.__rental_history: list[tuple[dt.datetime, str, str, str]] = []

    def __str__(self) -> str:
        return f"등록 도서: {len(self.__books)}권, 대여 중: {len(self.__rented_isbns)}권"

    def __repr__(self) -> str:
        return (
            f"Library(books={self.__books!r}, "
            f"rented_isbns={self.__rented_isbns!r}, "
            f"rental_history={self.__rental_history!r})"
        )

    # isbn 조회 후 Book 객체를 등록
    def add_book(self, book: Book) -> None:
        isbn = book.get_isbn()
        if isbn in self.__isbn_set:
            raise ValueError("이미 등록된 ISBN입니다.")
        self.__books[isbn] = book
        self.__isbn_set.add(isbn)

    # 전체 Book 인스턴스 조회
    def get_all_books(self) -> list[Book]:
        return list(self.__books.values())

    # isbn기반으로 Book 인스턴스 조회
    def search_book(self, isbn: str) -> Book:
        if isbn not in self.__books:
            raise KeyError("등록되지 않은 ISBN입니다.")
        return self.__books[isbn]

    # isbn기반으로 Book 인스턴스 대여 처리 및 기록
    def rent_book(self, isbn: str) -> None:
        book = self.search_book(isbn)
        if isbn in self.__rented_isbns:
            raise ValueError("이미 대여 중인 도서입니다.")
        self.__rented_isbns.add(isbn)
        self.__record_history(book, "대여")

    # isbn기반으로 Book 인스턴스 반납 처리 및 기록
    def return_book(self, isbn: str) -> None:
        book = self.search_book(isbn)
        if isbn not in self.__rented_isbns:
            raise ValueError("대여 중인 도서가 아닙니다.")
        self.__rented_isbns.remove(isbn)
        self.__record_history(book, "반납")

    # 위 두 함수에 자주쓰이는 비교 로직 함수화
    def is_rented(self, isbn: str) -> bool:
        return isbn in self.__rented_isbns

    # rental history 반환
    def get_rental_history(self) -> list[tuple[dt.datetime, str, str, str]]:
        return list(self.__rental_history)

    # 따로 로직을 만들 수도 있겠지만 Counter 클래스가 이미 collaction에 있어 사용해 보았다.
    # 제네레이터 표현식으로 Counter에 전달해주면 이터레이터의 각 원소별 개수를 준다.
    def get_rental_statistics(self) -> list[tuple[str, int]]:
        rental_counts = Counter(
            book_name
            for _, book_name, _, action in self.__rental_history
            if action == "대여"
        )
        return rental_counts.most_common()

    def __record_history(self, book: Book, action: str) -> None:
        self.__rental_history.append(
            (dt.datetime.now(), book.get_book_name(), book.get_isbn(), action)
        )
