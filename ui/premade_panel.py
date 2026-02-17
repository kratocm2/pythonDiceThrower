from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

class PremadePanel(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        label = QLabel("Zde budou premade hody")
        layout.addWidget(label)

        self.setLayout(layout)