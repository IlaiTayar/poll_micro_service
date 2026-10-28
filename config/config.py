
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    MYSQL_USER: str = "ilai"
    MYSQL_PASSWORD: str = "123456789"
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3309
    MYSQL_DATABASE: str = "main"

    DATABASE_URL: str = f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

    USER_SERVICE_URL: str = "http://localhost:8000"