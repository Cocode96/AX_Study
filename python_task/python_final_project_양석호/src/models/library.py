from .base_book import Book
from .specialized_books import Specialized_books
import datetime as dt

#books = {} # 도서 자체는 딕셔너리를 사용할 듯 
#rental_history = [(),()] # 리스트 튜플로 저장할듯 # 언제 대여했고(when) 무슨책이고(book) 대여인지 반납인지
class Library:

    def __init__(self):
        self.__books : dict[str : Book] = {}
        self.__rental_history = []

    def __str__(self):
        return f"{self.__books}, {self.__rental_history}"

    def __repr__(self):
        return (f"Library(books={self.__books!r}, rental_history={self.__rental_history!r})")

    # 도서 등록
    def add_book(self): # 예외 처리해야함
        print("도서 정보를 입력해주세요.")
        try:
            book_name = input("도서명 : ")
            book_writer = input("저자 : ")
            isbn = input("ISBN : ")
        except Exception as error:
            print("정보를 잘못 입력하셨습니다!", error)

        book = Book(book_name, book_writer, isbn)

        self.__books[isbn] = book

    # 전체 도서 조회
    def show_all_books(self):
        print("전체 도서 조회")
        print(self.__books.items())

    # 도서 검색
    def search_book(self):
        try:
            isbn = input("검색할 도서의 ISBN을 입력해주세요 : ")
        except Exception as error:
            print("잘못입력하셨습니다!", error)

        print(self.__books[isbn])

    # 도서 대여 처리
    def rent_book(self):
        try:
            isbn = input("대여할 도서의 ISBN을 입력해주세요 : ")
        except Exception as error:
            print("잘못입력하셨습니다!", error)

        self.__rental_history.append((dt.datetime.now(), self.__books[isbn].get_name() ,isbn)) # 시간 책이름 isbn까쥐 불변 튜플

    # 도서 반납 처리
    def return_book(self): # history control append
        try:
            isbn = input("반납할 도서의 ISBN을 입력해주세요 : ")
        except Exception as error:
            print("잘못입력하셨습니다!", error)

        self.__rental_history.append((dt.datetime.now(), self.__books[isbn].get_name() ,isbn)) # 시간 책이름 isbn까쥐 불변 튜플

    # 렌탈 히스토리!
    def show_rental_history(self):
        print(*self.__rental_history)