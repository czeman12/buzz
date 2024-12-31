# utils/scaling_helper.py

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont, QFontMetrics
import logging


class ScalingHelper:
    """
    Helper class to provide scaling-related utilities.
    """

    @staticmethod
    def get_scaling_factor() -> float:
        """
        Calculate the scaling factor based on the screen's DPI.

        :return: Scaling factor (default is 1.0).
        """
        screen = QApplication.primaryScreen()
        if not screen:
            logging.warning(
                "No primary screen found. Using default scaling factor 1.0."
            )
            return 1.0

        dpi = screen.logicalDotsPerInch()
        scaling_factor = dpi / 96.0  # 96 DPI is the standard reference
        logging.debug(f"Calculated scaling factor: {scaling_factor} (DPI: {dpi})")
        return scaling_factor

    @staticmethod
    def get_scaled_font(
        point_size: int,
        family: str = "Arial",
        weight: int = QFont.Normal,
        scaling_factor: float = 1.0,
    ) -> QFont:
        """
        Retrieve a QFont object scaled according to the scaling factor.

        :param point_size: Base font size in points.
        :param family: Font family name.
        :param weight: Font weight.
        :param scaling_factor: Scaling factor.
        :return: Scaled QFont object.
        """
        scaled_size = max(1, int(point_size * scaling_factor))
        font = QFont(family, scaled_size, weight)
        logging.debug(f"Scaled font: {family}, {scaled_size}pt, weight={weight}")
        return font
