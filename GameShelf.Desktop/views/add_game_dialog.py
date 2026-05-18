from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QListWidget,
    QPushButton,
    QLabel
)


class AddGameDialog(QDialog):
    def __init__(self, games):
        super().__init__()

        self.games = games
        self.selected_game = None

        self.setWindowTitle("Dodaj grę")
        self.setMinimumWidth(500)

        layout = QVBoxLayout()

        title = QLabel("Wybierz grę do dodania")
        layout.addWidget(title)

        self.games_list = QListWidget()

        for game in self.games:
            title = game.get("title", "Bez nazwy")
            genre = game.get("genre", {}).get("name", "")
            self.games_list.addItem(f"{title} - {genre}")

        layout.addWidget(self.games_list)

        self.add_button = QPushButton("Dodaj")
        layout.addWidget(self.add_button)

        self.setLayout(layout)

        self.add_button.clicked.connect(self.accept_selected_game)

    def accept_selected_game(self):
        selected_index = self.games_list.currentRow()

        if selected_index < 0:
            return

        self.selected_game = self.games[selected_index]
        self.accept()

    def get_selected_game(self):
        return self.selected_game