class IssueIDEntryWidget(QWidget):
    """
    Widget for entering an Issue ID and submitting it.
    """

    def __init__(self, submit_callback, parent=None):
        super().__init__(parent)
        self.submit_callback = submit_callback
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.issue_id_input = QLineEdit()
        self.issue_id_input.setPlaceholderText("Enter Issue ID")

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.on_submit)

        layout.addWidget(self.issue_id_input)
        layout.addWidget(self.submit_button)

    def on_submit(self):
        issue_id = self.issue_id_input.text().strip()
        if issue_id:
            self.submit_callback(issue_id)
        else:
            # Handle empty input (optional)
            pass
