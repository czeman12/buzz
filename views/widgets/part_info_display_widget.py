# ./views/widgets/part_info_display_widget.py

from PyQt5.QtWidgets import (
    QLineEdit,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QGraphicsOpacityEffect,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QFontMetrics
import logging

from utils.scalable_widget import ScalableWidget


class PartInfoDisplayWidget(ScalableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        logging.info("PartInfoDisplayWidget initialized.")

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.layout.setAlignment(Qt.AlignLeft)  # Align all contents to the left

        # Placeholder Label
        self.placeholder_label = QLabel("Enter Issue ID to view Part Information")
        self.placeholder_label.setAlignment(Qt.AlignLeft)
        self.placeholder_label.setStyleSheet("color: #aaaaaa;")
        scaled_font = self.get_scaled_font(
            point_size=8, family="Arial", weight=QFont.Bold
        )
        self.placeholder_label.setFont(scaled_font)
        self.layout.addWidget(self.placeholder_label)

        # Part Info Fields Layout
        self.info_layout = QHBoxLayout()
        self.info_layout.setSpacing(10)
        self.layout.addLayout(self.info_layout)

        # Part Number Display
        self.part_number_display = self.create_line_edit("Part Number")
        self.info_layout.addWidget(self.part_number_display)  # No stretch

        # Part Description Display
        self.part_description_display = self.create_line_edit("Description")
        self.info_layout.addWidget(self.part_description_display)  # No stretch

        # Part Revision Display
        self.part_revision_display = self.create_line_edit("Revision")
        self.info_layout.addWidget(self.part_revision_display)  # No stretch

        # Initially hide data displays
        self.part_number_display.hide()
        self.part_description_display.hide()
        self.part_revision_display.hide()

    def on_scaling_updated(self):
        logging.info("Scaling updated in PartInfoDisplayWidget.")
        scaled_font = self.get_scaled_font(
            point_size=8, family="Arial", weight=QFont.Bold
        )
        self.placeholder_label.setFont(scaled_font)
        scaled_font_data = self.get_scaled_font(
            point_size=10, family="Arial", weight=QFont.Normal
        )
        self.part_number_display.setFont(scaled_font_data)
        self.part_description_display.setFont(scaled_font_data)
        self.part_revision_display.setFont(scaled_font_data)

    def create_line_edit(self, placeholder_text):
        line_edit = QLineEdit()
        line_edit.setReadOnly(True)
        line_edit.setStyleSheet(self.get_display_style())
        line_edit.setPlaceholderText(placeholder_text)
        scaled_font = self.get_scaled_font(
            point_size=10, family="Arial", weight=QFont.Normal
        )
        line_edit.setFont(scaled_font)

        if placeholder_text == "Description":
            # For Part Description, set Fixed size policy
            line_edit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        else:
            # For Part Number and Revision, set Fixed size policy
            line_edit.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        return line_edit

    def get_display_style(self):
        return """
            QLineEdit {
                background-color: #2c2c2c;
                border: 1px solid #ffffff;
                border-radius: 4px;
                color: #ffffff;
                padding: 5px;
                font-size: 10pt;
            }
            QLineEdit:read-only {
                color: #ffffff;
            }
        """

    def log_widget_geometries(self):
        logging.debug("Widget Geometries:")
        logging.debug(f"Part Number Display: {self.part_number_display.geometry()}")
        logging.debug(
            f"Part Description Display: {self.part_description_display.geometry()}"
        )
        logging.debug(f"Part Revision Display: {self.part_revision_display.geometry()}")

    def adjust_line_edit_size(self, line_edit: QLineEdit, text: str):
        font_metrics = QFontMetrics(line_edit.font())
        text_width = font_metrics.horizontalAdvance(text) + 20  # Add padding

        line_edit.setFixedWidth(text_width)

    def update_info(self, part_number: str, part_description: str, part_revision: str):
        logging.debug(
            f"Updating Part Info: Number={part_number}, Description={part_description}, Revision={part_revision}"
        )
        part_number = str(part_number)
        part_description = str(part_description)
        part_revision = str(part_revision)

        # Fade out placeholder
        self.fade_out_placeholder()

        # Update data displays
        self.part_number_display.setText(part_number)
        self.part_description_display.setText(part_description)
        self.part_revision_display.setText(part_revision)

        # Hide the placeholder
        self.placeholder_label.hide()

        # Adjust sizes based on content
        self.adjust_line_edit_size(self.part_number_display, part_number)
        self.adjust_line_edit_size(self.part_revision_display, part_revision)
        self.adjust_line_edit_size(self.part_description_display, part_description)

        # Show data displays
        self.part_number_display.show()
        self.part_description_display.show()
        self.part_revision_display.show()

        # Log widget geometries
        self.log_widget_geometries()

    def fade_out_placeholder(self):
        self.opacity_effect = QGraphicsOpacityEffect()
        self.placeholder_label.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.start()
        self.animation.finished.connect(self.hide_placeholder)

    def hide_placeholder(self):
        self.placeholder_label.setVisible(False)
        logging.debug("Placeholder label hidden after fade out.")
