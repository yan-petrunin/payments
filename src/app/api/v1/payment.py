from typing import Annotated
from src.app.settings.settings import config
from fastapi import APIRouter, Body, Depends, Path, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.core.schema.payment import PaymentBody, PaymentResponse

payment = APIRouter(prefix="/api/v1")

@payment.post("/payments")
async def create_short_link(
    body: Annotated[PaymentBody, Body()],
    db_session: Annotated[AsyncSession, Depends(config.db_helper.session_dependency)],
) -> PaymentResponse:
    ...

@payment.get("/payments/{payment_id}")
async def get_link(
    payment_id: Annotated[str, Path()],
    db_session: Annotated[AsyncSession, Depends(config.db_helper.session_dependency)],
):
    ...