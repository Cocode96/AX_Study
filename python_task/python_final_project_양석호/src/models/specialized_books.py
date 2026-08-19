from .base_book import Book

class Specialized_books(Book):

    def __init__(self, name, writer, isbn, book_type):
        super().__init__(name, writer, isbn)
        self.__book_type = book_type

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return super().__repr__()
    