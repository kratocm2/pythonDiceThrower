from PySide6.QtWidgets import QWidget, QVBoxLayout
from ui.dice_roller import DiceRollerPanel
from ui.history_panel import HistoryPanel

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dice Simulator - Multiple Dice Types")
        self.resize(600, 500)

        self.layout = QVBoxLayout()

        self.history_panel = HistoryPanel()
        self.dice_roller = DiceRollerPanel(history_callback=self.history_panel.add_roll)

        self.layout.addWidget(self.dice_roller)
        self.layout.addWidget(self.history_panel)

        self.setLayout(self.layout)