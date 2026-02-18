import json
import os

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QLabel, QPushButton, QMessageBox
)
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import Signal, QEvent

from logic.dice import roll_dice, calculate_total

PREMADE_FILE = "premade.json"


class DiceRow(QWidget):
    """Single dice row: count, sides, modifier, delete button"""

    def __init__(self, remove_callback):
        super().__init__()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.count_input = QLineEdit("1")
        self.count_input.setValidator(QIntValidator(1, 100))
        self.count_input.setFixedWidth(60)

        self.sides_input = QLineEdit("6")
        self.sides_input.setValidator(QIntValidator(1, 1000))
        self.sides_input.setFixedWidth(60)

        self.mod_input = QLineEdit("0")
        self.mod_input.setValidator(QIntValidator(-1000, 1000))
        self.mod_input.setFixedWidth(60)

        delete_button = QPushButton("Delete")
        delete_button.setFixedWidth(70)
        delete_button.clicked.connect(lambda: remove_callback(self))

        layout.addWidget(QLabel("Count:"))
        layout.addWidget(self.count_input)
        layout.addWidget(QLabel("Sides:"))
        layout.addWidget(self.sides_input)
        layout.addWidget(QLabel("MOD:"))
        layout.addWidget(self.mod_input)
        layout.addWidget(delete_button)
        layout.addStretch()

        self.setLayout(layout)


class DiceRollerPanel(QWidget):
    """Panel to roll multiple dice rows (bez tlačítka Save as Premade)"""

    premade_saved = Signal()  # signal pro budoucí kompatibilitu

    def __init__(self, history_callback):
        super().__init__()

        self.history_callback = history_callback
        self.dice_rows = []

        layout = QVBoxLayout()

        self.roll_button = QPushButton("Roll Dice")
        self.roll_button.clicked.connect(self.roll)

        self.add_row_button = QPushButton("Add Another Dice")
        self.add_row_button.clicked.connect(self.add_dice_row)

        self.rows_layout = QVBoxLayout()
        self.add_dice_row()

        self.rolls_label = QLabel("Rolls: -")
        self.modifiers_label = QLabel("Modifiers sum: -")
        self.total_label = QLabel("Total: -")
        self.total_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        layout.addWidget(self.roll_button)
        layout.addLayout(self.rows_layout)
        layout.addWidget(self.add_row_button)
        layout.addWidget(self.rolls_label)
        layout.addWidget(self.modifiers_label)
        layout.addWidget(self.total_label)
        layout.addStretch()

        self.setLayout(layout)

    # --------------------------
    # Dice row management
    # --------------------------
    def add_dice_row(self):
        row = DiceRow(remove_callback=self.remove_dice_row)
        self.dice_rows.append(row)
        self.rows_layout.addWidget(row)

    def remove_dice_row(self, row):
        if row in self.dice_rows:
            self.dice_rows.remove(row)
            row.deleteLater()

    # --------------------------
    # Rolling logic
    # --------------------------
    def roll(self):
        total_rolls = []
        formula_parts = []
        total_modifiers = 0

        for row in self.dice_rows:
            try:
                count = int(row.count_input.text())
                sides = int(row.sides_input.text())
                mod = int(row.mod_input.text())
            except ValueError:
                self.rolls_label.setText("Invalid input!")
                return

            rolls = roll_dice(count, sides)
            total_rolls.extend(rolls)
            total_modifiers += mod

            mod_text = f"+{mod}" if mod >= 0 else f"{mod}"
            formula_parts.append(f"{count}d{sides}{mod_text}")

        grand_total = calculate_total(total_rolls) + total_modifiers
        rolls_text = ", ".join(map(str, total_rolls))

        self.rolls_label.setText(f"Rolls: {rolls_text}")
        self.modifiers_label.setText(f"Modifiers sum: {total_modifiers}")
        self.total_label.setText(f"Total: {grand_total}")

        formula_str = " + ".join(formula_parts)

        self.history_callback(
            formula_str,
            grand_total,
            f"{rolls_text} + {total_modifiers}"
        )

    # --------------------------
    # Get / Load configuration
    # --------------------------
    def get_current_configuration(self):
        return [
            {
                "count": int(row.count_input.text()),
                "sides": int(row.sides_input.text()),
                "mod": int(row.mod_input.text())
            }
            for row in self.dice_rows
        ]

    def load_configuration(self, config):
        for row in self.dice_rows[:]:
            self.remove_dice_row(row)

        for row_data in config:
            self.add_dice_row()
            row = self.dice_rows[-1]
            row.count_input.setText(str(row_data["count"]))
            row.sides_input.setText(str(row_data["sides"]))
            row.mod_input.setText(str(row_data["mod"]))