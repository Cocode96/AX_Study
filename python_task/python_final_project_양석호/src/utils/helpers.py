# input에 아무것도 들어있지 않을때 처리하는 예외 함수
def input_non_empty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("공백은 입력할 수 없습니다.")

# 메뉴 input로직이 반복되 만든 함수
def input_menu(prompt: str, valid_choices: set[int]) -> int:
    while True:
        try:
            choice = int(input(prompt))
        except ValueError:
            print("숫자를 입력해주세요.")
            continue

        if choice in valid_choices:
            return choice
        print("메뉴에 있는 번호를 입력해주세요.")

# 저자나 도서명은 숫자일 수 있다 특수문자거나 하지만 전자 도서 일반 단행본은 양보못한다잇
def input_book_type(prompt: str)->str:
    while True:
        print("1. 일반 단행본")
        print("2. 전자 도서")

        value = int(input(prompt).strip())

        if value == 1:
            return "일반 단행본"
        elif value == 2:
            return "전자 도서"
        else:
            print("1 또는 2를 입력해주세요.")