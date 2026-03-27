from sqlalchemy.orm import  relationship
from src.app.core.db.models.base import Base
from src.app.core.db.models.base_status import BaseStatus

class BrokerStatus(Base, BaseStatus):
    __tablename__ = "broker_statuses"

    payments = relationship("Payment", back_populates="broker_statuses")