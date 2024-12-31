# views/widgets/issue_details_table.py

from PyQt5.QtWidgets import (
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QComboBox,
    QSizePolicy,
)
from PyQt5.QtCore import Qt
import logging


class IssueDetailsTable(QWidget):
    """
    Widget to display detailed information about issues in a table format with pagination.
    """

    def __init__(self, parent=None):
        """
        Initialize the IssueDetailsTable.

        :param parent: Parent widget.
        """
        super().__init__(parent)
        self.data = []
        self.headers = []
        self.current_page = 1
        self.total_pages = 1
        self.rows_per_page = 10  # Default rows per page
        self.rows_per_page_options = [10, 25, 50, 100]
        self.init_ui()
        logging.info("IssueDetailsTable initialized.")

    def init_ui(self):
        """
        Initialize the UI components and layout.
        """
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Table Widget
        self.table = QTableWidget()
        self.table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # Read-only
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)

        # Apply styles compatible with dark theme
        self.table.setStyleSheet(
            """
            QTableWidget {
                alternate-background-color: #3a3a3a;
                background-color: #2c2c2c;
                color: #ffffff;
                border: 1px solid #444444;
            }
            QHeaderView::section {
                background-color: #1c1c1c;
                color: #ffffff;
                padding: 4px;
                border: 1px solid #444444;
            }
            QTableWidget::item:selected {
                background-color: #555555;
            }
        """
        )

        # Pagination Controls
        self.pagination_layout = QHBoxLayout()
        self.pagination_layout.setAlignment(Qt.AlignCenter)

        # Rows per page ComboBox
        self.rows_per_page_label = QLabel("Rows per page:")
        self.rows_per_page_label.setStyleSheet("color: #ffffff;")
        self.rows_per_page_combo = QComboBox()
        self.rows_per_page_combo.addItems([str(n) for n in self.rows_per_page_options])
        self.rows_per_page_combo.setCurrentText(str(self.rows_per_page))
        self.rows_per_page_combo.currentTextChanged.connect(
            self.on_rows_per_page_changed
        )
        self.rows_per_page_combo.setStyleSheet(
            """
            QComboBox {
                background-color: #2c2c2c;
                color: #ffffff;
                border: 1px solid #444444;
            }
            QComboBox QAbstractItemView {
                background-color: #2c2c2c;
                color: #ffffff;
                selection-background-color: #555555;
            }
        """
        )

        # Navigation Buttons
        self.first_button = QPushButton("<< First")
        self.prev_button = QPushButton("< Previous")
        self.next_button = QPushButton("Next >")
        self.last_button = QPushButton("Last >>")

        for button in [
            self.first_button,
            self.prev_button,
            self.next_button,
            self.last_button,
        ]:
            button.clicked.connect(self.on_navigation_button_clicked)
            button.setStyleSheet(
                """
                QPushButton {
                    background-color: #3a3a3a;
                    color: #ffffff;
                    border: 1px solid #444444;
                    padding: 5px 10px;
                }
                QPushButton::hover {
                    background-color: #555555;
                }
                """
            )

        # Page Info Label
        self.page_info_label = QLabel()
        self.page_info_label.setStyleSheet("color: #ffffff;")

        # Add widgets to pagination layout
        self.pagination_layout.addWidget(self.rows_per_page_label)
        self.pagination_layout.addWidget(self.rows_per_page_combo)
        self.pagination_layout.addStretch()
        self.pagination_layout.addWidget(self.first_button)
        self.pagination_layout.addWidget(self.prev_button)
        self.pagination_layout.addWidget(self.page_info_label)
        self.pagination_layout.addWidget(self.next_button)
        self.pagination_layout.addWidget(self.last_button)
        self.pagination_layout.addStretch()

        # Add widgets to main layout
        layout.addWidget(self.table)
        layout.addLayout(self.pagination_layout)

    def update_table(self, headers: list, data: list):
        """
        Update the table with new data.

        :param headers: List of column headers.
        :param data: List of rows, each row is a list of cell values.
        """
        self.headers = headers
        self.data = data
        self.current_page = 1
        self.calculate_total_pages()
        self.update_table_view()
        logging.info("Issue details table updated successfully.")

    def calculate_total_pages(self):
        """
        Calculate the total number of pages based on data length and rows per page.
        """
        total_rows = len(self.data)
        self.total_pages = (total_rows + self.rows_per_page - 1) // self.rows_per_page

    def update_table_view(self):
        """
        Update the table view based on the current page and rows per page.
        """
        self.table.clear()
        self.table.setRowCount(0)

        # Set headers
        self.table.setColumnCount(len(self.headers))
        self.table.setHorizontalHeaderLabels(self.headers)

        # Calculate data slice
        start_idx = (self.current_page - 1) * self.rows_per_page
        end_idx = start_idx + self.rows_per_page
        page_data = self.data[start_idx:end_idx]

        # Update page info label
        self.page_info_label.setText(f"Page {self.current_page} of {self.total_pages}")

        # Populate table
        self.table.setRowCount(len(page_data))
        for row_idx, row_data in enumerate(page_data):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.table.setItem(row_idx, col_idx, item)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def on_rows_per_page_changed(self, value):
        """
        Handle changes to the rows per page selection.
        """
        self.rows_per_page = int(value)
        self.current_page = 1  # Reset to first page
        self.calculate_total_pages()
        self.update_table_view()

    def on_navigation_button_clicked(self):
        """
        Handle navigation button clicks.
        """
        sender = self.sender()
        if sender == self.first_button:
            self.current_page = 1
        elif sender == self.prev_button and self.current_page > 1:
            self.current_page -= 1
        elif sender == self.next_button and self.current_page < self.total_pages:
            self.current_page += 1
        elif sender == self.last_button:
            self.current_page = self.total_pages
        self.update_table_view()
