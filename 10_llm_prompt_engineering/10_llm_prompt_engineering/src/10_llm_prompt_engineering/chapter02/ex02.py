from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage

model = init_chat_model(
    model_provider="ollama",
    model="mistral"
)

parser = StrOutputParser()

chain = model | parser

text = input("단어를 입력하세요 : ")

messages: list[BaseMessage] = [
    SystemMessage(" 당신은 엄격한 국어 교사입니다. 입력된 문장의 맞춤법을 수정하여 결과만 간결하게 출력하세요."),
    HumanMessage(f"이번 주말에 {text}로 여행을 갑니다.")
]

response = chain.invoke(messages)
print(response)