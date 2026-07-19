from dataclasses import dataclass, field


@dataclass
class TransitionRule:

    source_role: str

    target_role: str

    keep: list[str] = field(default_factory=list)

    remove: list[str] = field(default_factory=list)

    promote: list[str] = field(default_factory=list)


class RoleTransitionEngine:
    """
    Contains recruiter knowledge for moving
    from one role to another.
    """

    RULES = [

        TransitionRule(

            source_role="AI/ML Engineer",

            target_role="Full Stack Developer",

            keep=[

                "python",

                "java",

                "git",

                "sql",

                "rest api",

            ],

            remove=[

                "tensorflow",

                "keras",

                "opencv",

                "yolo",

                "deep learning",

                "machine learning",

            ],

            promote=[

                "react",

                "angular",

                "vue",

                "node.js",

                "express",

                "typescript",

                "ci/cd",

            ],

        ),

        TransitionRule(

            source_role="Backend Developer",

            target_role="Full Stack Developer",

            keep=[

                "java",

                "python",

                "node.js",

                "sql",

                "git",

                "rest api",

            ],

            remove=[],

            promote=[

                "react",

                "angular",

                "vue",

                "typescript",

            ],

        ),

        TransitionRule(

            source_role="Frontend Developer",

            target_role="Full Stack Developer",

            keep=[

                "react",

                "angular",

                "vue",

                "javascript",

                "typescript",

                "git",

            ],

            remove=[],

            promote=[

                "node.js",

                "sql",

                "rest api",

                "express",

            ],

        ),

    ]

    @classmethod
    def find(

        cls,

        source_role: str,

        target_role: str,

    ) -> TransitionRule | None:

        for rule in cls.RULES:

            if (

                rule.source_role == source_role

                and

                rule.target_role == target_role

            ):

                return rule

        return None