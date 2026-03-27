from src.app.core.db.models.base import Base
from sqlalchemy.orm import MappedColumn, mapped_column
from sqlalchemy import Integer, String

class BaseStatus(Base):
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    status: MappedColumn[str] = mapped_column(String(15), nullable=False, unique=True)

