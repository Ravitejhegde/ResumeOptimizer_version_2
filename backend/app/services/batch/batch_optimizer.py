from app.core.logger import logger

from app.services.ai.ai_factory import AIFactory

from app.services.batch.batch_response_parser import (
    BatchResponseParser,
)

from app.services.docx.document_block import (
    DocumentBlock,
)

from app.services.intelligence.engine import (
    IntelligenceEngine,
)

from app.services.intelligence.prompt.prompt_builder import (
    PromptBuilder,
)

from app.services.intelligence.prompt.prompt_context import (
    PromptContext,
)

from app.services.writer.block_merger import (
    BlockMerger,
)


class BatchOptimizer:
    """
    Coordinates the AI optimization workflow.

    Blocks
        ↓
    Intelligence
        ↓
    Prompt
        ↓
    AI
        ↓
    JSON Validation
        ↓
    Block Merge
    """

    def __init__(self):

        self.ai = AIFactory.create()

    def optimize(
        self,
        blocks: list[DocumentBlock],
        job_description: str,
    ) -> list[DocumentBlock]:

        # -----------------------------------------
        # Intelligence
        # -----------------------------------------

        plan = IntelligenceEngine.analyze(
            blocks=blocks,
            job_description=job_description,
        )

        # -----------------------------------------
        # Editable Blocks
        # -----------------------------------------

        editable_blocks = [
            {
                "id": block.id,
                "type": block.block_type,
                "text": block.text,
            }
            for block in blocks
            if block.can_optimize
        ]

        # -----------------------------------------
        # Prompt Context
        # -----------------------------------------

        context = PromptContext(
            plan=plan,
            blocks=editable_blocks,
            keep=[
                item.skill.name
                for item in plan.keep
            ],
            remove=[
                item.skill.name
                for item in plan.remove
            ],
            add=[
                item.skill.name
                for item in plan.add
            ],
            warnings=plan.warnings,
            formatting_rules="""
Keep paragraph length similar.
Do not add new paragraphs.
Do not remove paragraphs.
Preserve formatting.
""",
            job_description=job_description,
            system_rules="",
        )

        # -----------------------------------------
        # Build Prompt
        # -----------------------------------------

        prompt = PromptBuilder.build(
            context
        )

        # -----------------------------------------
        # AI
        # -----------------------------------------

        logger.info(
            "Sending optimization request to AI..."
        )

        logger.info(f"Prompt length: {len(prompt)} characters")
        logger.info(f"Editable blocks: {len(context.blocks)}")
        response = self.ai.generate(
            prompt
        )
        logger.info(prompt[:2000])
        logger.info("===== RAW AI RESPONSE =====")
        logger.info(response)
        logger.info("===========================")

        logger.info(
            "AI response received."
        )

        # -----------------------------------------
        # Validate Response
        # -----------------------------------------

        if response is None:
            raise ValueError(
                "AI returned None."
            )

        if not isinstance(response, str):
            response = str(response)

        response = response.strip()

        if not response:
            raise ValueError(
                "AI returned an empty response."
            )

        # -----------------------------------------
        # Parse AI Response
        # -----------------------------------------

        parsed = BatchResponseParser.parse(
            response
        )
        

        logger.info(f"Parsed result: {parsed}")
        # -----------------------------------------
        # Merge Updated Blocks
        # -----------------------------------------

        optimized_blocks = BlockMerger.merge(
            original_blocks=blocks,
            updated_blocks=parsed,
        )

        return optimized_blocks