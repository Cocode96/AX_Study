from .base_book import Book


class SpecializedBook(Book):
    def __init__(self, name: str, writer: str, isbn: str, book_type: str):
        super().__init__(name, writer, isbn)
        self.__book_type = book_type

    def get_details(self) -> str:
        return f"{super().get_details()}, 유형: {self.__book_type}"

    def __repr__(self) -> str:
        return (
            f"SpecializedBook(name={self.get_book_name()!r}, "
            f"writer={self.get_book_writer()!r}, isbn={self.get_isbn()!r}, "
            f"book_type={self.__book_type!r})"
        )
