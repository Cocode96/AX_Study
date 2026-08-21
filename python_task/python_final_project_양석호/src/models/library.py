import datetime as dt
from collections import Counter

from .base_book import Book


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

    def add_book(self, book: Book) -> None:
        isbn = book.get_isbn()
        if isbn in self.__isbn_set:
            raise ValueError("이미 등록된 ISBN입니다.")
        self.__books[isbn] = book
        self.__isbn_set.add(isbn)

    def get_all_books(self) -> list[Book]:
        return list(self.__books.values())

    def search_book(self, isbn: str) -> Book:
        if isbn not in self.__books:
            raise KeyError("등록되지 않은 ISBN입니다.")
        return self.__books[isbn]

    def rent_book(self, isbn: str) -> None:
        book = self.search_book(isbn)
        if isbn in self.__rented_isbns:
            raise ValueError("이미 대여 중인 도서입니다.")
        self.__rented_isbns.add(isbn)
        self.__record_history(book, "대여")

    def return_book(self, isbn: str) -> None:
        book = self.search_book(isbn)
        if isbn not in self.__rented_isbns:
            raise ValueError("대여 중인 도서가 아닙니다.")
        self.__rented_isbns.remove(isbn)
        self.__record_history(book, "반납")

    def is_rented(self, isbn: str) -> bool:
        return isbn in self.__rented_isbns

    def get_rental_history(self) -> list[tuple[dt.datetime, str, str, str]]:
        return list(self.__rental_history)

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
