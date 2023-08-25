from sqlalchemy import Column, VARCHAR, DECIMAL, INT, SMALLINT, CheckConstraint, ForeignKey, CHAR
from sqlalchemy.orm import relationship
from ulid import new

from .database import Base


class ShopCategory(Base):
    __tablename__ = 'shop_category'

    id = Column(SMALLINT, primary_key=True)
    name = Column(VARCHAR(32), nullable=False, unique=True)
    slug = Column(VARCHAR(32), nullable=False, unique=True)

    products = relationship(argument='Product', back_populates='category')

    def __repr__(self):
        return self.name


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
    category_id = Column(
        SMALLINT,
        ForeignKey(
            column='shop_category.id',
            ondelete='CASCADE'
        ),
        nullable=False,
        index=True
    )

    category = relationship(argument='ShopCategory', back_populates='products')
    images = relationship(argument='ProductImage')


class ProductImage(Base):
    __tablename__ = 'product_image'

    id = Column(INT, primary_key=True)
    product_id = Column(INT, ForeignKey(column='product.id', ondelete='CASCADE'), nullable=False)
    image = Column(VARCHAR(128), nullable=False)

    def __repr__(self):
        return self.image


class User(Base):
    __tablename__ = 'user'

    id = Column(CHAR(26), primary_key=True, default=lambda: new().str)
    email = Column(VARCHAR(128), nullable=False, unique=True)
    password = Column(VARCHAR(256), nullable=False)

    @property
    def is_authenticated(self):
        return True

    @property
    def identity(self):
        return self.id

    @property
    def display_name(self):
        return self.email
