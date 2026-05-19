from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QPushButton,
    QFileDialog,
    QMessageBox
)

from services.game_service import (
    get_game_genres,
    get_game_platforms,
    propose_game
)


class ProposeGameDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.image_path = None
        self.genres = []
        self.platforms = []

        self.setWindowTitle("Zgłoś nową grę")
        self.setMinimumWidth(500)

        self.setup_ui()
        self.load_options()
        self.connect_signals()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.description_input = QTextEdit()
        self.genre_select = QComboBox()
        self.platform_select = QComboBox()
        self.image_label = QLabel("Nie wybrano pliku")

        self.image_button = QPushButton("Wybierz miniaturkę")
        self.submit_button = QPushButton("Wyślij zgłoszenie")

        layout.addWidget(QLabel("Tytuł*"))
        layout.addWidget(self.title_input)

        layout.addWidget(QLabel("Opis"))
        layout.addWidget(self.description_input)

        layout.addWidget(QLabel("Gatunek*"))
        layout.addWidget(self.genre_select)

        layout.addWidget(QLabel("Platforma*"))
        layout.addWidget(self.platform_select)

        layout.addWidget(QLabel("Miniaturka"))
        layout.addWidget(self.image_label)
        layout.addWidget(self.image_button)

        layout.addWidget(self.submit_button)

        self.setLayout(layout)

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
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Wybierz miniaturkę gry",
            "",
            "Obrazy (*.png *.jpg *.jpeg *.webp)"
        )

        if not file_path:
            return

        self.image_path = file_path
        self.image_label.setText(file_path)

    def submit(self):
        title = self.title_input.text().strip()
        description = self.description_input.toPlainText().strip()

        if not title:
            self.show_warning("Tytuł gry jest wymagany.")
            return

        if self.genre_select.currentIndex() < 0:
            self.show_warning("Wybierz gatunek gry.")
            return

        if self.platform_select.currentIndex() < 0:
            self.show_warning("Wybierz platformę gry.")
            return

        genre_id = self.genre_select.currentData()
        platform_id = self.platform_select.currentData()

        success = propose_game(
            title,
            description,
            genre_id,
            platform_id,
            self.image_path
        )

        if not success:
            self.show_warning("Nie udało się wysłać zgłoszenia.")
            return

        QMessageBox.information(
            self,
            "GameShelf",
            "Zgłoszenie gry zostało wysłane do administratora."
        )

        self.accept()

    def show_warning(self, message):
        QMessageBox.warning(self, "GameShelf", message)