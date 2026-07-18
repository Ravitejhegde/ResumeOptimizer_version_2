from app.services.docx.loader import DocxLoader
from app.services.docx.parser import DocxParser

document = DocxLoader.load(
    "storage/temp/YOUR_FILE.docx"
)

blocks = DocxParser.parse(document)

for block in blocks:

    print("=" * 50)

    print("BLOCK")

    print(block.text)

    print("STYLE :", block.style)

    print("TYPE  :", block.block_type)

    print()

    for run in block.runs:

        print(

            run.text,

            "|",

            run.bold,

            "|",

            run.italic,

            "|",

            run.font_name,

            "|",

            run.font_size,

        )