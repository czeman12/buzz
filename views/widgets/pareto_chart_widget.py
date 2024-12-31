# views/widgets/pareto_chart_widget.py

import matplotlib.pyplot as plt
import pandas as pd
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import logging
from utils.matplotlib_style import apply_dark_theme


class ParetoChartWidget(QWidget):
    """
    Widget to display Pareto charts within the application.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        logging.info("ParetoChartWidget initialized.")

    def init_ui(self):
        """
        Initialize the UI components and layout.
        """
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create a Matplotlib figure and canvas
        self.figure = Figure(figsize=(5, 4), tight_layout=True, facecolor="#2b2b2b")
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Create an initial empty plot with dark theme compliance
        self.ax = self.figure.add_subplot(111)
        self.ax.set_facecolor("#2b2b2b")  # Match figure background
        # self.ax.tick_params(colors="white")  # Tick labels
        self.ax.xaxis.label.set_color("white")  # X-axis label
        self.ax.yaxis.label.set_color("white")  # Y-axis label
        self.ax.title.set_color("white")  # Title

        # Disable axis ticks and labels for a cleaner startup display
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_xlabel("")
        self.ax.set_ylabel("")
        self.ax.set_title("")

        # Optionally, remove the spine lines for an even cleaner look
        for spine in self.ax.spines.values():
            spine.set_visible(False)

        # Set grid lines to a lighter color for visibility
        # self.ax.grid(True, color="gray", linestyle="--", linewidth=0.5)

        # Add placeholder text
        self.ax.text(
            0.5,
            0.5,
            "No Data Loaded",
            horizontalalignment="center",
            verticalalignment="center",
            transform=self.ax.transAxes,
            color="white",
            fontsize=12,
        )

        self.canvas.draw()

    def plot_pareto(self, counts, title="Pareto Chart"):
        """
        Generate and display the Pareto chart based on the provided counts.

        :param counts: Dictionary or list of tuples containing category counts.
        :param title: Title of the Pareto chart.
        """
        try:
            # Determine if 'counts' is a dict or list of tuples
            if isinstance(counts, dict):
                counts_dict = counts
            elif isinstance(counts, list):
                counts_dict = dict(counts)
            else:
                raise TypeError("counts must be a dict or a list of tuples")

            # Convert dictionary to DataFrame
            df = pd.DataFrame(list(counts_dict.items()), columns=["Category", "Count"])
            df = df.sort_values(by="Count", ascending=False).reset_index(drop=True)

            # Calculate cumulative percentage
            df["Cumulative Percentage"] = df["Count"].cumsum() / df["Count"].sum() * 100

            # Find the threshold index where cumulative percentage first exceeds 80%
            threshold_index = df[df["Cumulative Percentage"] <= 80].index.max()

            if pd.isna(threshold_index):
                threshold_index = len(df) - 1
            else:
                threshold_index = df[df["Cumulative Percentage"] <= 80].index[-1]

            logging.debug(f"Threshold Index: {threshold_index}")

            # Create a list of colors based on the threshold
            colors = ["C0" if i <= threshold_index else "C7" for i in range(len(df))]

            # Clear previous plot
            self.figure.clear()

            # Create a subplot
            ax1 = self.figure.add_subplot(111)

            # Plot bars
            bars = ax1.bar(df["Category"], df["Count"], color=colors)
            ax1.set_ylabel("Count", color="C0")
            # ax1.set_xlabel("Category", color="#FFFFFF")
            # ax1.tick_params(labelcolor="C0")
            ax1.tick_params(labelcolor="#FFFFFF")
            ax1.set_title(title, color="#FFFFFF")

            # Rotate x-tick labels to avoid overlap
            plt.setp(ax1.get_xticklabels(), rotation=45, ha="right")

            # Plot cumulative percentage on a secondary y-axis
            ax2 = ax1.twinx()
            ax2.plot(
                df["Category"],
                df["Cumulative Percentage"],
                color="C1",
                marker="D",
                ms=7,
            )
            ax2.set_ylabel("Cumulative Percentage", color="C1")
            ax2.tick_params(axis="y", labelcolor="#FFFFFF")

            # Set background colors
            ax1.set_facecolor("#2e2e2e")
            ax2.set_facecolor("#2e2e2e")
            self.figure.patch.set_facecolor("#2e2e2e")

            # Apply custom dark style
            # apply_dark_theme()

            # Draw the canvas
            self.canvas.draw()
            logging.info("Pareto chart plotted successfully.")
        except Exception as e:
            logging.error(f"Error plotting Pareto chart: {e}")
