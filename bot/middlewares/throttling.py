from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
import time

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 0.7):
        self.rate_limit = rate_limit
        self.last_call: Dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id if event.from_user else 0
        now = time.time()
        last = self.last_call.get(user_id, 0)
        if now - last < self.rate_limit:
            return  # silently drop
        self.last_call[user_id] = now
        return await handler(event, data)
