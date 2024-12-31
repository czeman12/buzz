# controllers/theme_controller.py

from PyQt5.QtCore import QObject, pyqtSignal
import logging
from services.theme_service import ThemeService


class ThemeController(QObject):
    theme_changed = pyqtSignal(dict)  # Emit theme data as dict

    def __init__(self, theme_service: ThemeService = None):
        """
        Initialize the ThemeController.

        :param theme_service: An instance of ThemeService to manage themes.
        """
        super().__init__()
        self.theme_service = theme_service or ThemeService()
        self.current_theme = self.theme_service.current_theme
        logging.info("ThemeController initialized.")

    def change_theme(self, theme_name: str):
        """
        Change the application theme.

        :param theme_name: The name of the theme to apply.
        """
        if theme_name != self.current_theme:
            theme_data = self.theme_service.load_theme(theme_name)
            if theme_data:
                self.theme_service.apply_theme(theme_data)
                self.theme_changed.emit(theme_data)
                self.current_theme = theme_name
                logging.info(f"Theme changed to '{theme_name}'.")
            else:
                logging.error(f"Failed to load theme '{theme_name}'.")
