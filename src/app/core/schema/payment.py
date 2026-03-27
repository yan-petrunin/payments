from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl

class PaymentBody(BaseModel):
    sum: float = Field(description="Сумма покупки")
    currency: str = Field(description="Валюта")
    desctription: str = Field(description="Описание")
    metadata: dict = Field(description="Метаданные")
    webhook_url: HttpUrl = Field(description="Webhook URL")

class PaymentResponse(BaseModel):
    payment_id: int = Field(description="ID платежа")
    status: str = Field(description="Статус")
    created_at: datetime = Field(description="Дата создания платежа")