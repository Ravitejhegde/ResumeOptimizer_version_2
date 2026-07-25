from app.services.docx.loader import DocxLoader
from app.services.docx.parser import DocxParser
from app.services.docx.writer import DocxWriter

document = DocxLoader.load(
    "storage/temp/YOUR_FILE.docx"
)

blocks = DocxParser.parse(document)

for block in blocks:

    if block.can_optimize:

        block.text = (
            "THIS PARAGRAPH WAS MODIFIED BY ResumeOptimizer"
        )

        break

DocxWriter.replace_blocks(
    document,
    blocks,
)

DocxWriter.save(
    document,
    "storage/temp/output.docx",
)

print("Finished")