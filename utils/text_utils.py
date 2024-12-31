# utils/text_utils.py


def is_pdf(data: bytes) -> bool:
    return data.startswith(b"%PDF")
