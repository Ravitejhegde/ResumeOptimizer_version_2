from pathlib import Path

from docx import Document

from app.core.config import settings
from app.services.batch.batch_optimizer import (
    BatchOptimizer,
)
from app.services.docx.parser import (
    DocxParser,
)
from app.services.docx.writer import (
    DocxWriter,
)


class OptimizationService:

    def optimize(
        self,
        stored_filename: str,
        job_description: str,
    ) -> dict:

        input_path = (
            settings.TEMP_DIR
            / stored_filename
        )

        if not input_path.exists():

            raise FileNotFoundError(
                f"{stored_filename} not found."
            )

        document = Document(input_path)

        blocks = DocxParser.parse(
            document
        )

        optimizer = BatchOptimizer()

        updated_blocks = optimizer.optimize(
            blocks,
            job_description,
        )

        DocxWriter.replace_blocks(
            document,
            updated_blocks,
        )

        output_filename = (
            Path(stored_filename).stem
            + "_Optimized.docx"
        )

        output_path = (
            settings.TEMP_DIR
            / output_filename
        )

        DocxWriter.save(
            document,
            output_path,
        )

        return {

            "original_file": stored_filename,

            "optimized_file": output_filename,

        }