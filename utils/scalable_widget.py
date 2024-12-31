# utils/scalable_widget.py

import logging
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal

from .scaling_helper import ScalingHelper  # Import ScalingHelper


class ScalableWidget(QWidget):
    """
    Base widget class that provides scalable font functionality based on screen DPI.
    Other widgets should inherit from this class to automatically adjust their fonts.
    """

    # Signal to indicate that scaling has been updated
    scaling_updated = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scaling_factor = ScalingHelper.get_scaling_factor()
        self.scaling_updated.connect(self.on_scaling_updated)
        self.window_handle = self.window().windowHandle()
        if self.window_handle:
            self.window_handle.screenChanged.connect(self.on_screen_changed)
        else:
            logging.warning("No window handle found for ScalableWidget.")

    def get_scaled_font(
        self, point_size: int, family: str = "Arial", weight: int = QFont.Normal
    ) -> QFont:
        """
        Retrieve a QFont object scaled according to the scaling factor.

        :param point_size: Base font size in points.
        :param family: Font family name.
        :param weight: Font weight.
        :return: Scaled QFont object.
        """
        return ScalingHelper.get_scaled_font(
            point_size, family, weight, self.scaling_factor
        )

    def on_screen_changed(self):
        """
        Slot to handle screen change events. Recalculate the scaling factor and emit scaling_updated signal.
        """
        logging.info("Screen change detected. Recalculating scaling factor.")
        self.scaling_factor = ScalingHelper.get_scaling_factor()
        self.scaling_updated.emit()

    def on_scaling_updated(self):
        """
        Slot to handle scaling updates. Override this method in subclasses to adjust fonts or layouts.
        """
        logging.info(
            "Scaling updated. Override on_scaling_updated in subclasses to apply changes."
        )
        pass
