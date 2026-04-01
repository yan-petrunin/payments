import aiohttp
from src.app.core.helpers.retry import webhook_retry

class WebhookError(Exception):
    pass


@webhook_retry()
async def send_webhook_with_retry(url: str, payload: dict) -> int:
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            print(response.status)
            if not response.ok:
                raise WebhookError(f"Webhook failed: {response.status}")
            return response.status
