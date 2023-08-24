from math import ceil

from fastapi import APIRouter, Path, Query
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.sql.functions import count

from src.dependecies import get_categories
from src.models import ShopCategory, Product, ProductImage
from src.settings import templating

router = APIRouter(
    prefix='/shop',
    include_in_schema=False
)


@router.get(path='/', response_class=HTMLResponse, name='shop_index')
async def index(
        request: Request,
        page: int = Query(default=1),
        q: str = Query(default=None),
        categories: list[ShopCategory] = get_categories
):
    with ShopCategory.session() as session:
        objs_count = session.scalar(
            select(count(Product.id))
        )
        max_page = ceil(objs_count / 6)
        sql = select(
            Product, ProductImage
        ).join(ProductImage).order_by(
            Product.name
        ).limit(6).offset(page * 6 - 6)
        if q is not None:
            sql = sql.filter(Product.name.contains(q))
        products = session.execute(
            sql
        )
        return templating.TemplateResponse(
            name='app/shop.html',
            context={
                'request': request,
                'filters': {
                    'Category': categories
                },
                'products': products.all(),
                'page': page,
                'max_page': max_page
            }
        )


@router.get(
    path='/{slug}',
    response_class=HTMLResponse,
    name='shop_category'
)
async def product_category(
        request: Request,
        slug: str = Path(),
        page: int = Query(default=1),
        q: str = Query(default=None),
        categories: list[ShopCategory] = get_categories
):
    with ShopCategory.session() as session:
        current_category = session.scalar(
            select(ShopCategory)
            .filter_by(slug=slug)
        )
        objs_count = session.scalar(
            select(count(Product.id))
            .filter_by(category_id=current_category.id)
        )
        max_page = ceil(objs_count / 6)
        sql = select(Product, ProductImage).join(ProductImage).order_by(Product.name).limit(6).offset(page * 6 - 6).filter(Product.category_id == current_category.id)

        if q is not None:
            sql = sql.filter(Product.name.contains(q))

        products = session.execute(
            sql
        )
        return templating.TemplateResponse(
            name='app/shop.html',
            context={
                'request': request,
                'filters': {
                    'Category': categories
                },
                'products': products.all(),
                'page': page,
                'max_page': max_page
            }
        )
