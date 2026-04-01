import asyncio
from datetime import datetime

from faststream.rabbit import RabbitBroker, RabbitQueue
from src.app.core.db.crud import get_unpublished_payments
from src.app.core.db.models.outbox import BrokerStatus
from src.app.settings.settings import config

async def outbox_worker(broker: RabbitBroker, queue: RabbitQueue):
    while True:
        async with config.db_helper.session_factory() as session:
            try:
                result = await get_unpublished_payments(session)
            except Exception:
                pass

            for record in result:
                await broker.publish(record.payload, queue=queue)
                record.status = BrokerStatus.PUBLISHED
                record.published_at = datetime.now()

            await session.commit()
        
        await asyncio.sleep(2)
