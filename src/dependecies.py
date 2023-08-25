from sqlalchemy import select
from fastapi import Depends, Header, HTTPException
from starlette import status
from starlette.requests import Request

from src.models import ShopCategory, Base
from src.settings import SETTINGS
from src.utils import verify_token


def _get_db_session():
    session = Base.session()
    try:
        yield session
    finally:
        session.close()


def _get_categories():
    with ShopCategory.session() as session:
        return session.scalars(
            select(ShopCategory)
            .order_by(ShopCategory.name)
        ).all()


def _is_authenticated(request: Request):
    if not request.user.is_authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


is_authenticated = Depends(_is_authenticated)
get_categories = Depends(_get_categories)
get_db_session = Depends(_get_db_session)
