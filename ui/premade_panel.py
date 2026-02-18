import json
import os

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget,
    QPushButton, QMessageBox, QInputDialog
)

PREMADE_FILE = "premade.json"


class PremadePanel(QWidget):
    """Panel that lists premade rolls and loads them into DiceRoller"""

    def __init__(self, dice_roller):
        super().__init__()

        self.dice_roller = dice_roller

        layout = QVBoxLayout()

        # Tlačítko pro uložení premade přímo zde
        self.save_premade_button = QPushButton("Save as Premade")
        self.save_premade_button.clicked.connect(self.save_as_premade)

        self.premade_list = QListWidget()
        self.delete_button = QPushButton("Delete Selected")

        layout.addWidget(self.save_premade_button)
        layout.addWidget(self.premade_list)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)

        # Dvojklik = použít premade
        self.premade_list.itemDoubleClicked.connect(self.use_premade)
        self.delete_button.clicked.connect(self.delete_premade)

        self.load_premades()

    # --------------------------
    # Load & use premade
    # --------------------------
    def load_premades(self):
        """Načte premade a zobrazí v seznamu s formulí"""
        self.premade_list.clear()

        if not os.path.exists(PREMADE_FILE):
            return

        with open(PREMADE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        for item in data:
            # Spočítáme formuli: 8d6+0
            formula_parts = []
            for row in item["rows"]:
                mod_text = f"+{row['mod']}" if row['mod'] >= 0 else f"{row['mod']}"
                formula_parts.append(f"{row['count']}d{row['sides']}{mod_text}")
            formula_str = " + ".join(formula_parts)
            self.premade_list.addItem(f"{item['name']} ({formula_str})")

    def use_premade(self):
        """Použije vybraný premade hod v DiceRollerPanel a uloží do historie"""
        row = self.premade_list.currentRow()
        if row < 0:
            return

        with open(PREMADE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Naplnění dice řádků do DiceRoller
        self.dice_roller.load_configuration(data[row]["rows"])

        # Roll s názvem hodu pro historii
        self.dice_roller.roll(name=data[row]["name"])

    def delete_premade(self):
        row = self.premade_list.currentRow()

        if row < 0:
            QMessageBox.information(self, "Info", "Select premade to delete.")
            return

        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this premade?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        with open(PREMADE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        data.pop(row)

        with open(PREMADE_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        self.load_premades()

    # --------------------------
    # Save premade přímo z PremadePanel
    # --------------------------
    def save_as_premade(self):
        config = self.dice_roller.get_current_configuration()

        if not config:
            QMessageBox.warning(self, "Error", "No dice to save.")
            return

        name, ok = QInputDialog.getText(
            self,
            "Save Premade",
            "Enter premade name:"
        )

        if not ok or not name.strip():
            return

        data = self.load_json()
        data.append({
            "name": name.strip(),
            "rows": config
        })

        self.save_json(data)

        self.load_premades()  # obnoví seznam
        QMessageBox.information(self, "Saved", "Premade saved.")

    # --------------------------
    # JSON helpers
    # --------------------------
    def load_json(self):
        if not os.path.exists(PREMADE_FILE):
            return []
        with open(PREMADE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    def save_json(self, data):
        with open(PREMADE_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)