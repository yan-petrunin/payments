from src.app.core.db.models.base import Base
from sqlalchemy.orm import MappedColumn, mapped_column, relationship
from sqlalchemy import Integer, String

class Currency(Base):
    __tablename__ = "currencies"

    id: MappedColumn[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    currency: MappedColumn[str] = mapped_column(String(5), nullable=False, unique=True)

    payments = relationship("Payment", back_populates="currencies")
