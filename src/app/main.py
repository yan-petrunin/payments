from fastapi import FastAPI
from src.app.api.v1.payment import payment

app = FastAPI()

app.include_router(payment)