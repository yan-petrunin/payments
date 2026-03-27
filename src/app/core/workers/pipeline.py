from abc import ABC, abstractmethod

class BasePipeline(ABC):
    @abstractmethod
    async def process():
        pass

    @abstractmethod
    async def insert_payment():
        pass
    
    @abstractmethod
    async def publish_payment():
        pass
    
    @abstractmethod
    async def check_payment():
        pass