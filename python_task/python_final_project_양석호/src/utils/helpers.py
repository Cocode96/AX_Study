def input_non_empty(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("공백은 입력할 수 없습니다.")


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
