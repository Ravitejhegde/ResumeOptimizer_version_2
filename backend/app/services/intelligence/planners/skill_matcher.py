from app.services.intelligence.constants import (
    CATEGORY_PRIORITY,
)

from app.services.intelligence.models import (
    JDAnalysis,
    ResumeAnalysis,
    SkillDecision,
    SkillAction,
)

from app.services.intelligence.technology.matcher import (
    TechnologyMatcher,
)

from app.services.intelligence.technology.canonicalizer import (
    TechnologyCanonicalizer,
)

class SkillMatcher:

    @staticmethod
    def match(
        resume: ResumeAnalysis,
        jd: JDAnalysis,
    ) -> tuple[
        list[SkillDecision],
        list[SkillDecision],
        list[SkillDecision],
    ]:

        keep: list[SkillDecision] = []
        remove: list[SkillDecision] = []
        add: list[SkillDecision] = []

        # ---------------------------------------
        # Resume Skills
        # ---------------------------------------

        resume_map = {
            TechnologyCanonicalizer.normalize(skill.name).lower(): skill
            for skill in resume.skills
        }

        jd_map = {
            TechnologyCanonicalizer.normalize(skill.name).lower(): skill
            for skill in jd.skills
        }

        # ---------------------------------------
        # KEEP & REMOVE
        # ---------------------------------------

        for name, skill in resume_map.items():

            if name in jd_map:

                keep.append(

                    SkillDecision(

                        skill=skill,

                        action=SkillAction.KEEP,

                        priority=CATEGORY_PRIORITY[
                            skill.category
                        ],

                        reason="Required by Job Description",

                    )

                )

            else:

                remove.append(

                    SkillDecision(

                        skill=skill,

                        action=SkillAction.REMOVE,

                        priority=CATEGORY_PRIORITY[
                            skill.category
                        ],

                        reason="Not required for target role",

                    )

                )

        # ---------------------------------------
        # ADD
        # ---------------------------------------

        for name, skill in jd_map.items():

            if name not in resume_map:

                add.append(

                    SkillDecision(

                        skill=skill,

                        action=SkillAction.ADD,

                        priority=CATEGORY_PRIORITY[
                            skill.category
                        ],

                        reason="Missing required technology",

                    )

                )

        # ---------------------------------------
        # Sort
        # ---------------------------------------

        keep.sort(
            key=lambda x: x.priority,
            reverse=True,
        )

        add.sort(
            key=lambda x: x.priority,
            reverse=True,
        )

        remove.sort(
            key=lambda x: x.priority,
        )

        return (
            keep,
            remove,
            add,
        )