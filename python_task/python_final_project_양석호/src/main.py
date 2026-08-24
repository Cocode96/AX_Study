from models.library import Library
from models.specialized_books import SpecializedBook
from utils.helpers import input_menu, input_non_empty, input_book_type


library_manager = Library()


def add_book() -> None:
    print("\n도서 정보를 입력해주세요.")
    name = input_non_empty("도서명: ")
    writer = input_non_empty("저자: ")
    isbn = input_non_empty("ISBN: ")
    book_type = input_book_type("도서 유형(단행본/전자도서 등): ")

    try:
        library_manager.add_book(SpecializedBook(name, writer, isbn, book_type))
    except ValueError as error:
        print(f"등록 실패: {error}")
    else:
        print("도서가 등록되었습니다.")


def show_all_books() -> None:
    books = library_manager.get_all_books()
    if not books:
        print("등록된 도서가 없습니다.")
        return
    print("\n전체 도서")
    for book in books:
        status = "대여 중" if library_manager.is_rented(book.get_isbn()) else "대여 가능"
        print(f"- {book} [{status}]")


def search_book() -> None:
    isbn = input_non_empty("검색할 도서의 ISBN: ")
    try:
        book = library_manager.search_book(isbn)
    except KeyError as error:
        print(error.args[0])
    else:
        status = "대여 중" if library_manager.is_rented(isbn) else "대여 가능"
        print(f"{book} [{status}]")


def rent_or_return_book() -> None:
    print("\n1. 대여")
    print("2. 반납")
    print("3. 대여 이력")
    print("4. 대여 통계")
    print("5. 이전 메뉴")
    command = input_menu("입력: ", {1, 2, 3, 4, 5})

    if command == 5:
        return
    if command == 3:
        show_rental_history()
        return
    if command == 4:
        show_rental_statistics()
        return

    isbn = input_non_empty("ISBN: ")
    try:
        if command == 1:
            library_manager.rent_book(isbn)
            print("대여가 완료되었습니다.")
        else:
            library_manager.return_book(isbn)
            print("반납이 완료되었습니다.")
    except (KeyError, ValueError) as error:
        print(f"처리 실패: {error.args[0]}")


def show_rental_history() -> None:
    history = library_manager.get_rental_history()
    if not history:
        print("대여/반납 이력이 없습니다.")
        return
    print("\n대여/반납 이력")
    for timestamp, book_name, isbn, action in history:
        print(f"- {timestamp: %H:%M:%S} | {action} | {book_name} | {isbn}")


def show_rental_statistics() -> None:
    statistics = library_manager.get_rental_statistics()
    if not statistics:
        print("집계할 대여 기록이 없습니다.")
        return
    print("\n도서별 누적 대여 횟수")
    for book_name, count in statistics:
        print(f"- {book_name}: {count}회")


# main 입니당
def main() -> None:
    while True:
        print("\n" + "=" * 30)
        print("1. 도서 등록")
        print("2. 전체 도서 조회")
        print("3. 도서 검색")
        print("4. 대여/반납 처리")
        print("5. 종료")
        print("=" * 30)

        command = input_menu("입력: ", {1, 2, 3, 4, 5})
        if command == 1:
            add_book()
        elif command == 2:
            show_all_books()
        elif command == 3:
            search_book()
        elif command == 4:
            rent_or_return_book()
        else:
            print("프로그램을 종료합니다.")
            break


if __name__ == "__main__":
    main()
