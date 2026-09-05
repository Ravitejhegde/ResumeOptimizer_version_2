from app.knowledge.knowledge_manager import KnowledgeManager
from app.optimizer.models.paragraph_update import ParagraphUpdate
from app.optimizer.validators.ai_response_validator import (
    AIResponseValidator,
)


def _request(
    original_paragraph: str,
    authorized_skills: list[str],
):
    class Knowledge:
        def __init__(self):
            self.optimization_skills = []

            for skill in authorized_skills:
                self.optimization_skills.append(
                    type(
                        "Skill",
                        (),
                        {
                            "canonical": skill,
                        },
                    )()
                )

    class SectionPlan:
        paragraph_ids = {
            "skills": ["p0"],
        }

    class Blueprint:
        section_plan = SectionPlan()
        knowledge = Knowledge()

    class Document:
        paragraphs = [original_paragraph]

    class Request:
        document = Document()
        blueprint = Blueprint()

    return Request()


def _update(
    original_text: str,
    optimized_text: str,
) -> ParagraphUpdate:

    return ParagraphUpdate(
        paragraph_id="p0",
        section="Skills",
        original_text=original_text,
        optimized_text=optimized_text,
        confidence=0.95,
        reason="test",
        approved=True,
        formatting_safe=True,
    )


def test_authorized_new_technology_is_allowed():
    validator = AIResponseValidator(
        KnowledgeManager()
    )

    original = (
        "Tools & Platforms: Git, GitHub, Postman"
    )

    optimized = (
        "Tools & Platforms: Git, GitHub, "
        "Docker, Postman"
    )

    request = _request(
        original,
        ["docker"],
    )

    errors = validator.validate(
        [_update(original, optimized)],
        request,
    )

    assert errors == []


def test_unauthorized_new_technology_is_rejected():
    validator = AIResponseValidator(
        KnowledgeManager()
    )

    original = (
        "Tools & Platforms: Git, GitHub, Postman"
    )

    optimized = (
        "Tools & Platforms: Git, GitHub, "
        "Kubernetes, Postman"
    )

    request = _request(
        original,
        ["docker"],
    )

    errors = validator.validate(
        [_update(original, optimized)],
        request,
    )

    assert any(
        "unauthorized" in error.lower()
        for error in errors
    )


def test_existing_technology_is_allowed():
    validator = AIResponseValidator(
        KnowledgeManager()
    )

    original = (
        "Tools & Platforms: Git, GitHub, Docker"
    )

    optimized = (
        "Tools & Platforms: Git, GitHub, "
        "Docker, Postman"
    )

    request = _request(
        original,
        ["docker"],
    )

    errors = validator.validate(
        [_update(original, optimized)],
        request,
    )

    assert errors == []