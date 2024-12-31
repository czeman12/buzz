# widgets/environment_toggle.py

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QPainter, QColor, QBrush, QFont


class EnvironmentToggle(QWidget):
    environment_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super(EnvironmentToggle, self).__init__(parent)
        self.setFixedSize(100, 30)
        self.setCursor(Qt.PointingHandCursor)
        self._checked = False  # False for PROD (left), True for R&D (right)
        self._color_on = QColor(0, 200, 0)  # Green for R&D
        self._color_off = QColor(0, 122, 204)  # Blue for PROD
        self._label_on = "R&D"
        self._label_off = "PROD"
        self._label_font = QFont("Arial", 10, QFont.Bold)

    def sizeHint(self):
        return QSize(100, 30)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._checked = not self._checked
            self.update()
            environment = "development" if self._checked else "production"
            self.environment_changed.emit(environment)
        super(EnvironmentToggle, self).mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Determine colors and labels based on the state
        if self._checked:
            bg_color = self._color_on
            label = self._label_on
            circle_x = self.width() - self.height()
        else:
            bg_color = self._color_off
            label = self._label_off
            circle_x = 0

        # Draw background
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 15, 15)

        # Draw the circle
        painter.setBrush(QBrush(Qt.white))
        circle_rect = self.height() - 4
        painter.drawEllipse(circle_x + 2, 2, circle_rect, circle_rect)

        # Draw the label
        painter.setFont(self._label_font)
        painter.setPen(Qt.white)

        # Calculate label position with integer coordinates
        label_width = painter.fontMetrics().width(label)
        label_x = int((self.width() - label_width) / 2)
        label_y = int((self.height() + painter.fontMetrics().ascent()) / 2 - 2)

        painter.drawText(label_x, label_y, label)
        painter.end()
