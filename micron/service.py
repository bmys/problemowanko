from abc import ABC


class Service(ABC):
    tasks: list

    @property
    def running(self):
        raise NotImplementedError

    @property
    def channel_pool(self):
        raise NotImplementedError

    @property
    def connection_pool(self):
        raise NotImplementedError
