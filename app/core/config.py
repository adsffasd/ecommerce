from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "E-Commerce API"
    DEBUG: bool = True

    DATABASE_URL: str = "sqlite:///./ecommerce.db"

    class Config:
        env_file = ".env"


settings = Settings()
