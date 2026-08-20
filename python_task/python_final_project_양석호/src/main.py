from models.library import Library
from utils import helpers

library_manager = Library()

def main() -> None:
    while True:
        print('='*30)
        print("1. 도서 등록")
        print("2. 전체 도서 조회")
        print("3. 도서 검색")
        print("4. 대여/반납 처리")
        print("5. 종료")
        print('='*30)

        try:
            main_command = int(input("입력 :"))
        except ValueError as e:
            print("숫자를 입력해주세요!")
        else:
            # 해당 문은 함수화나 객체화 시킬 것
            if main_command == 1: # 도서 등록
                library_manager.add_book()
            elif main_command == 2: # 전체 도서 조회
                library_manager.show_all_books()
            elif main_command == 3: # 도서 검색
                library_manager.search_book()
            elif main_command == 4: # 대여/반납 처리
                library_manager.rent_book()
            elif main_command == 5:
                print("종료")
                break

if __name__ == "__main__":
    main()