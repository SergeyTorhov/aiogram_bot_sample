import asyncio
import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.dispatcher import DEFAULT_RATE_LIMIT


def rate_limit(limit: int, key=None):
    """
    Decorator for configuring rate limit and key in different functions.
    :param limit:
    :param key:
    :return:
    """

    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func

    return decorator


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit: int = DEFAULT_RATE_LIMIT, key_prefix: str = "antiflood_"):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):

        """
        This handler is called when dp receives a message
        :param data:
        :param message:
        """
        # Get current handler
        handler = current_handler.get()
        # Get dp from context
        dp = Dispatcher.get_current()
        # If handler was configured, get rate limit and key from handler
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"
        # print(f"Limit: {limit}, key: {key}")
        # Use Dispatcher.throttle method.
        try:
            await dp.throttle(key, rate=limit)
        except Throttled as t:
            # Execute action
            logging.info(msg="Users message from userid: {} throttled. {}".format(message.from_user.id,
                                                                                  t))
            await self.message_throttled(message, t)
            # Cancel current handler
            raise CancelHandler()

    async def on_process_callback_query(self, cb: types.CallbackQuery, data: dict):
        """
        This handler is called when dp receives a callback query
        :param data:
        :param cb:
        """
        # Get current handler
        handler = current_handler.get()
        # Get dp from context
        dp = Dispatcher.get_current()
        # If handler was configured, get rate limit and key from handler
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"
        print(f"Limit: {limit}, key: {key}")
        # Use Dispatcher.throttle method.
        try:
            await dp.throttle(key, rate=limit)
        except Throttled as t:
            # Execute action
            logging.info(msg="Users callback query from userid: {} throttled. {}".format(cb.from_user.id,
                                                                                         t))
            await self.cb_throttled(cb, throttled=t)
            # Cancel current handler
            raise CancelHandler()

    async def cb_throttled(self, cb: types.CallbackQuery, throttled: Throttled):
        """
        Notify user only on first exceed and notify about unlocking only on last exceed
        :param cb:
        :param throttled:
        """
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            key = f"{self.prefix}_message"
        # Calculate how much time is left until the end of the block
        delta = throttled.rate - throttled.delta
        # Prevent flooding
        if throttled.exceeded_count <= 2:
            await cb.answer('Too many requests! ')
        # Sleep.
        await asyncio.sleep(delta)
        # Check lock status
        thr = await dispatcher.check_key(key)
        # If current message is not last with current key - do not send message
        if thr.exceeded_count == throttled.exceeded_count:
            await cb.answer('Unlocked.')

    async def message_throttled(self, message: types.Message, throttled: Throttled):
        """
        Notify user only on first exceed and notify about unlocking only on last exceed
        :param message:
        :param throttled:
        """
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            key = f"{self.prefix}_message"
        # Calculate how much time is left until the end of the block
        delta = throttled.rate - throttled.delta
        # Prevent flooding
        if throttled.exceeded_count <= 2:
            await message.reply('Too many requests! ')
        # Sleep.
        await asyncio.sleep(delta)
        # Check lock status
        thr = await dispatcher.check_key(key)
        # If current message is not last with current key - do not send message
        if thr.exceeded_count == throttled.exceeded_count:
            await message.reply('Unlocked.')


async def register_middleware(dp: Dispatcher) -> None:
    """
    Registering the middleware in the dispatcher object.
    :param dp:
    :return:
    """
    dp.setup_middleware(middleware=ThrottlingMiddleware())
