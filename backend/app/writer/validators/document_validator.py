"""
app.writer.validators.document_validator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Validates the Writer context and protects the
original DOCX structure and formatting.
"""

from __future__ import annotations

import hashlib
import re

from docx.document import Document as DocxDocument

from app.writer.models.write_context import WriteContext


class DocumentValidator:
    """
    Validates the Writer document before export.

    The original DOCX is the formatting authority.

    The validator creates a structural/formatting
    fingerprint while ignoring editable text content.
    """

    def validate(
        self,
        context: WriteContext,
    ) -> None:
        """
        Perform basic validation and formatting
        preservation validation.
        """

        if context.working_document is None:
            context.add_error(
                "Working document is missing."
            )

        if context.document is None:
            context.add_error(
                "Document model is missing."
            )

        if context.optimization is None:
            context.add_error(
                "Optimization result is missing."
            )

        if context.format_fingerprint is None:
            context.add_error(
                "Original format fingerprint is missing."
            )
        else:
            self.validate_format_preservation(
                context
            )

    # =================================================
    # Fingerprinting
    # =================================================

    def create_format_fingerprint(
        self,
        document: DocxDocument,
    ) -> str:
        """
        Create a fingerprint representing the DOCX
        structure and formatting while ignoring
        editable text content.
        """

        package_parts = self._collect_package_parts(
            document
        )

        normalized_parts: list[str] = []

        for part_name, xml_content in package_parts:
            normalized_xml = self._normalize_xml(
                xml_content
            )

            normalized_parts.append(
                f"{part_name}\n{normalized_xml}"
            )

        complete_content = "\n".join(
            normalized_parts
        )

        return hashlib.sha256(
            complete_content.encode("utf-8")
        ).hexdigest()

    # =================================================
    # Format Preservation
    # =================================================

    def validate_format_preservation(
        self,
        context: WriteContext,
    ) -> None:
        """
        Verify that the working document has retained
        the original DOCX structure and formatting.

        Text content is intentionally ignored because
        changing approved text is Writer's responsibility.
        """

        if context.format_fingerprint is None:
            context.add_error(
                "Cannot validate formatting because "
                "the original fingerprint is missing."
            )
            return

        working_fingerprint = (
            self.create_format_fingerprint(
                context.working_document
            )
        )

        if (
            working_fingerprint
            != context.format_fingerprint
        ):
            context.add_error(
                "Writer changed the original DOCX "
                "structure or formatting."
            )

    # =================================================
    # Diagnostic
    # =================================================

    def debug_format_difference(
        self,
        original: DocxDocument,
        working: DocxDocument,
    ) -> None:
        """
        Print a compact description of the first XML
        difference between the original and working documents.

        This method is diagnostic only.
        It does not modify either document.
        """

        original_parts = dict(
            self._collect_package_parts(
                original
            )
        )

        working_parts = dict(
            self._collect_package_parts(
                working
            )
        )

        all_parts = sorted(
            set(original_parts)
            | set(working_parts)
        )

        for part_name in all_parts:
            original_xml = self._normalize_xml(
                original_parts.get(
                    part_name,
                    "",
                )
            )

            working_xml = self._normalize_xml(
                working_parts.get(
                    part_name,
                    "",
                )
            )

            if original_xml == working_xml:
                continue

            print(
                "\nDIFFERENT PART:",
                part_name,
            )

            min_length = min(
                len(original_xml),
                len(working_xml),
            )

            difference_index: int | None = None

            for index in range(min_length):
                if (
                    original_xml[index]
                    != working_xml[index]
                ):
                    difference_index = index
                    break

            if difference_index is None:
                difference_index = min_length

            context_radius = 250

            start = max(
                0,
                difference_index - context_radius,
            )

            original_end = min(
                len(original_xml),
                difference_index + context_radius,
            )

            working_end = min(
                len(working_xml),
                difference_index + context_radius,
            )

            print(
                "DIFFERENCE INDEX:",
                difference_index,
            )

            print(
                "\nORIGINAL CONTEXT:\n",
                original_xml[start:original_end],
            )

            print(
                "\nWORKING CONTEXT:\n",
                working_xml[start:working_end],
            )

            # Only inspect the first different XML part.
            break

    # =================================================
    # Package Inspection
    # =================================================

    def _collect_package_parts(
        self,
        document: DocxDocument,
    ) -> list[tuple[str, str]]:
        """
        Collect XML parts belonging to the DOCX package.

        Binary resources such as images are not fingerprinted
        here. They remain part of the original DOCX package
        because Writer starts from a deep copy.
        """

        parts: list[tuple[str, str]] = []

        package = document.part.package

        for part in package.iter_parts():
            part_name = str(part.partname)

            if not part_name.lower().endswith(".xml"):
                continue

            try:
                blob = part.blob
                xml_content = blob.decode("utf-8")
            except (
                AttributeError,
                UnicodeDecodeError,
            ):
                continue

            parts.append(
                (
                    part_name,
                    xml_content,
                )
            )

        parts.sort(
            key=lambda item: item[0]
        )

        return parts

    # =================================================
    # XML Normalization
    # =================================================

    def _normalize_xml(
        self,
        xml_content: str,
    ) -> str:
        """
        Normalize XML before fingerprinting.

        Editable text content is removed because Writer
        is explicitly allowed to modify approved text.

        Formatting and structural XML remain.
        """

        normalized = xml_content

        # ---------------------------------------------
        # Remove editable Word text nodes
        # ---------------------------------------------

        normalized = re.sub(
            r"<w:t(?:\s[^>]*)?>.*?</w:t>",
            "<w:t></w:t>",
            normalized,
            flags=re.DOTALL,
        )

        normalized = re.sub(
            r"<w:delText(?:\s[^>]*)?>.*?</w:delText>",
            "<w:delText></w:delText>",
            normalized,
            flags=re.DOTALL,
        )

        normalized = re.sub(
            r"<w:instrText(?:\s[^>]*)?>.*?</w:instrText>",
            "<w:instrText></w:instrText>",
            normalized,
            flags=re.DOTALL,
        )

        # ---------------------------------------------
        # Remove xml:space
        # ---------------------------------------------

        normalized = re.sub(
            r'\s+xml:space="preserve"',
            "",
            normalized,
        )

        # ---------------------------------------------
        # Remove insignificant XML whitespace
        # ---------------------------------------------

        normalized = re.sub(
            r">\s+<",
            "><",
            normalized,
        )

        return normalized.strip()