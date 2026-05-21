from PySide6.QtWidgets import QListWidget, QPushButton, QLabel

from views.propose_game_dialog import ProposeGameDialog
from views.styled_dialog import StyledDialog, show_warning


class AddGameDialog(StyledDialog):
    def __init__(self, games):
        super().__init__("Dodaj grę")

        self.games = games
        self.selected_game = None
        self.setMinimumWidth(540)

        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        title = QLabel("Wybierz grę do dodania")
        self.body_layout.addWidget(title)

        self.games_list = QListWidget()

        for game in self.games:
            title = game.get("title", "Bez nazwy")
            genre = game.get("genre", {}).get("name", "")
            self.games_list.addItem(f"{title} - {genre}")

        self.body_layout.addWidget(self.games_list)

        self.add_button = QPushButton("Dodaj")
        self.propose_button = QPushButton("Nie widzę gry — zgłoś nową")

        self.body_layout.addWidget(self.add_button)
        self.body_layout.addWidget(QLabel("Nie widzisz swojej gry na liście?"))
        self.body_layout.addWidget(self.propose_button)

    def connect_signals(self):
        self.add_button.clicked.connect(self.accept_selected_game)
        self.propose_button.clicked.connect(self.open_propose_game_dialog)

    def accept_selected_game(self):
        selected_index = self.games_list.currentRow()

        if selected_index < 0:
            show_warning(self, "Najpierw wybierz grę z listy.")
            return

        self.selected_game = self.games[selected_index]
        self.accept()

    def open_propose_game_dialog(self):
        dialog = ProposeGameDialog()
        dialog.exec()

    def get_selected_game(self):
        return self.selected_game
