from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QComboBox,
    QSpinBox,
    QListWidget
)

from logic.dice import roll_dice, calculate_total


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dice Simulator")
        self.resize(400, 400)

        self.layout = QVBoxLayout()

        # Dice selection row
        selection_layout = QHBoxLayout()

        self.dice_selector = QComboBox()
        self.dice_selector.addItems(["4", "6", "8", "10", "12", "20"])

        self.count_selector = QSpinBox()
        self.count_selector.setMinimum(1)
        self.count_selector.setMaximum(100)
        self.count_selector.setValue(1)

        selection_layout.addWidget(QLabel("Dice sides:"))
        selection_layout.addWidget(self.dice_selector)
        selection_layout.addWidget(QLabel("Count:"))
        selection_layout.addWidget(self.count_selector)

        # Roll button
        self.roll_button = QPushButton("Roll Dice")
        self.roll_button.clicked.connect(self.roll)

        # Results
        self.rolls_label = QLabel("Rolls: -")
        self.total_label = QLabel("Total: -")

        self.rolls_label.setStyleSheet("font-size: 16px;")
        self.total_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        # History
        self.history = QListWidget()

        # Add to main layout
        self.layout.addLayout(selection_layout)
        self.layout.addWidget(self.roll_button)
        self.layout.addWidget(self.rolls_label)
        self.layout.addWidget(self.total_label)
        self.layout.addWidget(QLabel("History:"))
        self.layout.addWidget(self.history)

        self.setLayout(self.layout)

    def roll(self):
        sides = int(self.dice_selector.currentText())
        count = self.count_selector.value()

        rolls = roll_dice(count, sides)
        total = calculate_total(rolls)

        rolls_text = ", ".join(map(str, rolls))

        self.rolls_label.setText(f"Rolls: {rolls_text}")
        self.total_label.setText(f"Total: {total}")

        self.history.addItem(f"{count}d{sides}: {rolls_text} = {total}")