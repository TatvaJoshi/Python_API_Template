from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_TYPE: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DEV_HOST: str
    DEV_PORT: int
    STATUS: str

    class Config:
        env_file = "Settings/Environments/.env.dev"
        env_file_encoding = "utf-8"

def load_config():
    settings = Settings()
    return (
        settings.DATABASE_HOST,
        settings.DATABASE_PORT,
        settings.DATABASE_USER,
        settings.DATABASE_PASSWORD,
        settings.DATABASE_NAME,
    )