from abc import ABC, abstractmethod

import typing

from astrak.types import MessageEvent


class AbstractRule(ABC):
    title: typing.Optional[str] = None

    @abstractmethod
    async def check(self, message: MessageEvent, text: str) -> bool:
        """
        check rule data
        :return:
        """


class TextRule(AbstractRule):
    title = "text"

    async def check(self, message: MessageEvent, text: str) -> bool:
        return message.text.lower() == text


class TextContainsRule(AbstractRule):
    title = "text_contains"

    async def check(self, message: MessageEvent, text: typing.Any) -> bool:
        return text in [word.lower() for word in message.text.split()]


default_rules: typing.Dict[str, typing.Type[AbstractRule]] = {
    TextRule.title: TextRule,
    TextContainsRule.title: TextContainsRule,
}
