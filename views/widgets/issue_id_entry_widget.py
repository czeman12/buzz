# views/widgets/issue_id_entry_widget.py

from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QLabel,
    QMessageBox,
    QProgressBar,
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIntValidator, QPalette, QColor, QFont
import logging

from utils.scalable_widget import ScalableWidget  # Import ScalableWidget


class IDEntryWidget(ScalableWidget):
    """
    IDEntryWidget Widget
    Allows users to enter and submit an Issue ID with inline validation.
    Inherits from ScalableWidget to support dynamic font scaling.
    """

    # Define a custom signal that emits the valid issue ID
    issue_id_submitted = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        logging.info("IDEntryWidget initialized.")

    def init_ui(self):
        """
        Initialize the UI components and layout.
        """
        # Create the main layout
        layout = QHBoxLayout()
        self.setLayout(layout)

        # Label for Issue ID
        # self.label = QLabel("Issue ID:")
        # self.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        # self.label.setObjectName("IssueIDLabel")

        # Apply scaled font styling
        label_font = self.get_scaled_font(
            point_size=14, family="Arial", weight=QFont.Bold
        )
        #  self.label.setFont(label_font)

        # layout.addWidget(self.label)

        # Line Edit for Issue ID input
        self.issue_id_input = QLineEdit()
        self.issue_id_input.setPlaceholderText("Issue ID")
        self.issue_id_input.setMaxLength(5)  # Set max length to 5
        self.issue_id_input.setFixedWidth(
            int(150 * self.scaling_factor)
        )  # Adjusted width based on scaling

        # Set object name for styling
        self.issue_id_input.setObjectName("IssueIDInput")

        # Set up the validator for integers between 10 and 99999 (2-5 digits)
        validator = QIntValidator(10, 99999, self)
        self.issue_id_input.setValidator(validator)

        # Apply scaled font styling
        input_font = self.get_scaled_font(
            point_size=14, family="Arial", weight=QFont.Normal
        )
        self.issue_id_input.setFont(input_font)

        # Connect returnPressed signal for submission via Enter key
        self.issue_id_input.returnPressed.connect(self.on_submit)

        # Connect textChanged signal for real-time validation and label visibility
        self.issue_id_input.textChanged.connect(self.handle_text_changed)
        layout.addWidget(self.issue_id_input)

        # Error Message Label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        self.error_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.error_label.setObjectName("ErrorLabel")

        # Apply scaled font styling
        error_font = self.get_scaled_font(
            point_size=12, family="Arial", weight=QFont.Normal
        )
        self.error_label.setFont(error_font)

        layout.addWidget(self.error_label)

        # Spacer to push the spinner to the right
        layout.addStretch()

        # Spinner Loader (QProgressBar in busy indicator mode)
        self.spinner = QProgressBar()
        self.spinner.setRange(0, 0)  # Makes it a busy indicator
        self.spinner.setFixedSize(
            int(20 * self.scaling_factor), int(20 * self.scaling_factor)
        )  # Adjust size based on scaling
        self.spinner.setVisible(False)
        layout.addWidget(self.spinner)

        # Set focus to the Issue ID input field on initialization
        self.issue_id_input.setFocus()

    def on_scaling_updated(self):
        """
        Override the method to update fonts and widget sizes when scaling changes.
        """
        logging.info("Scaling updated in IDEntryWidget.")
        # Update label font
        label_font = self.get_scaled_font(
            point_size=14, family="Arial", weight=QFont.Bold
        )
        # self.label.setFont(label_font)

        # Update input font
        input_font = self.get_scaled_font(
            point_size=14, family="Arial", weight=QFont.Normal
        )
        self.issue_id_input.setFont(input_font)

        # Update error label font
        error_font = self.get_scaled_font(
            point_size=12, family="Arial", weight=QFont.Normal
        )
        self.error_label.setFont(error_font)

        # Update widget sizes based on scaling factor
        self.issue_id_input.setFixedWidth(int(150 * self.scaling_factor))
        self.spinner.setFixedSize(
            int(20 * self.scaling_factor), int(20 * self.scaling_factor)
        )

    def handle_text_changed(self, text):
        """
        Handle text changes to manage label visibility and input validation.
        """
        # if text:
        #     self.label.hide()
        # else:
        #     self.label.show()

        # Validate input
        self.validate_input(text)

    def validate_input(self, text):
        """
        Validates the input in real-time and provides user feedback.
        """
        if 2 <= len(text) <= 5 and text.isdigit():
            # Valid input
            self.set_valid_state()
        else:
            # Invalid input
            self.set_invalid_state()

    def set_valid_state(self):
        """
        Sets the visual state of the input to valid.
        """
        palette = self.issue_id_input.palette()
        palette.setColor(QPalette.Base, QColor("#d4ffd4"))  # Light green background
        self.issue_id_input.setPalette(palette)
        self.issue_id_input.setStyleSheet("border: 1px solid green;")
        self.error_label.setText("")

    def set_invalid_state(self):
        """
        Sets the visual state of the input to invalid.
        """
        palette = self.issue_id_input.palette()
        palette.setColor(QPalette.Base, QColor("#ffd4d4"))  # Light red background
        self.issue_id_input.setPalette(palette)
        self.issue_id_input.setStyleSheet("border: 1px solid red;")
        text = self.issue_id_input.text()
        if len(text) > 0:
            if not text.isdigit():
                self.error_label.setText("Issue ID must be numeric.")
            elif len(text) < 2:
                self.error_label.setText("Issue ID must be at least 2 digits.")
            elif len(text) > 5:
                self.error_label.setText("Issue ID must be less than 6 digits.")
        else:
            self.error_label.setText("")

    def on_submit(self):
        """
        Handles the submit event triggered by pressing the Enter key.
        Emits the issue_id_submitted signal if input is valid.
        """
        issue_id = self.issue_id_input.text()
        if self.is_input_valid(issue_id):
            logging.info(f"Issue ID submitted: {issue_id}")
            self.issue_id_submitted.emit(issue_id)
            # Optionally, clear the input after submission
            # self.issue_id_input.clear()
        else:
            # This should not happen as validation should disable invalid input
            QMessageBox.warning(
                self, "Invalid Input", "Please enter a valid 2-5 digit Issue ID."
            )
            logging.warning(f"Attempted to submit invalid Issue ID: {issue_id}")

    def is_input_valid(self, issue_id: str) -> bool:
        """
        Checks if the input Issue ID is valid.

        :param issue_id: The Issue ID string to validate.
        :return: True if valid, False otherwise.
        """
        return 2 <= len(issue_id) <= 5 and issue_id.isdigit()

    def show_spinner(self, show: bool):
        """
        Show or hide the spinner loader.

        :param show: True to show the spinner, False to hide.
        """
        self.spinner.setVisible(show)
