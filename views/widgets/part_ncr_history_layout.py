# ui/report_layout.py

import os
import logging
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QSplitter,
    QWidget,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class ReportLayout:
    def __init__(self, parent_notebook):
        """
        Initialize the report layout with a splitter containing pie charts and table.
        :param parent_notebook: The parent QTabWidget where the report tab is added.
        """
        self.parent_notebook = parent_notebook

        # Create the report tab
        self.report_tab = QWidget()
        self.report_layout = QVBoxLayout()
        self.report_tab.setLayout(self.report_layout)

        # Add the report tab to the notebook
        self.parent_notebook.addTab(self.report_tab, "Report")

        # Initialize QSplitter with vertical orientation
        self.splitter = QSplitter(Qt.Vertical)
        self.report_layout.addWidget(self.splitter)

        # Initialize the pie charts and table placeholders
        self.initialize_pie_charts_widget()
        self.initialize_table_widget()

        # Add the pie charts and table to the splitter
        self.splitter.addWidget(self.pie_charts_widget)
        self.splitter.addWidget(self.table_widget)

        # Set initial sizes and minimum sizes for the pie charts and table
        self.pie_charts_widget.setMinimumSize(900, 600)  # Width: 900, Height: 600
        self.table_widget.setMinimumSize(900, 500)  # Width: 900, Height: 500

        # Adjust the stretch factor for a 5:2 ratio (pie charts vs. table)
        self.splitter.setStretchFactor(0, 5)  # Pie charts section gets 5 parts
        self.splitter.setStretchFactor(1, 2)  # Table section gets 2 parts

    def initialize_pie_charts_widget(self):
        """
        Initialize the pie charts widget as a placeholder with a logo before data is loaded.
        """
        self.pie_charts_widget = QWidget()
        self.pie_charts_widget.setObjectName("PieChartsWidget")
        self.pie_charts_layout = QVBoxLayout()
        self.pie_charts_widget.setLayout(self.pie_charts_layout)

        # Placeholder logo when no charts are displayed
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignCenter)
        logo_path = "assets/logos/Joby_Aviation_Logo (Heart).ico"
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            logo_label.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio))
        else:
            logo_label.setText("Logo not found.")
            logging.warning(f"Logo not found at {logo_path}")
        self.pie_charts_layout.addWidget(logo_label)

    def initialize_table_widget(self):
        """
        Initialize the table widget as a placeholder before data is loaded.
        """
        self.table_widget = QWidget()
        self.table_widget.setObjectName("TableWidget")
        self.table_layout = QVBoxLayout()
        self.table_widget.setLayout(self.table_layout)

        # Set a reduced minimum size for the table (Width: 900, Height: 300)
        self.table_widget.setMinimumSize(900, 300)

        # Placeholder text when no table is displayed
        placeholder_label = QLabel("Table will appear here when data is loaded.")
        placeholder_label.setAlignment(Qt.AlignCenter)
        self.table_layout.addWidget(placeholder_label)

    def show_pie_charts(self, disposition_counts, defect_code_counts):
        """
        Display pie charts for disposition and defect code distributions.
        :param disposition_counts: Dictionary with disposition counts.
        :param defect_code_counts: Dictionary with defect code counts.
        """
        # Clear the current layout
        for i in reversed(range(self.pie_charts_layout.count())):
            widget_to_remove = self.pie_charts_layout.itemAt(i).widget()
            self.pie_charts_layout.removeWidget(widget_to_remove)
            widget_to_remove.deleteLater()

        if not disposition_counts or not defect_code_counts:
            placeholder_label = QLabel("No data available to display pie charts.")
            placeholder_label.setAlignment(Qt.AlignCenter)
            self.pie_charts_layout.addWidget(placeholder_label)
            return

        # Create a Matplotlib figure and axes with dark background
        fig, axes = plt.subplots(
            1, 2, figsize=(20, 10), facecolor="#2e2e2e"
        )  # Two pie charts

        # Pie chart 1: Disposition Distribution
        ax1 = axes[0]
        ax1.set_facecolor("#2e2e2e")
        values1 = list(disposition_counts.values())
        labels1 = list(disposition_counts.keys())
        ax1.pie(
            values1,
            labels=labels1,
            autopct="%1.1f%%",
            startangle=90,
            textprops={"fontsize": 12, "color": "white"},
        )
        ax1.axis("equal")
        ax1.set_title(
            "Disposition Distribution", fontsize=16, fontweight="bold", color="white"
        )

        # Pie chart 2: Defect Code Distribution
        ax2 = axes[1]
        ax2.set_facecolor("#2e2e2e")
        values2 = list(defect_code_counts.values())
        labels2 = list(defect_code_counts.keys())
        ax2.pie(
            values2,
            labels=labels2,
            autopct="%1.1f%%",
            startangle=90,
            textprops={"fontsize": 12, "color": "white"},
        )
        ax2.axis("equal")
        ax2.set_title(
            "Defect Code Distribution", fontsize=16, fontweight="bold", color="white"
        )

        # Adjust layout and create canvas
        plt.tight_layout()
        canvas = FigureCanvas(fig)
        self.pie_charts_layout.addWidget(canvas)

        # Close the figure to release memory
        plt.close(fig)

    def show_table(self, ncr_history):
        """
        Display the NCR history table.
        :param ncr_history: Dictionary with NCR history.
        """
        # Clear the current layout
        for i in reversed(range(self.table_layout.count())):
            widget_to_remove = self.table_layout.itemAt(i).widget()
            self.table_layout.removeWidget(widget_to_remove)
            widget_to_remove.deleteLater()

        if not ncr_history:
            placeholder_label = QLabel("No data available to display the table.")
            placeholder_label.setAlignment(Qt.AlignCenter)
            self.table_layout.addWidget(placeholder_label)
            return

        # Create table widget
        table_widget = QTableWidget()
        table_widget.setColumnCount(4)
        table_widget.setHorizontalHeaderLabels(
            ["Issue ID", "Issue Title", "Defect Code", "Disposition Title"]
        )
        table_widget.setRowCount(len(ncr_history))

        for row, (issue_id, (title, defect_code, disposition)) in enumerate(
            ncr_history.items()
        ):
            table_widget.setItem(row, 0, QTableWidgetItem(str(issue_id)))
            table_widget.setItem(row, 1, QTableWidgetItem(title))
            table_widget.setItem(
                row, 2, QTableWidgetItem(defect_code if defect_code else "N/A")
            )
            table_widget.setItem(row, 3, QTableWidgetItem(disposition))

        # Set the table layout
        table_widget.verticalHeader().setVisible(
            False
        )  # Hide the vertical header (index column)
        table_widget.horizontalHeader().setStretchLastSection(
            True
        )  # Stretch the last column
        table_widget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )  # Stretch all columns equally

        self.table_layout.addWidget(table_widget)
