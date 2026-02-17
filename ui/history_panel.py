import json
import os

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QListWidget,
    QMessageBox
)


class HistoryPanel(QWidget):
    """Panel to show roll history, save it, and load it automatically."""

    FILE_NAME = "history.json"

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

        # Load history from file on startup
        self.load_history()

    def add_roll(self, formula_str: str, total: int, rolls_with_modifier: str):
        """Add a roll to history and save."""
        entry = f"{formula_str} = {total} ({rolls_with_modifier})"
        self.history.insertItem(0, entry)
        self.save_history()

    def clear_history(self):
        self.history.clear()
        self.save_history()

    def remove_selected(self):
        selected_items = self.history.selectedItems()

        if not selected_items:
            QMessageBox.information(self, "Remove Selected", "No throw selected!")
            return

        for item in selected_items:
            self.history.takeItem(self.history.row(item))

        self.save_history()

    def save_history(self):
        """Save history to JSON file."""
        history_list = []

        for i in range(self.history.count()):
            history_list.append(self.history.item(i).text())

        try:
            with open(self.FILE_NAME, "w", encoding="utf-8") as file:
                json.dump(history_list, file, indent=4)
        except Exception as e:
            print("Failed to save history:", e)

    def load_history(self):
        """Load history from JSON file."""
        if not os.path.exists(self.FILE_NAME):
            return

        try:
            with open(self.FILE_NAME, "r", encoding="utf-8") as file:
                history_list = json.load(file)

            for entry in history_list:
                self.history.addItem(entry)

        except Exception as e:
            print("Failed to load history:", e)