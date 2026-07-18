from app.services.optimizer.optimization_map import (
    OptimizationMap,
)


class ParagraphOptimizer:

    @staticmethod
    def optimize(
        item: OptimizationMap,
    ) -> OptimizationMap:

        if not item.block.can_optimize:

            return item

        item.optimized_text = (
            "[OPTIMIZED] "
            + item.original_text
        )

        item.modified = (
            item.optimized_text
            != item.original_text
        )

        return item