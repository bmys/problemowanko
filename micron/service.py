from abc import ABC


class Service(ABC):
    tasks: list

    @property
    def channel_pool(self):
        raise NotImplementedError

    @property
    def connection_pool(self):
        raise NotImplementedError
