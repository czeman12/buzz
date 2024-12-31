# views/widgets/vtk_widget.py

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

import logging


class VTKWidget(QWidget):
    """
    Temporary VTKWidget placeholder.
    This widget is intended to display 3D visualizations using VTK in the future.
    """

    def __init__(self, parent=None):
        """
        Initialize the VTKWidget.

        :param parent: Parent widget.
        """
        super().__init__(parent)
        self.init_ui()
        logging.info("VTKWidget initialized (placeholder).")

    def init_ui(self):
        """
        Initialize the UI components and layout.
        """
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Placeholder label indicating future implementation
        placeholder_label = QLabel("VTK Widget - To Be Implemented")
        placeholder_label.setStyleSheet("font-size: 16px; color: gray;")
        placeholder_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(placeholder_label)
