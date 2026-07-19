from pathlib import Path

from docx import Document

from app.document.parser.snapshot_builder import SnapshotBuilder
from app.document.parser.block_builder import BlockBuilder

from app.services.batch.batch_optimizer import BatchOptimizer

from app.services.docx.writer import DocxWriter

from app.services.layout_validation.layout_validator import (
    LayoutValidator,
)


class OptimizationPipeline:

    def optimize(
        self,
        resume_path: str,
        job_description: str,
        selected_skills: list[str],
    ):

        # -----------------------------------------
        # Build Snapshot
        # -----------------------------------------

        snapshot = SnapshotBuilder.build(
            resume_path
        )

        # -----------------------------------------
        # Snapshot -> Blocks
        # -----------------------------------------

        blocks = BlockBuilder.build(
            snapshot
        )

        # -----------------------------------------
        # AI Optimization
        # -----------------------------------------

        optimizer = BatchOptimizer()

        optimized_blocks = optimizer.optimize(
            blocks=blocks,
            job_description=job_description,
        )

        # -----------------------------------------
        # Validate Layout
        # -----------------------------------------

        validation = LayoutValidator.validate(
            original_blocks=blocks,
            optimized_blocks=optimized_blocks,
        )

        print(validation)

        # -----------------------------------------
        # Load Original DOCX
        # -----------------------------------------

        document = Document(
            resume_path
        )

        # -----------------------------------------
        # Replace Optimized Paragraphs
        # -----------------------------------------

        DocxWriter.replace_blocks(
            document=document,
            blocks=optimized_blocks,
        )

        # -----------------------------------------
        # Save Optimized DOCX
        # -----------------------------------------

        output_path = (
            Path("storage/exports")
            / (
                Path(resume_path).stem
                + "_Optimized.docx"
            )
        )

        DocxWriter.save(
            document=document,
            output_path=output_path,
        )

        # -----------------------------------------
        # Build Preview Model
        # -----------------------------------------

        preview_blocks = []

        for block in optimized_blocks:

            preview_blocks.append(
                {
                    "id": block.id,
                    "paragraphIndex": block.paragraph_index,
                    "text": block.text,
                    "style": block.style,
                    "block_type": block.block_type,
                    "blockType": block.block_type,
                    "can_optimize": block.can_optimize,
                    "editable": block.can_optimize,
                    "section": "",
                    "modified": False,
                    "runs": [
                        {
                            "text": run.text,
                            "bold": run.bold,
                            "italic": run.italic,
                            "underline": run.underline,
                            "fontName": run.font_name,
                            "fontSize": run.font_size,
                            "color": run.color,
                        }
                        for run in block.runs
                    ],
                }
            )

        # -----------------------------------------
        # Response
        # -----------------------------------------

        return {
            "optimized_filename": output_path.name,
            "blocks": preview_blocks,
        }