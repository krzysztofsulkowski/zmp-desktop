from PySide6.QtWidgets import QLabel, QLineEdit, QTextEdit, QComboBox, QPushButton, QDialog

from services.game_service import get_game_genres, get_game_platforms, propose_game
from views.styled_dialog import StyledDialog, show_info, show_warning
from views.styled_file_dialog import StyledFileDialog


class ProposeGameDialog(StyledDialog):
    def __init__(self):
        super().__init__("Zgłoś nową grę")

        self.image_path = None
        self.genres = []
        self.platforms = []

        self.setMinimumWidth(560)
        self.setup_ui()
        self.load_options()
        self.connect_signals()

    def setup_ui(self):
        self.title_input = QLineEdit()
        self.description_input = QTextEdit()
        self.description_input.setMinimumHeight(100)
        self.genre_select = QComboBox()
        self.platform_select = QComboBox()
        self.image_label = QLabel("Nie wybrano pliku")
        self.image_label.setWordWrap(True)

        self.image_button = QPushButton("Wybierz miniaturkę")
        self.submit_button = QPushButton("Wyślij zgłoszenie")

        self.body_layout.addWidget(QLabel("Tytuł*"))
        self.body_layout.addWidget(self.title_input)
        self.body_layout.addWidget(QLabel("Opis"))
        self.body_layout.addWidget(self.description_input)
        self.body_layout.addWidget(QLabel("Gatunek*"))
        self.body_layout.addWidget(self.genre_select)
        self.body_layout.addWidget(QLabel("Platforma*"))
        self.body_layout.addWidget(self.platform_select)
        self.body_layout.addWidget(QLabel("Miniaturka"))
        self.body_layout.addWidget(self.image_label)
        self.body_layout.addWidget(self.image_button)
        self.body_layout.addWidget(self.submit_button)

    def connect_signals(self):
        self.image_button.clicked.connect(self.select_image)
        self.submit_button.clicked.connect(self.submit)

    def load_options(self):
        self.genres = get_game_genres()
        self.platforms = get_game_platforms()

        self.genre_select.clear()
        self.platform_select.clear()

        for genre in self.genres:
            genre_id = genre.get("id")
            genre_name = genre.get("name", "Bez nazwy")
            self.genre_select.addItem(genre_name, genre_id)

        for platform in self.platforms:
            platform_id = platform.get("id")
            platform_name = platform.get("name", "Bez nazwy")
            self.platform_select.addItem(platform_name, platform_id)

    def select_image(self):
        file_dialog = StyledFileDialog(
            self,
            "Wybierz miniaturkę gry",
            "Obrazy (*.png *.jpg *.jpeg *.webp)",
        )

        if file_dialog.exec() != QDialog.DialogCode.Accepted:
            return

        selected_files = file_dialog.selectedFiles()

        if not selected_files:
            return

        self.image_path = selected_files[0]
        self.image_label.setText(self.image_path)

    def submit(self):
        title = self.title_input.text().strip()
        description = self.description_input.toPlainText().strip()

        if not title:
            show_warning(self, "Tytuł gry jest wymagany.")
            return

        if self.genre_select.currentIndex() < 0:
            show_warning(self, "Wybierz gatunek gry.")
            return

        if self.platform_select.currentIndex() < 0:
            show_warning(self, "Wybierz platformę gry.")
            return

        genre_id = self.genre_select.currentData()
        platform_id = self.platform_select.currentData()

        success = propose_game(title, description, genre_id, platform_id, self.image_path)

        if not success:
            show_warning(self, "Nie udało się wysłać zgłoszenia.")
            return

        show_info(self, "Zgłoszenie gry zostało wysłane do administratora.")
        self.accept()
