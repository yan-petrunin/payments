from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from src.app.settings.settings import config
from typing import Annotated
API_KEY = config.api_key

api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: Annotated[str, Security(api_key_header)]):
    if api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
