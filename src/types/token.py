from pydantic import BaseModel, Field

from src.settings import SETTINGS


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = Field(default=SETTINGS.TOKEN_TYPE)
    expire: int = SETTINGS.EXP_ACCESS_TOKEN * 60
