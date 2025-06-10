from pathlib import Path
from dotenv import find_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator


class EnvSettings(BaseSettings):
    class Config:
        env_file: str = find_dotenv()
        extra: str = 'ignore'


class LanggraphConfig(EnvSettings):
    language_model: str = Field('hf.co/t-tech/T-lite-it-1.0-Q8_0-GGUF:latest')
    embedding_model: str = Field('all-minilm:latest')
    similarity_search_k: int = Field(3)
    temperature: float = Field(0.0)
    separators: list[str] = Field(['---'])
    default_doc_file_path: str = Field('')
    splitter_chunk_size: int = Field(200)
    splitter_chunk_overlap: int = Field(100)


    @field_validator('default_doc_file_path', mode='before')
    def default_doc_file_path_validator(cls, value: str) -> str:
        base = Path(__file__).parent.parent
        abs_path = str(base / 'fixtures' /  value)
        return abs_path

    class Config:
        env_prefix = 'langgraph_'


class BotConfig(EnvSettings):
    token: str = Field('bot_token')

    class Config:
        env_prefix = 'bot_'


class PostgresConfig(EnvSettings):
    name: str = Field('postgres')
    host: str = Field('postgres')
    port: str = Field('5432')
    username: str = Field('postgres')
    password: str = Field('password')

    class Config:
        env_prefix = 'postgres_'


class ChromaConfig(EnvSettings):
    host: str = Field('chroma')
    port: int = Field(8000)

    class Config:
        env_prefix = 'chromadb_'


class Settings(EnvSettings):
    langgraph: LanggraphConfig = LanggraphConfig()
    bot: BotConfig = BotConfig()
    db_postgres: PostgresConfig = PostgresConfig()
    db_chroma: ChromaConfig = ChromaConfig()


class SettingsSingleton:
    _instance: Settings = None

    @classmethod
    def get_instance(cls) -> Settings:
        if cls._instance is None:
            cls._instance = Settings()
        return cls._instance
