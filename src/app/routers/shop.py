from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.requests import Request

from src.settings import templating


router = APIRouter(
    prefix='/shop',
    include_in_schema=False
)


@router.get(path='/', response_class=HTMLResponse, name='shop_index')
async def index(request: Request):
    return templating.TemplateResponse(
        name='app/shop.html',
        context={
            'request': request
        }
    )
