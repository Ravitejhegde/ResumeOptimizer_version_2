from pathlib import Path

from docx import Document

from app.core.config import settings
from app.core.logger import logger

from app.services.document.parser.document_parser import (
    DocumentParser,
)

from app.services.document.snapshot.snapshot_builder import (
    SnapshotBuilder,
)
from app.document.parser.block_builder import (
    BlockBuilder,
)

from app.services.batch.batch_optimizer import (
    BatchOptimizer,
)

from app.services.docx.writer import (
    DocxWriter,
)

from app.services.layout_validation.layout_validator import (
    LayoutValidator,
)


class OptimizationPipeline:
    """
    Resume Optimization Pipeline

    Resume
        ↓
    Snapshot Builder
        ↓
    Block Builder
        ↓
    AI Optimization
        ↓
    Layout Validation
        ↓
    DOCX Writer
        ↓
    Preview Model
    """

    def optimize(
        self,
        resume_path: str,
        job_description: str,
        selected_skills: list[str],
    ):

        # -----------------------------------------
        # Build Snapshot
        # -----------------------------------------

        # -----------------------------------------
# Parse Document
# -----------------------------------------

        document_model = DocumentParser.parse(
    resume_path
)

# -----------------------------------------
# Build Snapshot
# -----------------------------------------

        snapshot = SnapshotBuilder.build(
    document_model
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
    selected_skills=selected_skills,
)
        # -----------------------------------------
# Preserve hyperlinks
# -----------------------------------------

        for original, optimized in zip(
        blocks,
        optimized_blocks,
        ):

            optimized.hyperlinks = original.hyperlinks

        # -----------------------------------------
        # Validate Layout
        # -----------------------------------------

        validation = LayoutValidator.validate(
            original_blocks=blocks,
            optimized_blocks=optimized_blocks,
        )

        logger.info(
            "Layout validation completed."
        )

        logger.info(
            f"Layout Score : {validation.overall_similarity}%"
        )

        # -----------------------------------------
        # Load Original DOCX
        # -----------------------------------------

        document = Document(
            resume_path
        )

        # -----------------------------------------
        # Replace Optimized Blocks
        # -----------------------------------------

        DocxWriter.replace_blocks(
            document=document,
            blocks=optimized_blocks,
        )

        # -----------------------------------------
        # Save DOCX
        # -----------------------------------------

        output_path = (
            settings.EXPORT_PATH
            / f"{Path(resume_path).stem}_Optimized.docx"
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

            "layout": {

                "overall_similarity": (
                    validation.overall_similarity
                ),

                "passed": (
                    validation.passed
                ),

                "original_paragraphs": (
                    validation.original_paragraphs
                ),

                "optimized_paragraphs": (
                    validation.optimized_paragraphs
                ),

                "paragraph_count_match": (
                    validation.paragraph_count_match
                ),

                "structure_match": (
                    validation.structure_match
                ),

            },

        }