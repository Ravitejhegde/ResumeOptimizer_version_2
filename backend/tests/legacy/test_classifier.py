from app.services.knowledge.technology_classifier import (
    TechnologyClassifier,
)

tests = [
    "Angular",
    "Spring Boot",
    "MySQL",
    "Docker",
    "AWS",
    "Java",
    "React",
    "Python",
]

print("=" * 60)

for tech in tests:

    print(
        f"{tech:15} -> {TechnologyClassifier.classify(tech)}"
    )