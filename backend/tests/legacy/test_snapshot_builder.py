from app.document.parser.snapshot_builder import (
    SnapshotBuilder,
)

snapshot = SnapshotBuilder.build(
    "storage/temp/Ravitej_Hegde_Resume_Fullstack.docx"
)

print("=" * 60)
print("Total Paragraphs:", len(snapshot.paragraphs))
print("=" * 60)

# Inspect Paragraph 4 (index = 3)
paragraph = snapshot.paragraphs[3]

print("\nDETAILED PARAGRAPH INSPECTION")
print("=" * 60)
print("Text:")
print(repr(paragraph.text))
print()

print("Style:", paragraph.style)
print("Runs:", len(paragraph.runs))
print("=" * 60)

for i, run in enumerate(paragraph.runs, start=1):

    print(f"Run {i}")

    print("Text      :", repr(run.text))
    print("Bold      :", run.bold)
    print("Italic    :", run.italic)
    print("Underline :", run.underline)
    print("Font      :", run.font_name)
    print("Font Size :", run.font_size)
    print("Color     :", run.color)

    print("-" * 60)

print("\nFIRST FIVE PARAGRAPHS")
print("=" * 60)

for i, p in enumerate(snapshot.paragraphs[:5], start=1):

    print(f"Paragraph {i}")

    print("Style :", p.style)
    print("Text  :", repr(p.text))
    print("Runs  :", len(p.runs))

    print("-" * 60)