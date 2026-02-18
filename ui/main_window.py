from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from ui.dice_roller import DiceRollerPanel
from ui.history_panel import HistoryPanel
from ui.premade_panel import PremadePanel


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dice Simulator - Multiple Dice Types")
        self.resize(600, 500)

        self.layout = QVBoxLayout()
        self.tabs = QTabWidget()

        # Panely
        self.history_panel = HistoryPanel()
        self.dice_roller = DiceRollerPanel(
            history_callback=self.history_panel.add_roll
        )
        self.premade_panel = PremadePanel(self.dice_roller)

        # Tab setup
        self.tabs.addTab(self.history_panel, "History")
        self.tabs.addTab(self.premade_panel, "Premade hody")

        # Layout
        self.layout.addWidget(self.dice_roller)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)