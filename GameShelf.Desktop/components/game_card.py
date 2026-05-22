from pathlib import Path

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QSizePolicy, QHBoxLayout, QVBoxLayout


class GameCard(QFrame):
    def __init__(self, game, assets_dir, cover_service, on_rate, on_move, on_remove):
        super().__init__()

        self.game = game
        self.assets_dir = Path(assets_dir)
        self.cover_service = cover_service
        self.on_rate = on_rate
        self.on_move = on_move
        self.on_remove = on_remove

        self.setObjectName("libraryGameCard")
        self.setFixedSize(252, 218)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        cover = QLabel()
        cover.setObjectName("gameCover")
        cover.setFixedSize(252, 140)
        cover.setAlignment(Qt.AlignCenter)
        self.cover_service.set_cover_image(cover, self.game)

        info = QFrame()
        info.setObjectName("gameInfoPanel")
        info.setFixedSize(252, 78)

        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(10, 6, 10, 6)
        info_layout.setSpacing(3)

        title = QLabel(self.game.title)
        title.setObjectName("libraryGameTitle")
        title.setAlignment(Qt.AlignLeft)
        title.setWordWrap(False)

        platform_label = QLabel(self.game.platform or "")
        platform_label.setObjectName("libraryGamePlatform")
        platform_label.setAlignment(Qt.AlignLeft)

        actions_row = QHBoxLayout()
        actions_row.setContentsMargins(0, 0, 0, 0)
        actions_row.setSpacing(5)

        actions_row.addWidget(self.create_rating_button())
        actions_row.addWidget(self.create_move_button())
        actions_row.addStretch()
        actions_row.addWidget(self.create_delete_button())

        info_layout.addWidget(title)
        info_layout.addWidget(platform_label)
        info_layout.addLayout(actions_row)
        info.setLayout(info_layout)

        self.add_platform_badge()

        layout.addWidget(cover)
        layout.addWidget(info)
        self.setLayout(layout)

    def create_rating_button(self):
        button = QPushButton()
        button.setObjectName("gameCardActionBtn")
        button.setToolTip("Oceń grę")
        button.setFixedSize(32, 24)
        button.setIcon(QIcon(str(self.assets_dir / "GameCardStarIcon.svg")))
        button.setIconSize(QSize(13, 13))

        if self.game.rating:
            button.setText(str(self.game.rating))
            button.setFixedSize(62, 24)

        button.clicked.connect(lambda checked=False: self.on_rate(self.game))
        return button

    def create_move_button(self):
        button = QPushButton()
        button.setObjectName("gameCardActionBtn")
        button.setToolTip("Przenieś do kolekcji")
        button.setFixedSize(30, 24)
        button.setIcon(QIcon(str(self.assets_dir / "GameCardMoveIcon.svg")))
        button.setIconSize(QSize(14, 14))
        button.clicked.connect(lambda checked=False: self.on_move(self.game))
        return button

    def create_delete_button(self):
        button = QPushButton()
        button.setObjectName("gameCardDeleteBtn")
        button.setToolTip("Usuń z kolekcji")
        button.setFixedSize(30, 24)
        button.setIcon(QIcon(str(self.assets_dir / "GameCardDeleteIcon.svg")))
        button.setIconSize(QSize(14, 14))
        button.clicked.connect(lambda checked=False: self.on_remove(self.game.game_id))
        return button

    def add_platform_badge(self):
        platform_text = self.game.platform or ""

        if not platform_text:
            return

        badge = QLabel(platform_text)
        badge.setObjectName("platformBadge")
        badge.setAlignment(Qt.AlignCenter)
        badge.setParent(self)
        badge.adjustSize()
        badge.resize(max(40, badge.sizeHint().width() + 16), 22)
        badge.move(10, 10)
        badge.raise_()


class AddGameCard(QPushButton):
    def __init__(self, assets_dir, on_click):
        super().__init__()

        self.assets_dir = Path(assets_dir)
        self.setObjectName("addGameCard")
        self.setFixedSize(252, 218)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.clicked.connect(on_click)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 24, 20, 24)
        layout.setSpacing(14)

        plus_circle = QLabel()
        plus_circle.setObjectName("addGamePlus")
        plus_circle.setAlignment(Qt.AlignCenter)
        plus_circle.setFixedSize(58, 58)
        plus_icon = QPixmap(str(self.assets_dir / "AddGameIcon.svg"))
        plus_circle.setPixmap(plus_icon.scaled(58, 58, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        text = QLabel("dodaj kolejną grę")
        text.setObjectName("addGameText")
        text.setAlignment(Qt.AlignCenter)
        text.setWordWrap(True)

        layout.addStretch()
        layout.addWidget(plus_circle, alignment=Qt.AlignCenter)
        layout.addWidget(text)
        layout.addStretch()

        self.setLayout(layout)
