from docx import Document

from app.services.docx.parser import DocxParser
from app.services.planner.optimization_planner import (
    OptimizationPlanner,
)

# Load Resume
document = Document("storage/temp/YOUR_FILE.docx")

# Parse Resume
blocks = DocxParser.parse(document)

# Plan Optimization
selected_blocks = OptimizationPlanner.plan(blocks)

print("=" * 70)
print(f"Total Blocks      : {len(blocks)}")
print(f"Selected for AI   : {len(selected_blocks)}")
print("=" * 70)

for i, block in enumerate(selected_blocks, start=1):

    print(f"\n[{i}] {block.block_type}")
    print("-" * 50)
    print(block.text)