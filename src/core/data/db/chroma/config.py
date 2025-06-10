from chromadb import HttpClient
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from src.config import SettingsSingleton


settings = SettingsSingleton.get_instance()

class ChromaSingleton:
    _instance: Chroma = None

    @classmethod
    def get_instance(cls) -> Chroma:
        if cls._instance is None:
            chroma_client = HttpClient(
                host=settings.db_chroma.host,
                port=settings.db_chroma.port,
            )

            cls._instance = Chroma(
                embedding_function=OllamaEmbeddings(model=settings.langgraph.embedding_model),
                client=chroma_client,
            )
        return cls._instance

