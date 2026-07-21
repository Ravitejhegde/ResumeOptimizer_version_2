for index, paragraph in enumerate(document.paragraphs):

    if index not in paragraph_updates:
        continue

    ParagraphEditor.replace(
        paragraph,
        paragraph_updates[index],
    )