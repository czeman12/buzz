# views/widgets/heatmap_widget.py

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

import logging


class HeatmapWidget(QWidget):
    """
    Temporary HeatmapWidget placeholder.
    This widget is intended to display heatmaps in the future.
    """

    def __init__(self, parent=None):
        """
        Initialize the HeatmapWidget.

        :param parent: Parent widget.
        """
        super().__init__(parent)
        self.init_ui()
        logging.info("HeatmapWidget initialized (placeholder).")

    def init_ui(self):
        """
        Initialize the UI components and layout.
        """
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Placeholder label indicating future implementation
        placeholder_label = QLabel("Heatmap Widget - To Be Implemented")
        placeholder_label.setStyleSheet("font-size: 16px; color: gray;")
        placeholder_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(placeholder_label)
