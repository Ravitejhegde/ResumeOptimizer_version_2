class OptimizationRules:
    """
    Resume optimization rules based on
    career transition.
    """

    DEFAULT_RULES = """
General Rules

- Replace instead of append whenever possible.
- Keep resume length approximately the same.
- Never keyword stuff.
- Preserve readability.
- Preserve ATS compatibility.
- Do not modify factual information.
"""

    ROLE_RULES = {

        (
            "AI/ML Engineer",
            "Full Stack Developer",
        ): """
Career Transition

AI/ML Engineer → Full Stack Developer

Priority

KEEP

- Python
- Java
- SQL
- Git
- REST API

REMOVE WHEN NECESSARY

- TensorFlow
- Keras
- YOLO
- OpenCV
- Deep Learning
- Machine Learning

PROMOTE

- React
- Angular
- Vue
- Node.js
- Express
- TypeScript
- CI/CD

Always replace low-priority AI technologies
before adding new frontend technologies.
""",

        (
            "Backend Developer",
            "Full Stack Developer",
        ): """
Career Transition

Backend → Full Stack

Keep backend strengths.

Promote

- React
- Angular
- Vue
- TypeScript
""",

        (
            "Frontend Developer",
            "Full Stack Developer",
        ): """
Career Transition

Frontend → Full Stack

Keep frontend technologies.

Promote

- Node.js
- REST API
- SQL
- Express
"""
    }

    @classmethod
    def build(

        cls,

        source_role: str,

        target_role: str,

    ) -> str:

        role_rules = cls.ROLE_RULES.get(

            (

                source_role,

                target_role,

            ),

            "",

        )

        return (

            cls.DEFAULT_RULES

            + "\n\n"

            + role_rules

        )