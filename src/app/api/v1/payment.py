from typing import Annotated
from src.app.core.db.crud import get_payment_by_id
from src.app.core.auth import verify_api_key
from src.app.workers.payment import PaymentPipeline
from src.app.settings.settings import config
from fastapi import APIRouter, Body, Depends, HTTPException, Header, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.core.schema.payment import PaymentBody, PaymentFullResponse, PaymentResponse

payment = APIRouter(prefix="/api/v1", dependencies=[Depends(verify_api_key)])

@payment.post("/payments")
async def post_payment(
    body: Annotated[PaymentBody, Body()],
    db_session: Annotated[AsyncSession, Depends(config.db_helper.session_dependency)],
    idempotency_key: Annotated[str, Header()]
) -> PaymentResponse:
    worker = PaymentPipeline(db_session=db_session)
    result = await worker.process(payment=body, idempotency_key=idempotency_key)
    return result

@payment.get("/payments/{payment_id}")
async def get_payment(
    payment_id: Annotated[int, Path()],
    db_session: Annotated[AsyncSession, Depends(config.db_helper.session_dependency)],
):
    result = await get_payment_by_id(db_session, payment_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payment not found")
    return PaymentFullResponse(
        payment_id=result.id,
        status=result.status,
        sum=result.sum,
        currency=result.currency,
        description=result.description,
        metadata=result.payment_metadata,
        webhook_url=result.webhook_url,
        created_at=result.created_at,
        modified_at=result.modified_at,
    )