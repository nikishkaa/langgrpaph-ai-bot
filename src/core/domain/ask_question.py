from typing import Annotated, TypedDict
from langchain_ollama import ChatOllama
from langgraph.constants import START, END
from langgraph.graph import StateGraph, add_messages
from src.core.domain.memory import get_checkpointer
from src.core.domain.document_service import DocumentService
from src.config import SettingsSingleton

settings = SettingsSingleton.get_instance()


llm = ChatOllama(
    model=settings.langgraph.language_model,
    temperature=settings.langgraph.temperature
)


class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)


def chatbot(state: State) -> State:
    return {'messages': [llm.invoke(state['messages'])]}


graph_builder.add_node('chatbot', chatbot)
graph_builder.add_edge(START, 'chatbot'),
graph_builder.add_edge('chatbot', END),

def ask_question(question: str, thread_id: str) -> str:
    with get_checkpointer() as checkpointer:
        checkpointer.setup()

        graph = graph_builder.compile(checkpointer=checkpointer)
        service = DocumentService()
        context = service.search_with_formatting(question)
        prompt = ('Ты умный ассистент, используй ТОЛЬКО информацию из контекста для ответа на вопрос.\n '
                  f'контекст: {context}\n вопрос:{question}\n')
        user_input = {'messages': [{'role': 'user', 'content': prompt}]}
        config = {'configurable': {'thread_id': thread_id}}
        state = graph.invoke(user_input, config=config)

        if state.get("messages") and len(state["messages"]) > 0:
            last_message = state["messages"][-1]
            return last_message.content
