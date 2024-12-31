# utils/document_utils.py


from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

import logging


def add_hyperlink(
    paragraph, url: str, text: str, color: str = "0000FF", underline: bool = True
):
    # Implementation
    pass


def is_pdf(data: bytes) -> bool:
    """
    Check if the given data represents a PDF file.

    :param data: Byte data of the file.
    :return: True if data is a PDF, False otherwise.
    """
    return data.startswith(b"%PDF")


def add_section_break(paragraph: Paragraph) -> None:
    """
    Add a section break to the document.

    :param paragraph: The paragraph object where the section break is to be added.
    """
    try:
        paragraph.add_run().add_break()
        # You can specify the type of section break if needed
    except Exception as e:
        logging.error(f"Failed to add section break: {e}")
        raise


def add_caption(paragraph: Paragraph, caption_text: str) -> None:
    """
    Add a caption below an image in the document.

    :param paragraph: The paragraph object where the image was added.
    :param caption_text: The text for the caption.
    """
    try:
        caption = paragraph.add_run()
        caption.text = f"\n{caption_text}"
        # Optionally, format the caption
        caption.bold = False
        caption.italic = True
        paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    except Exception as e:
        logging.error(f"Failed to add caption: {e}")
        raise
