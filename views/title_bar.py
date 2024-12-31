# views/title_bar.py

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QSpacerItem,
    QSizePolicy,
    QLabel,
)
import logging

from utils.scalable_widget import ScalableWidget


class TitleBar(ScalableWidget):
    """
    Custom title bar widget with scalable fonts.
    Inherits from ScalableWidget to support dynamic font scaling.
    """

    def __init__(self, parent=None, theme_controller=None, container=None):
        super().__init__(parent)
        self.parent = parent
        self.initTitleBar()
        self.theme_controller = theme_controller
        self.container = container  # Dependency Injection Container
        self.start = QPoint(0, 0)
        self.pressing = False

        logging.info("Initialized the correct TitleBar instance")

    def initTitleBar(self):
        self.setFixedHeight(40)
        self.setObjectName("TitleBar")

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10, 0, 10, 0)
        self.setLayout(self.layout)

        # Calculate scaling factor
        scaling_factor = self.scaling_factor

        # Title Label
        self.title_label = QLabel("Options Analysis Tool")
        self.title_label.setStyleSheet("color: white;")

        # Set scaled font
        scaled_font = self.get_scaled_font(
            point_size=14, family="Arial", weight=QFont.Bold
        )
        self.title_label.setFont(scaled_font)
        self.layout.addWidget(self.title_label)

        # Spacer to push toggle to the right
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout.addItem(spacer)

        # Spacer to push window control buttons to the right
        self.layout.addStretch()

        # Minimize Button
        self.min_btn = QPushButton("-")
        self.min_btn.setFixedSize(30, 30)
        self.min_btn.setObjectName("MinimizeButton")
        self.min_btn.clicked.connect(self.parent.showMinimized)
        self.layout.addWidget(self.min_btn)

        # Maximize/Restore Button
        self.max_btn = QPushButton("□")
        self.max_btn.setFixedSize(30, 30)
        self.max_btn.setObjectName("MaximizeButton")
        self.max_btn.clicked.connect(self.toggle_maximize_restore)
        self.layout.addWidget(self.max_btn)

        # Close Button
        self.close_btn = QPushButton("×")
        self.close_btn.setFixedSize(30, 30)
        self.close_btn.setObjectName("CloseButton")
        self.close_btn.clicked.connect(self.parent.close)
        self.layout.addWidget(self.close_btn)

    def toggle_maximize_restore(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
            self.max_btn.setText("□")
        else:
            self.parent.showMaximized()
            self.max_btn.setText("❐")

    # Implement window dragging
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start = event.globalPos()
            self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            delta = event.globalPos() - self.start
            self.parent.move(self.parent.x() + delta.x(), self.parent.y() + delta.y())
            self.start = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.pressing = False

    def update_theme(self, theme_data):
        """
        Update the title bar's theme based on the provided theme data.
        :param theme_data: A dictionary containing theme-related styles.
        """
        if not theme_data:
            logging.error("No theme data provided to update_theme.")
            return

        titlebar_styles = theme_data.get("TitleBar", {})
        bg_color = titlebar_styles.get("background-color", "#2e2e2e")  # Default color

        # Apply the new background color to the title bar
        self.setStyleSheet(f"background-color: {bg_color};")

        # Update button styles if needed (for example, text color, hover color)
        button_styles = titlebar_styles.get("button-styles", "")
        self.min_btn.setStyleSheet(button_styles)
        self.max_btn.setStyleSheet(button_styles)
        self.close_btn.setStyleSheet(button_styles)

    def on_scaling_updated(self):
        """
        Override the method to update fonts when scaling changes.
        """
        logging.info("Scaling updated in TitleBar.")
        # Update title_label font
        scaled_font = self.get_scaled_font(
            point_size=14, family="Arial", weight=QFont.Bold
        )
        self.title_label.setFont(scaled_font)
        # Optionally, update button fonts or other elements if necessary
