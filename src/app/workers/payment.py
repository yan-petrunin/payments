from sqlalchemy.ext.asyncio import AsyncSession
from src.app.core.workers.pipeline import BasePipeline

class PaymentPipeline(BasePipeline):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
    
    async def insert_payment(self):
        ...

    async def process(self):
        ...