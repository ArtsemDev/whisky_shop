from pathlib import Path

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext

from .types import Settings


BASE_DIR = Path(__file__).resolve().parent.parent
SETTINGS = Settings()
templating = Jinja2Templates(directory=BASE_DIR / 'templates')
static = StaticFiles(directory=BASE_DIR / 'static')
media = StaticFiles(directory=BASE_DIR / 'media')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
