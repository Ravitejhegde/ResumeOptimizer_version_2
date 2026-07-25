from docx.oxml.ns import qn


class XmlUtils:
    """
    Utility methods for working with
    WordprocessingML (DOCX XML).
    """

    @staticmethod
    def is_hyperlink(node) -> bool:
        """Return True if the XML node is a hyperlink."""
        return (
            node is not None
            and node.tag == qn("w:hyperlink")
        )

    @staticmethod
    def is_run(node) -> bool:
        """Return True if the XML node is a run."""
        return (
            node is not None
            and node.tag == qn("w:r")
        )

    @staticmethod
    def get_relationship_id(node) -> str:
        """Return the relationship ID (r:id)."""
        if node is None:
            return ""

        return node.get(
            qn("r:id"),
            "",
        )

    @staticmethod
    def get_bookmark(node) -> str:
        """Return the bookmark (w:anchor)."""
        if node is None:
            return ""

        return node.get(
            qn("w:anchor"),
            "",
        )

    @staticmethod
    def get_text_nodes(run_node):
        """Return all text nodes (<w:t>) in a run."""
        if run_node is None:
            return []

        return run_node.findall(
            ".//" + qn("w:t")
        )

    @staticmethod
    def clear_text(run_node) -> None:
        """Clear all text in a run."""
        for text_node in XmlUtils.get_text_nodes(run_node):
            text_node.text = ""

    @staticmethod
    def set_text(run_node, text: str) -> None:
        """Set text in the first text node of a run."""
        nodes = XmlUtils.get_text_nodes(run_node)

        if not nodes:
            return

        nodes[0].text = text