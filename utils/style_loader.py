# utils/style_loader.py

import json
import os
import logging
from typing import Optional


def load_stylesheet(json_path: str) -> Optional[str]:
    """
    Load a JSON file containing Qt styles and convert it into a stylesheet string.

    :param json_path: Path to the JSON stylesheet file.
    :return: A string representing the Qt stylesheet, or None if loading fails.
    """
    if not os.path.exists(json_path):
        logging.error(f"Style JSON file not found at: {json_path}")
        return None

    try:
        with open(json_path, "r") as file:
            style_dict = json.load(file)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from {json_path}: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error loading JSON from {json_path}: {e}")
        return None

    qss = ""
    for selector, properties in style_dict.items():
        qss += f"{selector} {{\n"
        for prop, value in properties.items():
            qss += f"    {prop}: {value};\n"
        qss += "}\n\n"

    logging.info(f"Stylesheet successfully loaded from {json_path}.")
    return qss


def apply_stylesheet(app, json_path: str) -> bool:
    """
    Apply the stylesheet to the entire application.

    :param app: The QApplication instance.
    :param json_path: Path to the JSON stylesheet file.
    :return: True if stylesheet applied successfully, False otherwise.
    """
    try:
        stylesheet = load_stylesheet(json_path)
        if stylesheet:
            app.setStyleSheet(stylesheet)
            logging.info("Stylesheet applied to the application.")
            return True
        else:
            logging.error(
                "Failed to load stylesheet. Application will use default styles."
            )
            return False
    except Exception as e:
        logging.error(f"Failed to apply stylesheet from {json_path}: {e}")
        return False
