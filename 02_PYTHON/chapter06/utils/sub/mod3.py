#from chapter06.utils.sub.mod3 import VERSION # 모듈이 있는 전체 경로로 접근
#from ...mod1 import VERSION # 모듈이 있는 전체 경로로 접근
from mod1 import VERSION

def divide(num1, num2):
    return num1 / num2

def print_version():
    print("현재 버전은 : ", VERSION)