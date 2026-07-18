from app.services.writer.block_merger import (
    BlockMerger,
)

from app.services.docx.document_block import (
    DocumentBlock,
)

blocks = [

    DocumentBlock(
        id=1,
        paragraph_index=0,
        text="Original Summary",
        block_type="paragraph",
        style="Normal",
    ),

    DocumentBlock(
        id=2,
        paragraph_index=1,
        text="Original Bullet",
        block_type="bullet",
        style="List Bullet",
    ),
]

ai_response = {
    "version": 1,
    "blocks": [
        {
            "id": 2,
            "status": "updated",
            "text": "Updated Bullet",
        }
    ]
}

updated = BlockMerger.merge(
    blocks,
    ai_response,
)

print("=" * 60)

for block in updated:
    print(
        block.id,
        block.text,
    )