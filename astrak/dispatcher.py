from . import Astrak
from .rules import default_rules, AbstractRule
from .types import Event, Message
from .exceptions import AstrakException
import typing


class Handler:
    def __init__(self, func: typing.Callable, **rules: typing.List[AbstractRule]):
        self.func = func
        self.rules = rules

    async def __call__(self, message: Message):
        await self.func(message)


class Dispatcher:
    def __init__(self, astrak: Astrak):
        self.astrak = astrak
        self.message_handlers = []

    async def _dispatch_new_message(self, event: Event):
        for handler in self.message_handlers:
            for rule in handler.rules:
                if rule in default_rules:
                    executed = await default_rules[rule]().check(
                        message=event.event, text=handler.rules[rule]
                    )
                    if executed:
                        return executed, handler

    def message_handler(self, **rules):
        def decorator(func: typing.Callable) -> typing.Callable:
            handler = Handler(func, **rules)
            self.message_handlers.append(handler)
            return func

        return decorator

    async def _listen(self):
        while True:
            try:
                event_info = await self.astrak.get_events()
            except AstrakException:
                continue
            yield event_info

    async def dispatch_forever(self):
        async for event in self._listen():
            execute, handler = await self._dispatch_new_message(event)
            if execute is not None:
                message = Message(api=self.astrak, **event.event.dict())
                await handler(message)
