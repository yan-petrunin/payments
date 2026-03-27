from sqlalchemy.orm import  relationship
from src.app.core.db.models.base import Base
from src.app.core.db.models.base_status import BaseStatus

class PaymentStatus(Base, BaseStatus):
    __tablename__ = "payment_statuses"

    payments = relationship("Payment", back_populates="payment_statuses")