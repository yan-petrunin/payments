from src.app.core.db.models.base import Base
from sqlalchemy.orm import MappedColumn, mapped_column, relationship
from sqlalchemy import BigInteger, Integer, Text, String, DateTime, func, UUID, Float, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB

class Payment(Base):
    __tablename__ = "payments"

    id: MappedColumn[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    idempotency_key: MappedColumn[UUID] = mapped_column(UUID, nullable=False, unique=True)
    sum: MappedColumn[float] = mapped_column(Float, nullable=False)
    currency_id: MappedColumn[int] = mapped_column(ForeignKey("currencies.id"))
    description: MappedColumn[str] = mapped_column(Text)
    metadata: MappedColumn[JSONB] = mapped_column(JSONB)
    status_id: MappedColumn[int] = mapped_column(ForeignKey("payment_statuses.id"))
    count: MappedColumn[int] = mapped_column(BigInteger, nullable=False, default=0)
    webhook_url: MappedColumn[str] = mapped_column(String(150), nullable=False)
    created_at: MappedColumn[DateTime] = mapped_column(DateTime, nullable=False, default=func.now())
    modified_at: MappedColumn[DateTime] = mapped_column(DateTime, nullable=False, default=func.now())

    currency = relationship("Currency", back_populates="payments")
    status = relationship("PaymentStatus", back_populates="payments")
