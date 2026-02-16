from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QListWidget,
    QMessageBox
)

class HistoryPanel(QWidget):
    """Panel to show roll history and manage it."""

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.history = QListWidget()

        # Buttons
        self.clear_history_button = QPushButton("Clear History")
        self.clear_history_button.clicked.connect(self.clear_history)

        self.remove_selected_button = QPushButton("Remove Selected")
        self.remove_selected_button.clicked.connect(self.remove_selected)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.clear_history_button)
        buttons_layout.addWidget(self.remove_selected_button)

        self.layout.addLayout(buttons_layout)
        self.layout.addWidget(self.history)
        self.setLayout(self.layout)

    def add_roll(self, formula_str: str, total: int, rolls_with_modifier: str):
        """Add a roll to the history list."""
        self.history.insertItem(0, f"{formula_str} = {total} ({rolls_with_modifier})")

    def clear_history(self):
        self.history.clear()

    def remove_selected(self):
        selected_items = self.history.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "Remove Selected", "No throw selected!")
            return
        for item in selected_items:
            self.history.takeItem(self.history.row(item))