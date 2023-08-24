from sqlalchemy import select
from fastapi import Depends

from src.models import ShopCategory, Base


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


get_categories = Depends(_get_categories)
get_db_session = Depends(_get_db_session)
