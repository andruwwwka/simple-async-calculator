from pydantic import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения"""

    db_name: str
    db_password: str
    db_user: str
    db_host: str

    class Config:  # pylint: disable=too-few-public-methods,missing-class-docstring
        env_file = ".env"


settings = Settings()
