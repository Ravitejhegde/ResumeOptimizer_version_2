from docx import Document

from app.services.docx.parser import DocxParser
from app.services.writer.docx_writer import DocxWriter

# Load Resume
input_file = "storage/temp/YOUR_FILE.docx"

document = Document(input_file)

# Parse
blocks = DocxParser.parse(document)

# Simulate AI Update
blocks[0].text = "THIS IS A TEST FROM DOCX WRITER"

# Save
DocxWriter.write(
    input_path=input_file,
    blocks=blocks,
    output_path="storage/exports/Test_Output.docx",
)

print("=" * 60)
print("DOCX written successfully!")