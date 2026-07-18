from pathlib import Path

from docx import Document

from app.services.docx.parser import DocxParser
from app.services.knowledge.knowledge_builder import KnowledgeBuilder
from app.services.planner.optimization_planner import OptimizationPlanner
from app.services.ai.batch_ai_service import BatchAIService
from app.services.writer.block_merger import BlockMerger
from app.services.writer.docx_writer import DocxWriter


class ResumeOptimizerService:

    def optimize(
        self,
        input_path: str | Path,
        job_description: str,
    ) -> Path:

        input_path = Path(input_path)

        document = Document(input_path)

        blocks = DocxParser.parse(document)

        knowledge = KnowledgeBuilder.build(blocks)

        selected_blocks = OptimizationPlanner.plan(blocks)

        ai = BatchAIService()

        response = ai.optimize_resume(
            selected_blocks,
            knowledge,
            job_description,
        )

        updated_blocks = BlockMerger.merge(
            blocks,
            response,
        )

        output_path = (
            input_path.parent
            / f"{input_path.stem}_Optimized.docx"
        )

        DocxWriter.write(
            input_path=input_path,
            blocks=updated_blocks,
            output_path=output_path,
        )

        return output_path