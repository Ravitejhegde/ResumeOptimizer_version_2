from app.services.ai.batch.batch_rewrite_engine import (
    BatchRewriteEngine,
)

from app.services.intelligence.translator.paragraph_classifier import (
    ParagraphClassifier,
)

from app.services.intelligence.skills.skills_section_locator import (
    SkillsSectionLocator,
)

from app.services.intelligence.skills.skills_section_parser import (
    SkillsSectionParser,
)

from app.services.intelligence.skills.skills_optimizer import (
    SkillsOptimizer,
)

from app.services.intelligence.skills.skills_update_builder import (
    SkillsUpdateBuilder,
)


class ParagraphOptimizer:
    """
    Main optimization orchestrator.

    Responsibilities

    1. Optimize Skills section
    2. Rewrite editable paragraphs
    3. Preserve protected paragraphs
    """

    @classmethod
    def optimize(
        cls,
        snapshot,
        optimization_plan,
        job_description,
    ):

        editable = []

        updates = {}

        # =========================================
        # Skills Optimization
        # =========================================

        skills_paragraphs = SkillsSectionLocator.locate(
            snapshot
        )

        skills_ids = [
            paragraph.id
            for paragraph in skills_paragraphs
        ]

        if skills_paragraphs:

            print()
            print("=" * 60)
            print("SKILLS OPTIMIZATION")
            print("=" * 60)

            resume_categories = (
                SkillsSectionParser.parse(
                    skills_paragraphs
                )
            )

            optimized_categories = (
                SkillsOptimizer.optimize(

                    resume_categories=resume_categories,

                    jd_skills=optimization_plan.jd_skills,

                    selected_skills=optimization_plan.selected_skills,

                    target_role=optimization_plan.target_role,

                    max_lines=optimization_plan.max_skill_lines,

                )
            )

            updates.update(

                SkillsUpdateBuilder.build(

                    paragraph_ids=skills_ids,

                    categories=optimized_categories,

                )

            )

        # =========================================
        # Paragraph Classification
        # =========================================

        for paragraph in snapshot.paragraphs:

            # Skills handled already
            if paragraph.id in skills_ids:

                continue

            print()

            print(
                paragraph.id,
                "|",
                repr(paragraph.text),
            )

            if ParagraphClassifier.should_rewrite(
                paragraph
            ):

                print(" -> Rewrite")

                editable.append(
                    paragraph
                )

            else:

                print(" -> Skip")

                updates[
                    paragraph.id
                ] = paragraph.text

        # =========================================
        # AI Rewrite
        # =========================================

        if editable:

            ai_updates = BatchRewriteEngine.rewrite(

                editable,

                optimization_plan,

                job_description,

            )

            updates.update(
                ai_updates
            )

        return updates