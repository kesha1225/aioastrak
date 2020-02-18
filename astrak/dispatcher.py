from . import Astrak
from .rules import default_rules, AbstractRule
from .types import Event, Message
from .exceptions import AstrakServerException
import typing
import logging


class Handler:
    def __init__(self, func: typing.Callable, **rules):
        self.func = func
        self.rules: typing.Dict[str, str] = rules

    async def __call__(self, message: Message) -> None:
        await self.func(message)
        return None


class Dispatcher:
    def __init__(self, astrak: Astrak):
        self.astrak = astrak
        self.loop = astrak.loop
        self.message_handlers: typing.List[Handler] = []

    async def _dispatch_new_message(
        self, event: Event
    ) -> typing.Tuple[bool, typing.Optional[Handler]]:
        for handler in self.message_handlers:
            for rule in handler.rules:
                if rule in default_rules:
                    executed = await default_rules[rule]().check(
                        message=event.event, text=handler.rules[rule]
                    )
                    if executed:
                        return executed, handler
        else:
            return False, None

    async def _dispatch_event(self, event: Event) -> None:
        execute, handler = await self._dispatch_new_message(event)
        if execute and handler is not None:
            message = Message(api=self.astrak, **event.event.dict())
            return await handler(message)

    def message_handler(self, **rules):
        def decorator(func: typing.Callable) -> typing.Callable:
            handler = Handler(func, **rules)
            self.message_handlers.append(handler)
            return func

        return decorator

    async def _listen(self) -> typing.AsyncIterable:
        while True:
            try:
                event_info = await self.astrak.get_events()
            except AstrakServerException as e:
                logging.debug(
                    f"Smth went wrong on server while listening - {e}, skipping."
                )
                continue
            logging.debug(f"got events - {event_info}")
            yield event_info

    async def dispatch_forever(self):
        logging.debug("Starting listening lp...")
        async for event in self._listen():
            self.loop.create_task(self._dispatch_event(event))
