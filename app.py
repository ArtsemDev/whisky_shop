from fastapi import FastAPI

from src.app.routers import shop
from src.settings import static, media
from src.auth.endpoints import router


app = FastAPI()
app.mount(path='/static', app=static, name='static')
app.mount(path='/media', app=media, name='media')

app.include_router(router=shop.router)
app.include_router(router=router)
