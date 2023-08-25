import typing

from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.authentication import AuthCredentials
from starlette.middleware.authentication import AuthenticationBackend
from starlette.requests import HTTPConnection

from src.models import User
from src.settings import SETTINGS


class JWTAuthenticatedBackend(AuthenticationBackend):
    async def authenticate(
        self, conn: HTTPConnection
    ) -> typing.Optional[typing.Tuple["AuthCredentials", User]]:
        auth = conn.headers.get("Authorization") \
            if 'Authorization' in conn.headers \
            else conn.headers.get("authorization")

        if not auth or not auth.startswith(f"{SETTINGS.TOKEN_TYPE}"):
            return

        token = auth.replace(f"{SETTINGS.TOKEN_TYPE} ", "")
        try:
            payload = jwt.decode(
                token,
                SETTINGS.SECRET_KEY.get_secret_value(),
                algorithms=[SETTINGS.ALGORITHM]
            )
        except JWTError:
            return
        else:
            with User.session() as session:  # type: Session
                user: User = session.scalar(
                    select(User)
                    .filter_by(id=payload.get("sub"))
                )

                if not user:
                    return

                return AuthCredentials(["authenticated"]), user
