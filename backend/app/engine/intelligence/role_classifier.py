from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class RoleProfile:
    """
    Defines how ResumeOptimizer should
    optimize for a particular role.
    """

    role: str

    primary_categories: list[str]

    secondary_categories: list[str] = field(
        default_factory=list
    )

    ignored_categories: list[str] = field(
        default_factory=list
    )

    category_weights: dict[str, int] = field(
        default_factory=dict
    )


class RoleClassifier:
    """
    Converts a detected role into a
    structured optimization profile.
    """

    ROLE_PROFILES = {

        "Backend Developer": RoleProfile(

            role="Backend Developer",

            primary_categories=[
                "Backend",
                "Database",
            ],

            secondary_categories=[
                "Cloud & DevOps",
                "Tools",
            ],

            ignored_categories=[
                "Frontend",
            ],

            category_weights={

                "Backend":100,

                "Database":90,

                "Cloud & DevOps":75,

                "Tools":60,

                "Frontend":20,

                "AI/ML":20,

                "Testing":50,

            },

        ),

        "Frontend Developer": RoleProfile(

            role="Frontend Developer",

            primary_categories=[
                "Frontend",
            ],

            secondary_categories=[
                "Tools",
            ],

            ignored_categories=[
                "Database",
            ],

            category_weights={

                "Frontend":100,

                "Tools":70,

                "Backend":30,

                "Database":20,

                "Cloud & DevOps":30,

                "Testing":60,

            },

        ),

        "Full Stack Developer": RoleProfile(

            role="Full Stack Developer",

            primary_categories=[

                "Backend",

                "Frontend",

                "Database",

            ],

            secondary_categories=[

                "Cloud & DevOps",

                "Tools",

            ],

            category_weights={

                "Backend":100,

                "Frontend":95,

                "Database":90,

                "Cloud & DevOps":80,

                "Tools":70,

                "Testing":65,

                "AI/ML":40,

            },

        ),

        "AI/ML Engineer": RoleProfile(

            role="AI/ML Engineer",

            primary_categories=[

                "AI/ML",

                "Backend",

            ],

            secondary_categories=[

                "Database",

                "Cloud & DevOps",

            ],

            category_weights={

                "AI/ML":100,

                "Backend":90,

                "Database":75,

                "Cloud & DevOps":70,

                "Tools":60,

                "Frontend":20,

                "Testing":50,

            },

        ),

        "DevOps Engineer": RoleProfile(

            role="DevOps Engineer",

            primary_categories=[

                "Cloud & DevOps",

            ],

            secondary_categories=[

                "Backend",

                "Tools",

            ],

            category_weights={

                "Cloud & DevOps":100,

                "Backend":70,

                "Tools":70,

                "Database":50,

                "Frontend":20,

                "Testing":60,

            },

        ),

    }

    DEFAULT_ROLE = RoleProfile(

        role="General Software Engineer",

        primary_categories=[

            "Backend",

            "Frontend",

        ],

        secondary_categories=[

            "Database",

            "Tools",

        ],

        category_weights={

            "Backend":80,

            "Frontend":80,

            "Database":70,

            "Cloud & DevOps":60,

            "Tools":60,

            "Testing":60,

            "AI/ML":60,

        },

    )

    def classify(
        self,
        role: str,
    ) -> RoleProfile:

        return self.ROLE_PROFILES.get(

            role,

            self.DEFAULT_ROLE,

        )




