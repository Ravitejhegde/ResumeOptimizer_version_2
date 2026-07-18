from app.services.ai.openrouter_provider import OpenRouterProvider

from app.services.docx.document_block import DocumentBlock


class OptimizerService:

    def __init__(self):

        self.ai = OpenRouterProvider()

    def optimize(

        self,

        blocks: list[DocumentBlock],

        job_description: str,

    ) -> list[DocumentBlock]:

        for block in blocks:

            if not block.can_optimize:

                continue

            optimized = self.ai.optimize_paragraph(

                paragraph=block.text,

                job_description=job_description,

            )

            block.text = optimized

        return blocks