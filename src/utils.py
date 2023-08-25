from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import jwt, JWTError
from starlette import status

from .settings import SETTINGS


def create_token(sub: str, type_: str = 'access'):
    return jwt.encode(
        claims={
            'sub': sub,
            'exp': datetime.utcnow() + timedelta(minutes=SETTINGS.EXP_ACCESS_TOKEN),
            'type': type_
        },
        key=SETTINGS.SECRET_STR.get_secret_value(),
        algorithm=SETTINGS.ALGORITHM
    )


def verify_token(token: str):
    try:
        payload = jwt.decode(
            token=token,
            key=SETTINGS.SECRET_STR,
            algorithms=SETTINGS.ALGORITHM
        )
    except JWTError:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='token is invalid or expired')
    else:
        return payload
