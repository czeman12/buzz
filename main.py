# main.py

import sys
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import qdarkstyle
from factories.container import Container
from views.title_bar import TitleBar
from utils.scaling_helper import ScalingHelper
from config.app_config import (
    enable_high_dpi_scaling,
    apply_initial_theme,
)
from utils.db_utils import close_all_connections


def main():
    # Enable high DPI scaling
    enable_high_dpi_scaling()

    # Initialize the container
    container = Container()
    container.init_resources()

    # Create the Qt Application
    app = QApplication(sys.argv)

    # Initialize theme controller and apply initial theme
    theme_controller = container.theme_controller()  # This should now work
    apply_initial_theme(app, theme_controller)

    # Use the session resource
    with container.session() as session:  # Now returns a Session instance
        # Initialize controllers that depend on the session

        # Initialize main window
        logging.info("Initializing main window.")
        main_window = QMainWindow()
        main_window.setWindowTitle("Options Trading Tool")
        main_window.setMinimumSize(1600, 1200)
        main_window.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)

        # Set up central widget and layouts
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)
        central_widget.setLayout(central_layout)
        main_window.setCentralWidget(central_widget)

        # Initialize and add TitleBar
        title_bar = TitleBar(parent=main_window, theme_controller=theme_controller)
        central_layout.addWidget(title_bar)

        # Initialize content area
        content_area = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(10, 10, 10, 10)  # Add margins if desired
        content_layout.setSpacing(10)
        content_area.setLayout(content_layout)
        logging.info("Adding content_area to central_layout.")
        central_layout.addWidget(content_area)

        tab_widget = QTabWidget()
        content_layout.addWidget(tab_widget)

        # Get scaling factor
        scaling_factor = ScalingHelper.get_scaling_factor()

        # Get scaled font
        scaled_font = ScalingHelper.get_scaled_font(
            point_size=12,
            family="Arial",
            weight=QFont.Bold,
            scaling_factor=scaling_factor,
        )

        tab_bar = tab_widget.tabBar()
        tab_bar.setFont(scaled_font)

        # Apply initial theme
        initial_theme = "dark"  # Set your default theme here
        apply_initial_theme(app, theme_controller, initial_theme)

        # Show main window
        main_window.show()

        # Start the event loop
        try:
            sys.exit(app.exec_())
        finally:
            close_all_connections()


if __name__ == "__main__":
    main()
