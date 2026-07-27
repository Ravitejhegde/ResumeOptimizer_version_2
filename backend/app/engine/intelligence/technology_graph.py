from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class TechnologyNode:
    """
    Represents a technology inside the
    ResumeOptimizer knowledge graph.
    """

    name: str

    aliases: list[str] = field(default_factory=list)

    category: str = "Other"

    roles: list[str] = field(default_factory=list)

    priority: int = 50

    related: list[str] = field(default_factory=list)


class TechnologyGraph:
    """
    Central technology knowledge graph.

    Every intelligence module should query
    this graph instead of maintaining its
    own technology lists.
    """

    def __init__(self) -> None:

        self._graph: dict[
            str,
            TechnologyNode,
        ] = {}

        self._build()

    # --------------------------------------------------

    def _build(self) -> None:

        technologies = [

            # ---------------- Backend ----------------

            TechnologyNode(
                name="Python",
                aliases=["python3"],
                category="Backend",
                roles=[
                    "Backend",
                    "Full Stack",
                    "AI/ML",
                    "Data Engineering",
                ],
                priority=100,
                related=[
                    "FastAPI",
                    "Flask",
                    "Django",
                    "SQLAlchemy",
                ],
            ),

            TechnologyNode(
                name="FastAPI",
                category="Backend",
                roles=[
                    "Backend",
                    "Full Stack",
                ],
                priority=96,
                related=[
                    "Python",
                    "REST API",
                    "SQLAlchemy",
                ],
            ),

            TechnologyNode(
                name="Flask",
                category="Backend",
                roles=[
                    "Backend",
                ],
                priority=88,
                related=[
                    "Python",
                ],
            ),

            TechnologyNode(
                name="Django",
                category="Backend",
                roles=[
                    "Backend",
                    "Full Stack",
                ],
                priority=90,
                related=[
                    "Python",
                ],
            ),

            # ---------------- Frontend ----------------

            TechnologyNode(
                name="React",
                aliases=["React.js"],
                category="Frontend",
                roles=[
                    "Frontend",
                    "Full Stack",
                ],
                priority=95,
                related=[
                    "TypeScript",
                    "JavaScript",
                    "HTML",
                    "CSS",
                ],
            ),

            TechnologyNode(
                name="TypeScript",
                category="Frontend",
                roles=[
                    "Frontend",
                    "Full Stack",
                ],
                priority=92,
                related=[
                    "React",
                    "JavaScript",
                ],
            ),

            TechnologyNode(
                name="JavaScript",
                aliases=["JS"],
                category="Frontend",
                roles=[
                    "Frontend",
                    "Full Stack",
                ],
                priority=90,
                related=[
                    "React",
                    "TypeScript",
                ],
            ),

            TechnologyNode(
                name="HTML",
                aliases=["HTML5"],
                category="Frontend",
                priority=75,
            ),

            TechnologyNode(
                name="CSS",
                aliases=["CSS3"],
                category="Frontend",
                priority=75,
            ),

            # ---------------- Database ----------------

            TechnologyNode(
                name="PostgreSQL",
                category="Database",
                priority=90,
            ),

            TechnologyNode(
                name="MySQL",
                category="Database",
                priority=85,
            ),

            TechnologyNode(
                name="Redis",
                category="Database",
                priority=84,
            ),

            TechnologyNode(
                name="SQLAlchemy",
                category="Database",
                priority=88,
                related=[
                    "Python",
                    "PostgreSQL",
                ],
            ),

            # ---------------- Cloud ----------------

            TechnologyNode(
                name="Docker",
                category="Cloud & DevOps",
                priority=90,
            ),

            TechnologyNode(
                name="Kubernetes",
                aliases=["K8s"],
                category="Cloud & DevOps",
                priority=88,
            ),

            TechnologyNode(
                name="AWS",
                category="Cloud & DevOps",
                priority=90,
            ),

            TechnologyNode(
                name="Azure",
                category="Cloud & DevOps",
                priority=85,
            ),

            # ---------------- AI ----------------

            TechnologyNode(
                name="TensorFlow",
                category="AI/ML",
                priority=90,
            ),

            TechnologyNode(
                name="PyTorch",
                category="AI/ML",
                priority=90,
            ),

            TechnologyNode(
                name="OpenCV",
                category="AI/ML",
                priority=88,
            ),

            TechnologyNode(
                name="YOLO",
                category="AI/ML",
                priority=88,
            ),

            TechnologyNode(
                name="LangChain",
                category="AI/ML",
                priority=90,
            ),

            TechnologyNode(
                name="LLM",
                aliases=[
                    "Large Language Models",
                ],
                category="AI/ML",
                priority=92,
            ),

            TechnologyNode(
                name="OpenAI API",
                category="AI/ML",
                priority=90,
            ),

            # ---------------- Testing ----------------

            TechnologyNode(
                name="Pytest",
                aliases=["PyTest"],
                category="Testing",
                priority=80,
            ),

            # ---------------- Tools ----------------

            TechnologyNode(
                name="Git",
                category="Tools",
                priority=90,
            ),

            TechnologyNode(
                name="GitHub",
                category="Tools",
                priority=85,
            ),

            TechnologyNode(
                name="Linux",
                category="Tools",
                priority=82,
            ),

            TechnologyNode(
                name="REST API",
                aliases=["REST"],
                category="Backend",
                priority=90,
            ),
        ]

        for technology in technologies:

            self._graph[
                technology.name.lower()
            ] = technology

            for alias in technology.aliases:

                self._graph[
                    alias.lower()
                ] = technology

    # --------------------------------------------------

    def get(
        self,
        technology: str,
    ) -> TechnologyNode | None:

        return self._graph.get(
            technology.lower()
        )

    def exists(
        self,
        technology: str,
    ) -> bool:

        return (
            technology.lower()
            in self._graph
        )

    def technologies(self) -> list[TechnologyNode]:

        unique = {}

        for node in self._graph.values():

            unique[node.name] = node

        return sorted(
            unique.values(),
            key=lambda item: item.name,
        )




