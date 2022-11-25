from pydantic import BaseSettings


class Settings(BaseSettings):
    db_name: str
    db_password: str
    db_user: str

    class Config:
        env_file = ".env"


settings = Settings()
