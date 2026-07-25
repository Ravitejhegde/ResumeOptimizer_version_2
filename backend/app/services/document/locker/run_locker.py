from docx.oxml.ns import qn


class RunLocker:
    """
    Marks runs that should never be modified
    by the optimization engine.
    """

    @classmethod
    def lock(
        cls,
        paragraph,
        runs,
        hyperlinks,
    ) -> None:

        for index, run in enumerate(
            paragraph.runs
        ):

            parent = run._element.getparent()

            if (
                parent is not None
                and parent.tag == qn("w:hyperlink")
            ):

                if index < len(runs):

                    runs[index].editable = False

                    runs[index].object_type = (
                        "hyperlink"
                    )

                    runs[index].locked_reason = (
                        "Hyperlink"
                    )