import asyncio
from contextlib import asynccontextmanager
from faststream import FastStream
from src.broker.broker import broker, payments_queue
from src.broker.workers.outbox import outbox_worker

from src.broker.consumers.payment import handle_payment # noqa

@asynccontextmanager
async def lifespan():
    task = asyncio.create_task(outbox_worker(broker, payments_queue))
    yield
    task.cancel()

app = FastStream(broker, lifespan=lifespan)

if __name__ == "__main__":
    asyncio.run(app.run())