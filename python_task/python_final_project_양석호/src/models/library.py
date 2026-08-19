from .base_book import Book
from .specialized_books import Specialized_books
import datetime as dt

#books = {} # 도서 자체는 딕셔너리를 사용할 듯 
#rental_history = [(),()] # 리스트 튜플로 저장할듯 # 언제 대여했고(when) 무슨책이고(book) 대여인지 반납인지
class Library:

    def __init__(self):
        self.__books : dict[str, Book] = {}
        self.__rental_history = []
        pass

    def __str__(self):
        return f"{self.__books}, {self.__rental_history}"

    def __repr__(self):
        return (f"Library(books={self.__books!r}, rental_history={self.__rental_history!r})")

    # 도서 등록
    def add_book(self, book):
        pass

    # 전체 도서 조회
    def show_all_books(self):
        pass

    # 도서 검색
    def search_book(self, isbn):
        pass

    # 도서 대여 처리
    def rent_book(self, isbn):
        self.__rental_history.append((dt.now(), self.__books[isbn].get_name() ,isbn)) # 시간 책이름 isbn까쥐
        pass

    # 도서 반납 처리
    def return_book(self, isbn): # 여기도 똑같이 history control
        pass

    # 렌탈 히스토리!
    def rental_history(self):
        pass