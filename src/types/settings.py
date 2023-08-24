from pydantic import PostgresDsn, ConfigDict, SecretStr, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(
        frozen=True
    )

    DATABASE_URL: PostgresDsn
    SECRET_STR: SecretStr
    TOKEN_TYPE: str
    EXP_ACCESS_TOKEN: int
    EXP_REFRESH_TOKEN: int
    ALGORITHM: str = Field(default='HS256')
