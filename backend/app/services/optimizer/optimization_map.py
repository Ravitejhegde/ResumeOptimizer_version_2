from dataclasses import dataclass

from app.services.docx.document_block import DocumentBlock


@dataclass
class OptimizationMap:

    block: DocumentBlock

    original_text: str

    optimized_text: str

    approved: bool = False

    modified: bool = False