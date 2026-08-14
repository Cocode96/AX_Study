def add(num1, num2):
    return num1 + num2

def minus(num1, num2):
    return num1 - num2

VERSION = "1.0.0" # 바뀌고 싶지않은 const 상수 변수의 이름은 대문자로쓴다 전처리와 비슷한 규칙을 따르는듯?

if __name__ == "__main__": # 터미널에서 파이썬 파일을 실행할때로 한정
    print("모듈명 : ", __name__) # 모듈명 :  mod1

    result = add(1, 2)
    print("결과 : ", result)