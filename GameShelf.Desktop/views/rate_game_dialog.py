from PySide6.QtWidgets import QLabel, QComboBox, QPushButton

from views.styled_dialog import StyledDialog


class RateGameDialog(StyledDialog):
    def __init__(self, current_rating=None):
        super().__init__("Oceń grę")
        self.setMinimumWidth(340)
        self.current_rating = current_rating
        self.setup_ui()

    def setup_ui(self):
        title = QLabel("Wybierz ocenę gry")
        self.body_layout.addWidget(title)

        self.rating_select = QComboBox()

        for rating in range(1, 11):
            self.rating_select.addItem(str(rating), rating)

        if self.current_rating:
            index = self.rating_select.findData(self.current_rating)

            if index >= 0:
                self.rating_select.setCurrentIndex(index)

        self.body_layout.addWidget(self.rating_select)

        self.submit_button = QPushButton("Zapisz ocenę")
        self.submit_button.clicked.connect(self.accept)
        self.body_layout.addWidget(self.submit_button)

    def get_rating(self):
        return self.rating_select.currentData()
