from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage

model = init_chat_model(
    model_provider="ollama",
    model="mistral"
)

parser = StrOutputParser()

chain = model | parser

city = input("여행하고싶은 여행지를 입력하세요 : ")

messages: list[BaseMessage] = [
    SystemMessage("당신은 친절한 여행 가이드입니다. 방문하는 도시의 대표 관광지 1곳을 추천해주세요."),
    HumanMessage(f"이번 주말에 {city}로 여행을 갑니다.")
]

response = chain.invoke(messages)
print(response)