from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QCheckBox, QPushButton
)


class EditCollectionDialog(QDialog):
    def __init__(self, current_name, is_public=True):
        super().__init__()

        self.setWindowTitle("Edit Collection")

        layout = QVBoxLayout()

        self.name_label = QLabel("Nazwa kolekcji")
        self.name_input = QLineEdit()
        self.name_input.setText(current_name)

        self.public_checkbox = QCheckBox("Kolekcja publiczna")
        self.public_checkbox.setChecked(is_public)

        buttons_layout = QHBoxLayout()

        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")

        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)

        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.public_checkbox)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_collection_data(self):
        return self.name_input.text().strip(), self.public_checkbox.isChecked()