from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.core.db.models.payment import Payment
from src.app.core.db.crud import  check_payment_exist, create_payment_with_outbox
from src.app.core.schema.payment import PaymentBody, PaymentResponse
from src.app.core.workers.pipeline import BasePipeline


class PaymentPipeline(BasePipeline):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def check_payment(self, key: str) -> Payment | None:
        return await check_payment_exist(session=self.db_session, idempotency_key=key)

    async def insert_payment(self, payment: PaymentBody, key: str) -> Payment | None:
        try:
            return await create_payment_with_outbox(session=self.db_session, payload=payment, idempotency_key=key)
        except Exception:
            await self.db_session.rollback()
            raise
    async def process(self, payment: PaymentBody, idempotency_key: str) -> PaymentResponse:
        existing = await self.check_payment(idempotency_key)
        if existing:
            return PaymentResponse(
                payment_id=existing.id,
                status=existing.status,
                created_at=existing.created_at
            )
        
        try:
            payment = await self.insert_payment(payment, idempotency_key)
        except IntegrityError:
            payment = await self.check_payment(idempotency_key)
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error"
            ) from e

        if not payment:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Payment insert failed and could not be recovered"
            )

        return PaymentResponse(
            payment_id=payment.id,
            status=payment.status,
            created_at=payment.created_at
        )