from datetime import datetime
from src.app.core.db.models.currency import Currency
from src.app.core.db.models.payment_status import PaymentStatus
from pydantic import  BaseModel, Field

class PaymentBody(BaseModel):
    sum: float = Field(description="Сумма покупки")
    currency: Currency = Field(description="Валюта")
    description: str = Field(description="Описание")
    metadata: dict = Field(description="Метаданные")
    webhook_url: str = Field(description="Webhook URL")

class PaymentResponse(BaseModel):
    payment_id: int = Field(description="ID платежа")
    status: PaymentStatus = Field(description="Статус")
    created_at: datetime = Field(description="Дата создания платежа")

class PaymentFullResponse(PaymentResponse):
    sum: float = Field(description="Сумма покупки")
    currency: Currency = Field(description="Валюта")
    description: str | None = Field(description="Описание", default=None)
    metadata: dict | None = Field(description="Метаданные", default=None)
    webhook_url: str = Field(description="Webhook URL")
    modified_at: datetime = Field(description="Дата изменения платежа")