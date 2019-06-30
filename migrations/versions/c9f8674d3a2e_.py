"""empty message

Revision ID: c9f8674d3a2e
Revises: 412199dfec5b
Create Date: 2019-06-29 23:53:51.111446

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c9f8674d3a2e"
down_revision = "412199dfec5b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "plan",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("key", sa.String(length=32), nullable=True),
        sa.Column("name", sa.String(length=32), nullable=True),
        sa.Column("type", sa.String(length=32), nullable=True),
        sa.Column("stripe_id", sa.String(length=20), nullable=True),
        sa.Column("description", sa.String(length=64), nullable=True),
        sa.Column("price", sa.SmallInteger(), nullable=True),
        sa.Column("level", sa.SmallInteger(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column("user", sa.Column("plan_id", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "user", "plan", ["plan_id"], ["id"])
    op.drop_column("user", "plan")
    op.create_unique_constraint(None, "plan", ["key"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user",
        sa.Column("plan", sa.VARCHAR(length=16), autoincrement=False, nullable=True),
    )
    op.drop_constraint(None, "user", type_="foreignkey")
    op.drop_constraint(None, "plan", type_="unique")
    op.drop_column("user", "plan_id")
    op.drop_table("plan")
    # ### end Alembic commands ###