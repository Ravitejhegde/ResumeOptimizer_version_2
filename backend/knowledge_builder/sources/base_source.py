from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from knowledge_builder.models.source_package import (
    SourcePackage,
)


class BaseSource(ABC):

    @abstractmethod
    def load(
        self,
    ) -> SourcePackage:
        raise NotImplementedError