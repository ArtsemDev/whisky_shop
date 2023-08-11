from sqlalchemy import Column, VARCHAR, DECIMAL, INT, SMALLINT, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class ShopCategory(Base):
    __tablename__ = 'shop_category'

    id = Column(SMALLINT, primary_key=True)
    name = Column(VARCHAR(32), nullable=False, unique=True)
    slug = Column(VARCHAR(32), nullable=False, unique=True)

    products = relationship(argument='Product', back_populates='category')


class Product(Base):
    __tablename__ = 'product'
    __table_args__ = (
        CheckConstraint('price > 0'),
    )

    id = Column(INT, primary_key=True)
    name = Column(VARCHAR(64), nullable=False)
    slug = Column(VARCHAR(64), nullable=False, unique=True)
    descr = Column(VARCHAR(2048), nullable=False)
    price = Column(DECIMAL(precision=8, scale=2), nullable=False)
    category_id = Column(SMALLINT, ForeignKey('shop_category.id', ondelete='CASCADE'), nullable=False, index=True)

    category = relationship(argument='ShopCategory', back_populates='products')
    images = relationship(argument='ProductImage')


class ProductImage(Base):
    __tablename__ = 'product_image'

    id = Column(INT, primary_key=True)
    product_id = Column(INT, ForeignKey(column='product.id', ondelete='CASCADE'), nullable=False)
    image = Column(VARCHAR(128), nullable=False)
