from app.services.docx.loader import DocxLoader
from app.services.docx.parser import DocxParser

from app.services.optimizer.optimization_map import (
    OptimizationMap,
)

document = DocxLoader.load(
    "storage/temp/YOUR_FILE.docx"
)

blocks = DocxParser.parse(document)

maps = []

for block in blocks:

    maps.append(

        OptimizationMap(

            block=block,

            original_text=block.text,

            optimized_text=block.text,

        )

    )

for item in maps:

    print("=" * 50)

    print(item.original_text)

    print(item.optimized_text)

    print(item.approved)