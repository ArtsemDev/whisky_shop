from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .settings import SETTINGS


class Base(DeclarativeBase):
    engine = create_engine(url=SETTINGS.DATABASE_URL.unicode_string())
    session = sessionmaker(bind=engine)
