from PySide6.QtWidgets import QLabel, QComboBox, QPushButton

from views.styled_dialog import StyledDialog


class MoveGameDialog(StyledDialog):
    def __init__(self, collections, current_collection_id):
        super().__init__("Przenieś grę")

        self.collections = collections
        self.current_collection_id = current_collection_id

        self.setMinimumWidth(400)
        self.setup_ui()

    def setup_ui(self):
        title = QLabel("Wybierz kolekcję docelową")
        self.body_layout.addWidget(title)

        self.collection_select = QComboBox()

        for collection in self.collections:
            collection_id = collection.get("id")

            if collection_id == self.current_collection_id:
                continue

            collection_name = collection.get("name", "Bez nazwy")
            self.collection_select.addItem(collection_name, collection_id)

        self.body_layout.addWidget(self.collection_select)

        self.submit_button = QPushButton("Przenieś grę")
        self.submit_button.clicked.connect(self.accept)
        self.body_layout.addWidget(self.submit_button)

    def get_selected_collection_id(self):
        return self.collection_select.currentData()
