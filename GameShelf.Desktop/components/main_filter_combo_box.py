from pathlib import Path

from PySide6.QtWidgets import QComboBox


class MainFilterComboBox(QComboBox):
    def __init__(self, assets_dir):
        super().__init__()

        self.assets_dir = Path(assets_dir)
        self.setObjectName("mainFilter")
        self._apply_arrow_icon("ArrowDownIcon.svg")

    def showPopup(self):
        self._apply_arrow_icon("ArrowUpIcon.svg")
        super().showPopup()

    def hidePopup(self):
        super().hidePopup()
        self._apply_arrow_icon("ArrowDownIcon.svg")

    def _apply_arrow_icon(self, icon_name):
        icon_path = (self.assets_dir / icon_name).as_posix()
        self.setStyleSheet(f"""
            QComboBox#mainFilter::down-arrow {{
                image: url({icon_path});
            }}
        """)
