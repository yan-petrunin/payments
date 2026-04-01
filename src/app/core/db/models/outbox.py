from src.app.core.db.models.broker_status import BrokerStatus
from src.app.core.db.models.base import Base
from sqlalchemy.orm import MappedColumn, mapped_column
from sqlalchemy import BigInteger, DateTime, func, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

class OutboxRecord(Base):
    __tablename__ = "outbox_records"

    id: MappedColumn[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)        
    payload: MappedColumn[dict] = mapped_column(JSONB, nullable=False)  
    created_at: MappedColumn[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    published_at: MappedColumn[datetime] = mapped_column(DateTime, nullable=True, default=None)

    status: MappedColumn[BrokerStatus] = mapped_column(
        SQLAlchemyEnum(BrokerStatus), nullable=False, default=BrokerStatus.PENDING
    )