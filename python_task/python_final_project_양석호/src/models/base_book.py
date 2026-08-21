class Book:

    def __init__(self, name, writer, isbn):
        self.__book_name = name
        self.__book_writer = writer
        self.__isbn = isbn

    def __str__(self):
        return f"책 이름 : {self.__book_name}, 저자 : {self.__book_writer}, ISBN : {self.__isbn}"

    def __repr__(self):
        return (f"Book(name={self.__book_name!r}, writer={self.__book_writer!r}, isbn={self.__isbn!r})")

    def get_book_name(self):
        return self.__book_name

    def get_book_writer(self):
        return self.__book_writer
    

    def get_isbn(self):
        return self.__isbn