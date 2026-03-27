from src.app.core.db.models.base import Base
from sqlalchemy.orm import MappedColumn, mapped_column, relationship
from sqlalchemy import BigInteger, DateTime, func, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB


class OutboxRecord(Base):
    __tablename__ = "outbox_records"

    id: MappedColumn[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)        
    payload: MappedColumn[JSONB] = mapped_column(JSONB, nullable=False)  
    status_id: MappedColumn[int] = mapped_column(ForeignKey("broker_statuses.id"))
    created_at: MappedColumn[DateTime] = mapped_column(DateTime, nullable=False, default=func.now())
    published_at: MappedColumn[DateTime] = mapped_column(DateTime, nullable=True, default=None)

    status = relationship("BrokerStatus", back_populates="outbox_records")