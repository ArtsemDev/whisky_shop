from pydantic import PostgresDsn, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(
        frozen=True
    )

    DATABASE_URL: PostgresDsn
