from fastapi import FastAPI

from src.app.routers import shop
from src.settings import static


app = FastAPI()
app.mount(path='/static', app=static, name='static')

app.include_router(router=shop.router)
