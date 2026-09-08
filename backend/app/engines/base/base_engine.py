from abc import ABC


class BaseEngine(ABC):
    """
    Base class for all processing engines.

    Engines encapsulate reusable business processing logic
    and remain independent of API, Repository, and Database layers.
    """

    @property
    def engine_name(self) -> str:
        return self.__class__.__name__