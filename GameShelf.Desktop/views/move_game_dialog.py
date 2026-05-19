from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QPushButton
)


class MoveGameDialog(QDialog):
    def __init__(self, collections, current_collection_id):
        super().__init__()

        self.collections = collections
        self.current_collection_id = current_collection_id

        self.setWindowTitle("Przenieś grę")
        self.setMinimumWidth(350)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Wybierz kolekcję docelową")
        layout.addWidget(title)

        self.collection_select = QComboBox()

        for collection in self.collections:
            collection_id = collection.get("id")

            if collection_id == self.current_collection_id:
                continue

            collection_name = collection.get("name", "Bez nazwy")

            self.collection_select.addItem(
                collection_name,
                collection_id
            )

        layout.addWidget(self.collection_select)

        self.submit_button = QPushButton("Przenieś grę")
        self.submit_button.clicked.connect(self.accept)

        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def get_selected_collection_id(self):
        return self.collection_select.currentData()