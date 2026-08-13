"""
app.optimizer.services.optimizer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Public Optimizer service.
"""

from __future__ import annotations

from app.optimizer.engine.optimizer_engine import (
    OptimizerEngine,
)
from app.optimizer.models.optimization_request import (
    OptimizationRequest,
)
from app.optimizer.models.optimization_result import (
    OptimizationResult,
)


class Optimizer:
    """
    Public API for resume optimization.
    """

    def __init__(
        self,
    ) -> None:

        self._engine = OptimizerEngine()

    def optimize(
        self,
        request: OptimizationRequest,
    ) -> OptimizationResult:
        """
        Optimize a resume using AI.
        """

        return self._engine.optimize(
            request
        )