from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QListWidget,
    QPushButton,
    QLabel
)

from views.propose_game_dialog import ProposeGameDialog


class AddGameDialog(QDialog):
    def __init__(self, games):
        super().__init__()

        self.games = games
        self.selected_game = None

        self.setWindowTitle("Dodaj grę")
        self.setMinimumWidth(500)

        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
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
        self.propose_button = QPushButton("Nie widzę gry? Zgłoś nową")

        layout.addWidget(self.add_button)
        layout.addWidget(QLabel("Nie widzisz swojej gry na liście?"))
        layout.addWidget(self.propose_button)

        self.setLayout(layout)

    def connect_signals(self):
        self.add_button.clicked.connect(self.accept_selected_game)
        self.propose_button.clicked.connect(self.open_propose_game_dialog)

    def accept_selected_game(self):
        selected_index = self.games_list.currentRow()

        if selected_index < 0:
            return

        self.selected_game = self.games[selected_index]
        self.accept()

    def open_propose_game_dialog(self):
        dialog = ProposeGameDialog()
        dialog.exec()

    def get_selected_game(self):
        return self.selected_game