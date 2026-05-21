from PySide6.QtWidgets import QCheckBox, QHBoxLayout, QLabel, QLineEdit, QPushButton

from views.styled_dialog import StyledDialog


class CreateCollectionDialog(StyledDialog):
    def __init__(self):
        super().__init__("Utwórz kolekcję")
        self.setMinimumWidth(400)

        self.name_label = QLabel("Nazwa kolekcji")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Wpisz nazwę kolekcji")

        self.public_checkbox = QCheckBox("Kolekcja publiczna")
        self.public_checkbox.setChecked(True)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        self.cancel_button = QPushButton("Anuluj")
        self.create_button = QPushButton("Utwórz")

        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.create_button)

        self.body_layout.addWidget(self.name_label)
        self.body_layout.addWidget(self.name_input)
        self.body_layout.addWidget(self.public_checkbox)
        self.body_layout.addLayout(buttons_layout)

        self.create_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_collection_data(self):
        return self.name_input.text().strip(), self.public_checkbox.isChecked()
