from datetime import datetime

from src.app.core.db.models.currency import Currency
from src.app.core.db.models.payment_status import PaymentStatus
from src.app.core.db.models.base import Base
from sqlalchemy.orm import MappedColumn, mapped_column
from sqlalchemy import BigInteger, Text, String, DateTime, func, Float, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import JSONB

class Payment(Base):
    __tablename__ = "payments"

    id: MappedColumn[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    idempotency_key: MappedColumn[str] = mapped_column(String(255), nullable=False, unique=True)
    sum: MappedColumn[float] = mapped_column(Float, nullable=False)
    currency: MappedColumn[Currency] = mapped_column(
        SQLAlchemyEnum(Currency), nullable=False, default=Currency.RUB
    )
    description: MappedColumn[str] = mapped_column(Text)
    payment_metadata: MappedColumn[dict] = mapped_column(JSONB)
    status: MappedColumn[PaymentStatus] = mapped_column(
        SQLAlchemyEnum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING
    )
    webhook_url: MappedColumn[str] = mapped_column(String(150), nullable=False)
    created_at: MappedColumn[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    modified_at: MappedColumn[datetime] = mapped_column(DateTime, nullable=False, onupdate=func.now(), default=func.now())