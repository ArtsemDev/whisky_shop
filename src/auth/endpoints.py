from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.dependecies import get_db_session
from src.settings import pwd_context
from src.types.user import RegisterForm, LoginForm
from src.models import User
from src.utils import create_token

router = APIRouter(prefix='/auth')


@router.post(
    path='/register',
    response_model=RegisterForm,
    response_model_exclude={'password', 'confirm_password'}
)
async def register(form: RegisterForm, session: Session = get_db_session):
    user = User(**form.model_dump(exclude={'password', 'confirm_password'}))
    user.password = pwd_context.hash(form.password)
    session.add(user)
    session.commit()
    return form


@router.post(
    path='/login'
)
async def login(form: LoginForm, session: Session = get_db_session):
    user = session.query(User).filter_by(email=form.email).first()
    access_token = create_token(sub=user.id)
    return {'access_token': access_token}
