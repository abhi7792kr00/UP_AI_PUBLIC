from abc import ABC, abstractmethod
from typing import Generic, TypeVar


TInput = TypeVar("TInput")
TOutput = TypeVar("TOutput")


class BaseWorkflow(
    ABC,
    Generic[TInput, TOutput],
):
    """
    Base class for all workflows.

    A workflow orchestrates multiple engines,
    services, and repositories to execute
    a complete business process.
    """

    @property
    def workflow_name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def execute(
        self,
        request: TInput,
    ) -> TOutput:
        """
        Execute the workflow.
        """
        raise NotImplementedError