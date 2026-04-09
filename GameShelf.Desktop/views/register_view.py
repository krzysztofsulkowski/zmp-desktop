from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class RegisterView(QWidget):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller

        layout = QVBoxLayout()

        label = QLabel("Register View")

        layout.addWidget(label)
        self.setLayout(layout)