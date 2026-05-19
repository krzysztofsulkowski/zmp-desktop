from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QPushButton
)


class RateGameDialog(QDialog):
    def __init__(self, current_rating=None):
        super().__init__()

        self.setWindowTitle("Oceń grę")
        self.setMinimumWidth(300)

        self.current_rating = current_rating

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Wybierz ocenę gry")
        layout.addWidget(title)

        self.rating_select = QComboBox()

        for rating in range(1, 11):
            self.rating_select.addItem(str(rating), rating)

        if self.current_rating:
            index = self.rating_select.findData(self.current_rating)

            if index >= 0:
                self.rating_select.setCurrentIndex(index)

        layout.addWidget(self.rating_select)

        self.submit_button = QPushButton("Zapisz ocenę")
        self.submit_button.clicked.connect(self.accept)

        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def get_rating(self):
        return self.rating_select.currentData()