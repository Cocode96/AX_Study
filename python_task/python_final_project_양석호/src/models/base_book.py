class Book:
    def __init__(self, name: str, writer: str, isbn: str):
        self.__book_name = name
        self.__book_writer = writer
        self.__isbn = isbn

    def __str__(self) -> str:
        return self.get_details()

    def __repr__(self) -> str:
        return (
            f"Book(name={self.__book_name!r}, "
            f"writer={self.__book_writer!r}, isbn={self.__isbn!r})"
        )

    def get_details(self) -> str:
        return (
            f"도서명: {self.__book_name}, 저자: {self.__book_writer}, "
            f"ISBN: {self.__isbn}"
        )

    def get_book_name(self) -> str:
        return self.__book_name

    def get_book_writer(self) -> str:
        return self.__book_writer

    def get_isbn(self) -> str:
        return self.__isbn
