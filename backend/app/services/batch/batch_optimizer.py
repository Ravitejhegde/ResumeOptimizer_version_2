from app.services.ai.openrouter_provider import (
    OpenRouterProvider,
)

from app.services.batch.batch_prompt_builder import (
    BatchPromptBuilder,
)

from app.services.batch.batch_response_parser import (
    BatchResponseParser,
)

from app.services.docx.document_block import (
    DocumentBlock,
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

from app.services.knowledge.knowledge_builder import (
    KnowledgeBuilder,
)

from app.services.writer.block_merger import (
    BlockMerger,
)


class BatchOptimizer:

    def __init__(self):

        self.ai = OpenRouterProvider()

    def optimize(
    self,
    blocks,
    job_description,
    selected_skills: list[str],
):

        # Build resume knowledge
        resume_knowledge = KnowledgeBuilder.build(
            blocks
        )

        # Parse job description
        jd_knowledge = JDParser.parse(
            job_description
        )

        # Compare resume vs JD
        comparison = SkillComparator.compare(
            resume_knowledge,
            jd_knowledge,
        )

        # Decide what AI should prioritize
        promotion = TechnologyPromoter.build(
    comparison=comparison,
    selected_skills=selected_skills,
)

        # Build AI prompt
        prompt = BatchPromptBuilder.build(
            blocks=blocks,
            knowledge=resume_knowledge,
            promotion=promotion,
            job_description=job_description,
        )

        # Generate AI response
        response = self.ai.generate(
            prompt
        )

        # Parse JSON
        parsed = BatchResponseParser.parse(
            response
        )

        # Merge updated blocks
        return BlockMerger.merge(
            blocks,
            parsed,
        )