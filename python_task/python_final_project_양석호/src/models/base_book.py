# 해당 클래스는 도서관리시스템의 책의 정보를 담는 클래스로 책의 이름 저자 고유번호인 ISBN을 가지고 조회할 수 있게한다.
class Book:
    def __init__(self, name: str, writer: str, isbn: str):
        self.__book_name = name
        self.__book_writer = writer
        self.__isbn = isbn

    # repr에서 표현식으로 보여줬으니 str호출시 해당 객체가 가지고 있는 정보를 CLI에 보여주기 쉬운 형식으로 사용하겠두아
    def __str__(self) -> str:
        return (
            f"도서명: {self.__book_name}, 저자: {self.__book_writer}, "
            f"ISBN: {self.__isbn}"
        )

    # !r 은 represent형식으로 보여준다는 형식이다 앞으로 유용하게쓸듯?
    def __repr__(self) -> str:
        return (
            f"Book(name={self.__book_name!r}, "
            f"writer={self.__book_writer!r}, isbn={self.__isbn!r})"
        )

    # Book getter, 해당 클래스는 CLI구조상 입력받은 데이터 모델이므로 setter는 따로 만들지 않는다.
    def get_book_name(self) -> str:
        return self.__book_name

    def get_book_writer(self) -> str:
        return self.__book_writer

    def get_isbn(self) -> str:
        return self.__isbn
