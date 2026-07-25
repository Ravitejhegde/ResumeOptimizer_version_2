from app.services.docx.loader import DocxLoader
from app.services.docx.parser import DocxParser

from app.services.optimizer.optimization_map import (
    OptimizationMap,
)

from app.services.optimizer.paragraph_optimizer import (
    ParagraphOptimizer,
)

from app.services.optimizer.validator import (
    OptimizationValidator,
)

document = DocxLoader.load(
    "storage/temp/YOUR_FILE.docx"
)

blocks = DocxParser.parse(document)

for block in blocks:

    item = OptimizationMap(

        block=block,

        original_text=block.text,

        optimized_text=block.text,

    )

    item = ParagraphOptimizer.optimize(item)

    valid, reason = (

        OptimizationValidator.validate(item)

    )

    print("=" * 60)

    print(item.original_text)

    print()

    print(item.optimized_text)

    print()

    print(valid)

    print(reason)