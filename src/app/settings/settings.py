from pydantic_settings import BaseSettings
from src.app.core.db.database_init import DatabaseHelper

class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str

    rabbitmq_user: str
    rabbitmq_host: str
    rabbitmq_port: str
    rabbitmq_password: str

    api_key: str

    @property
    def db_async_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )
    
    @property
    def broker_url(self) -> str:
        return (
            f"amqp://{self.rabbitmq_user}:{self.rabbitmq_password}@{self.rabbitmq_host}:{self.rabbitmq_port}/"
        )
    
    @property
    def db_helper(self) -> DatabaseHelper:
        return DatabaseHelper(self.db_async_url)


config = Settings() # type: ignore