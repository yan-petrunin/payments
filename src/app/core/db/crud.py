from typing import Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.core.schema.payment import PaymentBody
from src.app.core.db.models.payment import Payment
from src.app.core.db.models.outbox import OutboxRecord
from src.app.core.db.models.payment_status import PaymentStatus
from src.app.core.db.models.broker_status import BrokerStatus

async def check_payment_exist(session: AsyncSession, idempotency_key: str) -> Payment | None:
    stmt = select(Payment).where(Payment.idempotency_key == idempotency_key)
    result = await session.execute(stmt)
    return result.scalars().one_or_none()

async def get_payment_by_id(session: AsyncSession, id: int) -> Payment | None:
    stmt = select(Payment).where(Payment.id == id)
    result = await session.execute(stmt)
    return result.scalars().one_or_none()

async def get_unpublished_payments(session: AsyncSession) -> Sequence[OutboxRecord]:
    stmt =  select(OutboxRecord).where(OutboxRecord.status == BrokerStatus.PENDING)
    result = await session.execute(stmt)
    return result.scalars().all()

async def update_payment_status(session, payment_id: int, new_status: PaymentStatus) -> None:
    stmt =  update(Payment).values(status=new_status).where(Payment.id == payment_id)
    await session.execute(stmt)
    await session.commit()

async def create_payment_with_outbox(session: AsyncSession, payload: PaymentBody, idempotency_key: str) -> Payment | None:
    new_payment = Payment(
                    idempotency_key=idempotency_key,
                    sum=payload.sum,
                    currency=payload.currency,
                    description=payload.description,
                    payment_metadata=payload.metadata,
                    status=PaymentStatus.PENDING,
                    webhook_url=payload.webhook_url
                )
    session.add(new_payment)
    await session.flush() 
    new_outbox = OutboxRecord(
        status=BrokerStatus.PENDING,
        payload={
            "payment_id": new_payment.id,
            "sum": new_payment.sum,
            "currency": new_payment.currency,
            "webhook_url": new_payment.webhook_url,
        }
    )
    session.add(new_outbox)
    await session.commit()
    return new_payment