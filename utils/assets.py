# utils/assets.py

import os
from PyQt5.QtGui import QIcon
import logging


def get_icon_path(filename: str) -> str:
    """
    Returns the absolute path to the specified icon file.
    """
    script_dir = os.path.dirname(os.path.realpath(__file__))
    icon_path = os.path.join(script_dir, "assets", "logos", filename)
    if not os.path.exists(icon_path):
        logging.error(f"Icon file not found at: {icon_path}")
    return icon_path


def load_application_icon() -> QIcon:
    """
    Loads and returns the application icon.
    """
    icon_path = get_icon_path("Joby_Aviation_Logo (Heart).ico")
    if os.path.exists(icon_path):
        return QIcon(icon_path)
    else:
        logging.warning("Application icon not set due to missing icon file.")
        return QIcon()  # Return a default empty icon


def load_titlebar_icon() -> QIcon:
    """
    Loads and returns the title bar icon if needed.
    """
    # If you have a separate icon for the title bar, specify it here
    return load_application_icon()
