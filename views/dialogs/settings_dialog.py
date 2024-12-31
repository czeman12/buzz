# ui/dialogs/settings_dialog.py

import os
import logging
import json
from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
    QSizePolicy,
    QMessageBox,
    QComboBox,
    QLineEdit,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class SettingsDialog(QDialog):
    def __init__(self, parent=None, theme_controller=None):
        super().__init__(parent)
        self.theme_controller = theme_controller  # Store the ThemeController instance

        # Set minimum size for the dialog
        self.setMinimumSize(500, 300)  # Adjust width and height as needed

        # **Updated Window Flags**
        # Changed from Qt.Popup to Qt.Dialog to ensure proper dialog behavior
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        # Optionally, add Qt.WindowStaysOnTopHint if you want the dialog to stay above other windows
        # self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # Main layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.main_layout)

        # Title Bar
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(30)
        self.title_bar.setObjectName("TitleBar")
        self.title_layout = QHBoxLayout()
        self.title_layout.setContentsMargins(10, 0, 10, 0)
        self.title_bar.setLayout(self.title_layout)

        # **Updated: Title Label with Image Instead of Text**
        self.title_label = QLabel()
        self.title_label.setObjectName("TitleLabel")  # Assign object name for styling

        # Load the pixmap
        image_path = os.path.join("assets", "logos", "menu.png")
        if not os.path.exists(image_path):
            logging.error(f"Settings icon not found at {image_path}.")
            # Fallback to text if image not found
            self.title_label.setText("Settings")
            self.title_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        else:
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                logging.error(f"Failed to load image from {image_path}.")
                self.title_label.setText("Settings")
                self.title_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
            else:
                logging.debug(f"Loaded image from {image_path}.")
                # Optionally, scale the pixmap if it's too large
                scaled_pixmap = pixmap.scaled(
                    24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
                self.title_label.setPixmap(scaled_pixmap)
                self.title_label.setText("")  # Ensure no text is displayed
                self.title_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                # Optionally, set a tooltip for accessibility
                self.title_label.setToolTip("Settings")

        # **Optional Debugging: Add a border to visualize the QLabel**
        # self.title_label.setStyleSheet("border: 1px solid red;")

        self.title_layout.addWidget(self.title_label)

        # Add stretch to push the close button to the right
        self.title_layout.addStretch()

        # Close Button
        self.close_button = QPushButton("X")
        self.close_button.setFixedSize(20, 20)
        self.close_button.clicked.connect(self.reject)
        self.title_layout.addWidget(self.close_button)

        # Content Widget
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(0, 10, 0, 0)  # Add some top margin
        self.content_widget.setLayout(self.content_layout)

        # Add theme toggle dropdown
        self.add_theme_toggle()

        # Add other settings as needed...

        # Add stretch to push content to the top
        self.content_layout.addStretch()

        # Add title bar and content to the main layout
        self.main_layout.addWidget(self.title_bar)
        self.main_layout.addWidget(self.content_widget)

        # Apply default styles
        self.apply_styles()

    def apply_styles(self):
        """
        Apply default styles to the dialog and its components.
        """
        self.setStyleSheet(
            """
            QWidget {
                background-color: #2c2c2c;
            }
            QWidget#TitleBar {
                background-color: #1c1c1c;
            }
            QLabel#TitleLabel {
                /* Remove any color settings that might interfere with pixmap */
                color: transparent;
            }
            QLabel {
                color: #f0f0f0;
            }
            QPushButton {
                background-color: transparent;
                border: none;
                color: #f0f0f0;
                font-weight: bold;
            }
            QPushButton:hover {
                color: red;
            }
            QLineEdit {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                padding: 5px;
                color: #ffffff;
            }
            QComboBox {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                padding: 5px;
                color: #ffffff;
            }
            """
        )

    def add_theme_toggle(self):
        """
        Add a dropdown menu to toggle themes.
        """
        # Theme Label
        theme_label = QLabel("Select Theme:")
        theme_label.setStyleSheet("color: white;")
        self.content_layout.addWidget(theme_label)

        # Theme Dropdown
        self.theme_combo_box = QComboBox()
        self.theme_combo_box.setStyleSheet("color: white;")
        self.content_layout.addWidget(self.theme_combo_box)

        # Populate theme options (example)
        self.theme_combo_box.addItems(["Light", "Dark", "System Default"])
        self.theme_combo_box.currentTextChanged.connect(self.on_theme_change)

    def on_theme_change(self, theme_name):
        """
        Handle theme change selection.
        """
        if self.theme_controller:
            self.theme_controller.set_theme(theme_name)
        else:
            logging.warning("ThemeController not set.")

    # You can add more methods and settings as needed...
