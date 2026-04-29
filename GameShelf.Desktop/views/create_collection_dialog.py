from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QCheckBox, QPushButton
)


class CreateCollectionDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Create Collection")

        layout = QVBoxLayout()

        self.name_label = QLabel("Nazwa kolekcji")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Wpisz nazwę kolekcji")

        self.public_checkbox = QCheckBox("Kolekcja publiczna")
        self.public_checkbox.setChecked(True)

        buttons_layout = QHBoxLayout()

        self.create_button = QPushButton("Create")
        self.cancel_button = QPushButton("Cancel")

        buttons_layout.addWidget(self.create_button)
        buttons_layout.addWidget(self.cancel_button)

        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.public_checkbox)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        self.create_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_collection_data(self):
        return self.name_input.text().strip(), self.public_checkbox.isChecked()