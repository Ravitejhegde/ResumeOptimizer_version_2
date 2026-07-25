from app.services.docx.loader import DocxLoader
from app.services.docx.parser import DocxParser

from app.services.optimizer.optimization_map import (
    OptimizationMap,
)

from app.services.optimizer.paragraph_optimizer import (
    ParagraphOptimizer,
)

document = DocxLoader.load(
    "storage/temp/YOUR_FILE.docx"
)

blocks = DocxParser.parse(document)

maps = []

for block in blocks:

    item = OptimizationMap(

        block=block,

        original_text=block.text,

        optimized_text=block.text,

    )

    maps.append(

        ParagraphOptimizer.optimize(item)

    )

for item in maps:

    print("=" * 60)

    print("Original :")

    print(item.original_text)

    print()

    print("Optimized :")

    print(item.optimized_text)