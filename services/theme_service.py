# services/theme_service.py

import os
import json
import logging
from PyQt5.QtWidgets import QApplication


class ThemeService:
    """
    Service to manage application themes.
    """

    def __init__(self, default_theme: str = "dark"):
        self.current_theme = None
        self.default_theme = default_theme
        logging.info("ThemeService initialized.")

    def load_theme(self, theme_name: str) -> dict:
        """
        Load a theme from a JSON file.

        :param theme_name: Name of the theme (e.g., 'dark', 'light').
        :return: theme_data dictionary or empty dict if failed.
        """
        theme_file = os.path.join("assets", "styles", f"{theme_name}_theme.json")
        if not os.path.exists(theme_file):
            logging.error(f"Theme file '{theme_file}' does not exist.")
            if theme_name != self.default_theme:
                logging.info(
                    f"Attempting to load default theme '{self.default_theme}'."
                )
                return self.load_theme(self.default_theme)
            else:
                logging.critical("Default theme is missing. Cannot apply theme.")
                return {}
        try:
            with open(theme_file, "r") as f:
                theme_data = json.load(f)
            logging.info(f"Theme '{theme_name}' loaded successfully.")
            return theme_data
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error in theme '{theme_name}': {e}")
            if theme_name != self.default_theme:
                logging.info(
                    f"Attempting to load default theme '{self.default_theme}'."
                )
                return self.load_theme(self.default_theme)
            else:
                logging.critical("Default theme JSON is invalid. Cannot apply theme.")
                return {}
        except Exception as e:
            logging.error(f"Failed to load theme '{theme_name}': {e}")
            if theme_name != self.default_theme:
                logging.info(
                    f"Attempting to load default theme '{self.default_theme}'."
                )
                return self.load_theme(self.default_theme)
            else:
                logging.critical("Default theme failed to load. Cannot apply theme.")
                return {}

    def apply_theme(self, theme_data: dict):
        """
        Apply the theme by setting the application's style sheet.

        :param theme_data: Dictionary containing theme styles.
        """
        if not theme_data:
            logging.error("No theme data to apply.")
            return
        try:
            style_sheet = self.generate_style_sheet(theme_data)
            QApplication.instance().setStyleSheet(style_sheet)
            logging.debug("Theme applied successfully.")
        except Exception as e:
            logging.error(f"Failed to apply theme: {e}")

    def generate_style_sheet(self, theme_data: dict) -> str:
        """
        Generate a style sheet string from theme data.

        :param theme_data: Dictionary containing theme styles.
        :return: A string representing the style sheet.
        """
        style_sheet = ""
        for selector, styles in theme_data.items():
            style_sheet += f"{selector} {{\n"
            for prop, value in styles.items():
                style_sheet += f"    {prop}: {value};\n"
            style_sheet += "}\n"
        return style_sheet

    def get_available_themes(self) -> list:
        """
        Get a list of available themes based on JSON files in the styles directory.

        :return: List of theme names.
        """
        styles_dir = os.path.join("assets", "styles")
        themes = []
        try:
            for file in os.listdir(styles_dir):
                if file.endswith("_theme.json"):
                    theme = file.replace("_theme.json", "")
                    themes.append(theme)
            logging.debug(f"Available themes: {themes}")
            return themes
        except Exception as e:
            logging.error(f"Failed to list available themes: {e}")
            return []
