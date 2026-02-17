from PySide6.QtWidgets import QWidget, QVBoxLayout, QTabWidget

from ui.dice_roller import DiceRollerPanel
from ui.history_panel import HistoryPanel
from ui.premade_panel import PremadePanel   # vytvoříš nový panel

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dice Simulator - Multiple Dice Types")
        self.resize(600, 500)

        self.layout = QVBoxLayout()

        # vytvoření tab widgetu
        self.tabs = QTabWidget()

        # panely
        self.history_panel = HistoryPanel()
        self.premade_panel = PremadePanel()

        # dice roller
        self.dice_roller = DiceRollerPanel(
            history_callback=self.history_panel.add_roll
        )

        # přidání tabů
        self.tabs.addTab(self.history_panel, "History")
        self.tabs.addTab(self.premade_panel, "Premade hody")

        # layout
        self.layout.addWidget(self.dice_roller)
        self.layout.addWidget(self.tabs)

        self.setLayout(self.layout)