from sqlalchemy.orm import MappedColumn, mapped_column
from sqlalchemy import Integer, String

class BaseStatus:
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    status: MappedColumn[str] = mapped_column(String(15), nullable=False, unique=True)
