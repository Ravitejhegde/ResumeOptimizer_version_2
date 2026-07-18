from pathlib import Path

from docx import Document
from app.services.layout_validation.layout_validator import LayoutValidator

from app.document.parser.snapshot_builder import SnapshotBuilder
from app.document.parser.block_builder import BlockBuilder

from app.services.knowledge.knowledge_builder import (
    KnowledgeBuilder,
)

from app.services.jd.jd_parser import (
    JDParser,
)

from app.services.jd.skill_comparator import (
    SkillComparator,
)

from app.services.jd.technology_promoter import (
    TechnologyPromoter,
)

from app.services.batch.batch_optimizer import (
    BatchOptimizer,
)

from app.services.docx.writer import (
    DocxWriter,
)


class OptimizationPipeline:

    def optimize(
        self,
        resume_path,
        job_description,
        selected_skills,
    ): 

        # -----------------------------------------
        # Build snapshot
        # -----------------------------------------

        snapshot = SnapshotBuilder.build(
            resume_path
        )

        # -----------------------------------------
        # Convert snapshot -> DocumentBlock
        # -----------------------------------------

        blocks = BlockBuilder.build(
            snapshot
        )

        # -----------------------------------------
        # Extract resume knowledge
        # -----------------------------------------

        resume_knowledge = KnowledgeBuilder.build(
            blocks
        )

        # -----------------------------------------
        # Parse Job Description
        # -----------------------------------------

        jd_knowledge = JDParser.parse(
            job_description
        )

        # -----------------------------------------
        # Compare Skills
        # -----------------------------------------

        comparison = SkillComparator.compare(
            resume_knowledge,
            jd_knowledge,
        )

        TechnologyPromoter.build(
            comparison
        )

        print("Matched :", comparison.matched)
        print("Missing :", comparison.missing)
        print("Extra   :", comparison.extra)

        # -----------------------------------------
        # AI Optimization
        # -----------------------------------------

        optimizer = BatchOptimizer()

        optimized_blocks = optimizer.optimize(
    blocks=blocks,
    job_description=job_description,
    selected_skills=selected_skills,
)
        validation = LayoutValidator.validate(
    original_blocks=blocks,
    optimized_blocks=optimized_blocks,
)

        # -----------------------------------------
        # Load original document
        # -----------------------------------------

        document = Document(
            resume_path
        )

        # -----------------------------------------
        # Replace paragraphs
        # -----------------------------------------

        DocxWriter.replace_blocks(
            document=document,
            blocks=optimized_blocks,
        )

        # -----------------------------------------
        # Save optimized document
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
        # Build Preview Blocks
        # -----------------------------------------

        preview_blocks = []

        for block in optimized_blocks:

            preview_blocks.append({

                "id": block.id,

                "block_type": block.block_type,

                "text": block.text,

                "style": block.style,

                "can_optimize": block.can_optimize,

        })

        # -----------------------------------------
        # Response
        # -----------------------------------------

        return {

            "optimized_filename": output_path.name,

            "matched": sorted(
                comparison.matched
            ),

            "missing": sorted(
                comparison.missing
            ),

            "extra": sorted(
                comparison.extra
            ),

            "blocks": preview_blocks,

        }