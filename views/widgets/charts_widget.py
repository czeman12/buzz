# views/widgets/charts_widget.py

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSizePolicy
from PyQt5.QtChart import QChartView, QPieSeries, QChart
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
import logging


class ChartsWidget(QWidget):
    """
    Widget containing two pie charts to visualize different aspects of issue data.
    """

    def __init__(self, parent=None):
        """
        Initialize the PieChartsWidget.

        :param parent: Parent widget.
        """
        super().__init__(parent)
        self.init_ui()
        logging.info("PieChartsWidget initialized.")

    def init_ui(self):
        """
        Initialize the UI components and layout.
        """
        layout = QHBoxLayout()
        self.setLayout(layout)

        # First Pie Chart
        self.pie_chart_view1 = QChartView()
        self.pie_chart_view1.setRenderHint(QPainter.Antialiasing)
        self.chart1 = QChart()
        self.pie_chart_view1.setChart(self.chart1)
        self.pie_chart_view1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.pie_chart_view1)

        # Second Pie Chart
        self.pie_chart_view2 = QChartView()
        self.pie_chart_view2.setRenderHint(QPainter.Antialiasing)
        self.chart2 = QChart()
        self.pie_chart_view2.setChart(self.chart2)
        self.pie_chart_view2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.pie_chart_view2)

    def update_charts(self, data1: list, data2: list):
        """
        Update the pie charts with new data.

        :param data1: List of tuples for the first chart (label, value).
        :param data2: List of tuples for the second chart (label, value).
        """
        # Update first chart
        self.chart1.removeAllSeries()
        series1 = QPieSeries()
        for label, value in data1:
            series1.append(label, value)
        series1.setLabelsVisible(True)
        self.chart1.addSeries(series1)
        self.chart1.setTitle("Issue Status Distribution")
        self.chart1.legend().setVisible(True)
        self.chart1.legend().setAlignment(Qt.AlignBottom)
        logging.info("First pie chart updated.")

        # Update second chart
        self.chart2.removeAllSeries()
        series2 = QPieSeries()
        for label, value in data2:
            series2.append(label, value)
        series2.setLabelsVisible(True)
        self.chart2.addSeries(series2)
        self.chart2.setTitle("Root Cause Analysis")
        self.chart2.legend().setVisible(True)
        self.chart2.legend().setAlignment(Qt.AlignBottom)
        logging.info("Second pie chart updated.")
