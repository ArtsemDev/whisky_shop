"""empty message

Revision ID: 1807fded6239
Revises: f6eb6e60bbec
Create Date: 2023-08-11 13:40:01.965607

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1807fded6239'
down_revision = 'f6eb6e60bbec'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('category_id', sa.SMALLINT(), nullable=False))
    op.create_index(op.f('ix_product_category_id'), 'product', ['category_id'], unique=False)
    op.create_foreign_key(None, 'product', 'shop_category', ['category_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'product', type_='foreignkey')
    op.drop_index(op.f('ix_product_category_id'), table_name='product')
    op.drop_column('product', 'category_id')
    # ### end Alembic commands ###