# views/widgets/pie_charts_widget.py

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import logging


class PieChartsWidget(QWidget):
    """
    Widget to display pie charts with legends.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        logging.info("PieChartsWidget initialized.")

    def init_ui(self):
        """
        Initialize the UI components and layout.
        """
        layout = QHBoxLayout()
        self.setLayout(layout)

        # Disposition Pie Chart
        self.disposition_canvas = FigureCanvas(plt.Figure(figsize=(4, 4)))
        layout.addWidget(self.disposition_canvas)

        # Defect Code Pie Chart
        self.defect_code_canvas = FigureCanvas(plt.Figure(figsize=(4, 4)))
        layout.addWidget(self.defect_code_canvas)

        # Legends
        self.legend_layout = QVBoxLayout()
        layout.addLayout(self.legend_layout)

        self.disposition_legend = QListWidget()
        self.defect_code_legend = QListWidget()

        self.legend_layout.addWidget(QLabel("Disposition Counts"))
        self.legend_layout.addWidget(self.disposition_legend)

        self.legend_layout.addWidget(QLabel("Defect Code Counts"))
        self.legend_layout.addWidget(self.defect_code_legend)

    def update_charts(self, disposition_data, defect_code_data):
        """
        Update the pie charts with new data and update legends.

        :param disposition_data: List of tuples (label, value).
        :param defect_code_data: List of tuples (label, value).
        """
        # Update Disposition Pie Chart
        disposition_fig = self.disposition_canvas.figure
        disposition_ax = disposition_fig.subplots()
        disposition_ax.clear()

        labels, sizes = zip(*disposition_data) if disposition_data else ([], [])
        colors = plt.cm.Paired(range(len(labels)))

        disposition_ax.pie(
            sizes, labels=None, colors=colors, autopct="%1.1f%%", startangle=140
        )
        disposition_ax.axis(
            "equal"
        )  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Update Defect Code Pie Chart
        defect_code_fig = self.defect_code_canvas.figure
        defect_code_ax = defect_code_fig.subplots()
        defect_code_ax.clear()

        labels, sizes = zip(*defect_code_data) if defect_code_data else ([], [])
        colors = plt.cm.Paired(range(len(labels)))

        defect_code_ax.pie(
            sizes, labels=None, colors=colors, autopct="%1.1f%%", startangle=140
        )
        defect_code_ax.axis("equal")

        # Draw the canvases
        self.disposition_canvas.draw()
        self.defect_code_canvas.draw()

        # Update Legends
        self.update_legend(self.disposition_legend, disposition_data, plt.cm.Paired)
        self.update_legend(self.defect_code_legend, defect_code_data, plt.cm.Paired)

        logging.info("Pie charts and legends updated successfully.")

    def update_legend(self, legend_widget: QListWidget, data, color_map):
        """
        Update the legend widget with new data.

        :param legend_widget: The QListWidget to update.
        :param data: List of tuples (label, value).
        :param color_map: The color map used for the pie chart.
        """
        legend_widget.clear()
        for idx, (label, value) in enumerate(data):
            item = QListWidgetItem(f"{label}: {value}")
            color = QColor.fromRgbF(*color_map(idx)[:3])
            item.setBackground(color)
            legend_widget.addItem(item)
