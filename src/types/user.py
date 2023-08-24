from fastapi import Form
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

from src.models import User
from src.settings import pwd_context


class LoginForm(BaseModel):
    email: EmailStr = Field(default=...)
    password: str = Field(default=..., min_length=8, max_length=64)

    @field_validator('email')
    def email_validator(cls, value: str):
        with User.session() as session:
            user = session.query(User).filter_by(email=value).first()
            if not user:
                raise ValueError('user not found')
            return value

    @model_validator(mode='after')
    def validator(self):
        with User.session() as session:
            user = session.query(User).filter_by(email=self.email).first()
            if not pwd_context.verify(self.password, user.password):
                raise ValueError('password is not correct')
        return self

    @classmethod
    def as_form(cls, email: str = Form(...), password: str = Form(...)):
        return cls(email=email, password=password)


class RegisterForm(LoginForm):
    confirm_password: str = Field(default=..., min_length=8, max_length=64)

    @field_validator('email')
    def email_validator(cls, value: str):
        with User.session() as session:
            user = session.query(User).filter_by(email=value).first()
            if user:
                raise ValueError('email is not unique')
            return value

    @model_validator(mode='after')
    def validator(self):
        if self.password != self.confirm_password:
            raise ValueError
        return self

    @classmethod
    def as_form(cls, email: str = Form(...), password: str = Form(...), confirm_password: str = Form(...)):
        return cls(email=email, password=password, confirm_password=confirm_password)
