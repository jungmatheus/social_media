from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_USERNAME: str = "postgres"
    DATABASE_NAME: str
    DATABASE_PASSWORD: str
    SECRET_KEY: str
    DATABASE_HOSTNAME: str = "localhost"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str

    class Config:
        env_file = '.env'
settings = Settings()

