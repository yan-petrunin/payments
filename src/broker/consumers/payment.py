import asyncio
import random

from faststream.rabbit import RabbitMessage
from src.app.core.workers.external_api import send_webhook_with_retry
from src.app.core.db.crud import get_payment_by_id, update_payment_status
from src.app.settings.settings import config
from src.app.core.db.models.payment_status import PaymentStatus
from src.broker.broker import broker, payments_queue, payments_dlq_queue

@broker.subscriber(payments_queue)
async def handle_payment(data: dict, msg: RabbitMessage):
    payment_id = data["payment_id"]
    retry_count = msg.headers.get("x-retry-count", 0)

    async with config.db_helper.session_factory() as session:
        payment = await get_payment_by_id(session, payment_id)

        if not payment:
            return
        
        if retry_count == 0:
            if payment.status != PaymentStatus.PENDING:
                return

            await asyncio.sleep(random.uniform(2, 5))
            success = random.random() < 0.9
            new_status = PaymentStatus.SUCCEEDED if success else PaymentStatus.FAILED
            await update_payment_status(session, payment_id, new_status)
        else:
            new_status = payment.status
    try:
        await send_webhook_with_retry(
            url=data["webhook_url"],
            payload={
                "payment_id": payment_id,
                "status": new_status.value,
                "sum": data["sum"],
                "currency": data["currency"],
            }
        )
    except Exception:
        if retry_count >= 2: 
            await msg.reject(requeue=False)
            return

        await broker.publish(
            data,
            queue=payments_queue,
            headers={"x-retry-count": retry_count + 1},
        )

@broker.subscriber(payments_dlq_queue)
async def handle_dlq(data: dict):
    print(f"DLQ получил: {data}")
