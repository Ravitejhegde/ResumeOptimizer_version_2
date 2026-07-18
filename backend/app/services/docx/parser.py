from email.mime import text

from docx.document import Document

from .document_block import DocumentBlock
from .document_run import DocumentRun
from .paragraph_format import ParagraphFormat
from .section_detector import SectionDetector
from .block_classifier import BlockClassifier


class DocxParser:

    @staticmethod
    def parse(
        document: Document,
    ) -> list[DocumentBlock]:

        blocks: list[DocumentBlock] = []

        block_id = 1

        current_section = ""

        for index, paragraph in enumerate(document.paragraphs):

            # --------------------------------------------------
            # Preserve original spacing
            # --------------------------------------------------

            text = paragraph.text

            if not text.strip():
                continue

            style = paragraph.style.name

            pf = paragraph.paragraph_format

            paragraph_format = ParagraphFormat(

                alignment=paragraph.alignment,

                left_indent=(
                    pf.left_indent.pt
                    if pf.left_indent
                    else None
                ),

                right_indent=(
                    pf.right_indent.pt
                    if pf.right_indent
                    else None
                ),

                first_line_indent=(
                    pf.first_line_indent.pt
                    if pf.first_line_indent
                    else None
                ),

                space_before=(
                    pf.space_before.pt
                    if pf.space_before
                    else None
                ),

                space_after=(
                    pf.space_after.pt
                    if pf.space_after
                    else None
                ),

                line_spacing=pf.line_spacing,

                keep_together=pf.keep_together,

                keep_with_next=pf.keep_with_next,

                page_break_before=pf.page_break_before,

            )

            # --------------------------------------------------
            # Detect Section
            # --------------------------------------------------

            

            current_section = SectionDetector.detect(
                text=text,
                current_section=current_section,
            )
            upper = text.strip().upper()
            # --------------------------------------------------
            # Detect Block Type
            # --------------------------------------------------

            block_type, can_optimize = BlockClassifier.classify(
                text=text,
                style=style,
    current_section=current_section,
)

            if block_type == "heading":

                can_optimize = False

            elif "Title" in style:

                block_type = "title"

                can_optimize = False

            elif upper == current_section:

                block_type = "section"

                can_optimize = False

            elif current_section == "PROJECTS":

                if "•" in text:

                    block_type = "technology"

                    can_optimize = False

                elif len(text) < 70:

                    block_type = "project"

                    can_optimize = False

            elif current_section == "INTERNSHIP EXPERIENCE":

                if "|" in text or "–" in text:

                    block_type = "company"

                    can_optimize = False

            elif current_section == "SKILLS":

                block_type = "skills"

                can_optimize = False

            elif current_section == "EDUCATION":

                block_type = "education"

                can_optimize = False

            elif text.strip().startswith(("•", "-", "·")):

                block_type = "bullet"

                can_optimize = True

            # --------------------------------------------------
            # Runs
            # --------------------------------------------------

            runs: list[DocumentRun] = []

            for run in paragraph.runs:

                color = None

                if run.font.color.rgb:

                    color = str(run.font.color.rgb)

                size = None

                if run.font.size:

                    size = run.font.size.pt

                runs.append(

                    DocumentRun(

                        text=run.text,

                        bold=bool(run.bold),

                        italic=bool(run.italic),

                        underline=bool(run.underline),

                        font_name=run.font.name,

                        font_size=size,

                        color=color,

                    )

                )

            blocks.append(

                DocumentBlock(

                    id=block_id,

                    paragraph_index=index,

                    text=text,

                    block_type=block_type,

                    style=style,

                    runs=runs,

                    paragraph_format=paragraph_format,

                    can_optimize=can_optimize,

                )

            )

            block_id += 1

        return blocks