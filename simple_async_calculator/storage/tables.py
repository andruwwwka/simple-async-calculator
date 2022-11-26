import sqlalchemy as sa

from simple_async_calculator.storage import Base


class Task(Base):  # pylint: disable=too-few-public-methods
    """Представление модели хранения данных о задачах"""

    __tablename__ = "tasks"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    created = sa.Column(sa.DateTime(timezone=True), nullable=False)
    updated = sa.Column(sa.DateTime(timezone=True), nullable=False)
    x = sa.Column(sa.Integer, nullable=False)
    y = sa.Column(sa.Integer, nullable=False)
    operator = sa.Column(sa.String(1), nullable=False)
    status = sa.Column(sa.String(10), nullable=False)
    result = sa.Column(sa.Numeric, nullable=True)
