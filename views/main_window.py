# views/main_window.py

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget
from PyQt5.QtGui import QIcon
import logging
import os
import json


class MainWindow(QMainWindow):
    def __init__(self, app):
        """
        Initialize the MainWindow with the given QApplication instance.

        :param app: The QApplication instance.
        """
        super().__init__()
        self.app = app  # Keep a reference to the QApplication
        self.setWindowTitle("Airframe Assembly Stress Tool")
        self.resize(1200, 800)
        self.setup_ui()
        logging.info("MainWindow initialized.")

    def setup_ui(self):
        """
        Set up the main window UI components, including the dark theme and tab widget.
        """
        # Apply the dark theme
        self.apply_dark_theme()

        # Set window icon (optional)
        icons_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "logos")
        icon_path = os.path.join(icons_dir, "Joby_Aviation_Logo (Heart).ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            logging.warning(f"Icon not found at path: {icon_path}")

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout for the central widget
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Tab widget to hold different views
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        logging.info("Main window UI setup complete.")

    def add_tab(self, widget: QWidget, title: str):
        """
        Add a new tab to the tab widget.

        :param widget: The QWidget to add as a tab.
        :param title: The title of the tab.
        """
        self.tabs.addTab(widget, title)
        logging.info(f"Tab '{title}' added to main window.")

    def apply_dark_theme(self):
        """
        Apply the dark theme to the application by loading the stylesheet.
        """
        styles_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "styles")
        dark_theme_path = os.path.join(styles_dir, "dark_theme.json")
        if os.path.exists(dark_theme_path):
            try:
                with open(dark_theme_path, "r") as f:
                    theme_data = json.load(f)
                stylesheet = theme_data.get("stylesheet", "")
                self.app.setStyleSheet(stylesheet)
                logging.info("Dark theme applied successfully.")
            except Exception as e:
                logging.error(f"Failed to apply dark theme: {e}")
        else:
            logging.warning(f"Dark theme file not found at path: {dark_theme_path}")
