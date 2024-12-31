# views/widgets/spinner_widget.py

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie
import logging


class SpinnerWidget(QWidget):
    """
    A reusable spinner widget that can be displayed within any parent widget.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        # Remove window flags to embed within layout
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # Removed window flags to allow embedding
        # self.setWindowFlags(
        #     Qt.FramelessWindowHint | Qt.Dialog | Qt.WindowStaysOnTopHint
        # )
        self.setFixedSize(90, 20)  # Increased size (3x the original)
        self.init_ui()
        logging.info("SpinnerWidget initialized.")

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        # Remove any spacing and margins in the spinner's layout
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignCenter)

        # Create a QLabel to hold the spinner GIF
        self.spinner_label = QLabel(self)
        self.spinner_label.setScaledContents(True)  # Enable scaling
        self.spinner_movie = QMovie(
            "assets/logos/loader.gif"
        )  # Ensure this path is correct and high-res
        if not self.spinner_movie.isValid():
            logging.error(
                "Failed to load spinner GIF. Check the path 'assets/logos/loader.gif'."
            )
        self.spinner_label.setMovie(self.spinner_movie)
        layout.addWidget(self.spinner_label)

        # Start the spinner animation
        self.spinner_movie.start()

    def show_spinner(self):
        """
        Show the spinner.
        """
        self.setVisible(True)
        self.spinner_movie.start()
        logging.debug("SpinnerWidget shown.")

    def hide_spinner(self):
        """
        Hide the spinner.
        """
        self.setVisible(False)
        self.spinner_movie.stop()
        logging.debug("SpinnerWidget hidden.")
