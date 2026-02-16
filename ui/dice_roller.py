from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton
)
from PySide6.QtGui import QIntValidator
from logic.dice import roll_dice, calculate_total

class DiceRow(QWidget):
    """Single dice row: count, sides, modifier, delete button"""

    def __init__(self, remove_callback):
        super().__init__()
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Count input
        self.count_input = QLineEdit()
        self.count_input.setValidator(QIntValidator(1, 100))
        self.count_input.setText("1")

        # Sides input
        self.sides_input = QLineEdit()
        self.sides_input.setValidator(QIntValidator(1, 1000))
        self.sides_input.setText("6")

        # Modifier input (specific to this row)
        self.mod_input = QLineEdit()
        self.mod_input.setValidator(QIntValidator(-1000, 1000))
        self.mod_input.setText("0")

        # Delete button
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(lambda: remove_callback(self))

        # Layout widgets
        self.layout.addWidget(QLabel("Count:"))
        self.layout.addWidget(self.count_input)
        self.layout.addWidget(QLabel("Sides:"))
        self.layout.addWidget(self.sides_input)
        self.layout.addWidget(QLabel("MOD:"))
        self.layout.addWidget(self.mod_input)
        self.layout.addWidget(self.delete_button)

        self.setLayout(self.layout)


class DiceRollerPanel(QWidget):
    """Panel to roll multiple dice rows, each with its own modifier."""

    def __init__(self, history_callback):
        super().__init__()
        self.history_callback = history_callback
        self.dice_rows = []

        self.layout = QVBoxLayout()

        # Container for dice rows
        self.rows_layout = QVBoxLayout()
        self.add_dice_row()  # first default row

        # Add row button
        self.add_row_button = QPushButton("Add Another Dice")
        self.add_row_button.clicked.connect(self.add_dice_row)

        # Roll button
        self.roll_button = QPushButton("Roll Dice")
        self.roll_button.clicked.connect(self.roll)

        # Result labels
        self.rolls_label = QLabel("Rolls: -")
        self.modifiers_label = QLabel("Modifiers sum: 0")  # NEW LABEL
        self.total_label = QLabel("Total: -")
        self.rolls_label.setStyleSheet("font-size: 16px;")
        self.modifiers_label.setStyleSheet("font-size: 16px;")
        self.total_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        # Assemble layout
        self.layout.addLayout(self.rows_layout)
        self.layout.addWidget(self.add_row_button)
        self.layout.addWidget(self.roll_button)
        self.layout.addWidget(self.rolls_label)
        self.layout.addWidget(self.modifiers_label)  # show sum of modifiers
        self.layout.addWidget(self.total_label)
        self.setLayout(self.layout)

    def add_dice_row(self):
        row = DiceRow(remove_callback=self.remove_dice_row)
        self.dice_rows.append(row)
        self.rows_layout.addWidget(row)

    def remove_dice_row(self, row):
        self.dice_rows.remove(row)
        row.setParent(None)

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
                self.rolls_label.setText("Invalid input in a dice row!")
                return

            # Roll dice for this row
            rolls = roll_dice(count, sides)
            total_rolls.extend(rolls)

            # Keep track of sum of all row modifiers
            total_modifiers += mod

            # Prepare formula string for this row (keep MOD visible)
            mod_text = f"+{mod}" if mod >= 0 else f"{mod}"
            formula_parts.append(f"{count}d{sides}{mod_text}")

        # Grand total = sum of all rolls + sum of modifiers
        grand_total = calculate_total(total_rolls) + total_modifiers

        # Update main display labels
        rolls_text = ", ".join(map(str, total_rolls))
        self.rolls_label.setText(f"Rolls: {rolls_text}")
        self.modifiers_label.setText(f"Modifiers sum: {total_modifiers}")
        self.total_label.setText(f"Total: {grand_total}")

        # History: formula with per-row MOD, parentheses = rolls + sum of MOD
        formula_str = " + ".join(formula_parts)
        self.history_callback(
            formula_str,
            grand_total,
            f"{rolls_text} + {total_modifiers}"
        )