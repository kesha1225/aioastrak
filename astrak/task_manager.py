import asyncio
import typing
import logging


class TaskManager:
    """
    Task manager represent to user high-level API of asyncio interface
    """

    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.tasks: typing.List[typing.Coroutine] = []
        self.loop: asyncio.AbstractEventLoop = loop

    def run(
        self,
        *,
        on_shutdown: typing.Callable = None,
        on_startup: typing.Callable = None,
        asyncio_debug_mode: bool = False,
    ):
        """
        Method which run event loop

        :param on_shutdown: coroutine which runned after complete tasks
        :param on_startup: coroutine which runned before start main tasks
        :param asyncio_debug_mode: asyncio debug mode state
        :return:
        """
        if len(self.tasks) < 1:
            raise RuntimeError("Count of tasks - 0. Add tasks.")
        try:
            if on_startup is not None:
                self.loop.run_until_complete(on_startup())

            if asyncio_debug_mode:
                self.loop.set_debug(True)

            [self.loop.create_task(task) for task in self.tasks]

            logging.info("Loop started!")
            self.loop.run_forever()

        finally:
            if on_shutdown is not None:
                self.loop.run_until_complete(on_shutdown())

    def add_task(self, task: typing.Coroutine) -> None:
        """

        Add task to loop when loop don`t started.

        :param task: coroutine for run in loop
        :return:
        """
        self.tasks.append(task)
        return None
