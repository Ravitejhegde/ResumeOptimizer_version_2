from app.services.knowledge.section_detector import (
    SectionDetector,
)

tests = [
    "Professional Summary",
    "Summary",
    "Internship Experience",
    "Projects",
    "Technical Skills",
    "Education",
    "Certificates",
    "Languages",
]

print("=" * 60)

for text in tests:

    print(
        f"{text:25} -> {SectionDetector.detect(text)}"
    )