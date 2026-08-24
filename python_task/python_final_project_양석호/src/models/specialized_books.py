from .base_book import Book

# 해당 클래스는 book의 타입 즉 전자 도서, 일반 단행본을 type별로 나눠 Book클래스를 상속받는 클래스다.
# 딱히 요구사항에 전자도서와 일반 단행본을 통해 뭘 하라는건 없어 상속 클래스 뼈대만 남긴다.
class SpecializedBook(Book):
    def __init__(self, name: str, writer: str, isbn: str, book_type: str):
        super().__init__(name, writer, isbn)
        self.__book_type = book_type

    def __str__(self):
        return f"{super().__str__()}, 유형: {self.__book_type}"

    def __repr__(self) -> str:
        return (
            f"SpecializedBook(name={self.get_book_name()!r}, "
            f"writer={self.get_book_writer()!r}, isbn={self.get_isbn()!r}, "
            f"book_type={self.__book_type!r})"
        )
