from pydantic import BaseModel

class OutboxPayload(BaseModel):
    payment_id: int
    sum: float
    currency_id: int
    webhook_url: str