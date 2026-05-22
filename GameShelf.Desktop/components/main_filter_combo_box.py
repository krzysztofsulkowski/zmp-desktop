from pathlib import Path

from PySide6.QtWidgets import QComboBox


class MainFilterComboBox(QComboBox):
    def __init__(self, assets_dir):
        super().__init__()

        self.assets_dir = Path(assets_dir)
        self.setObjectName("mainFilter")
        self.set_arrow_icon("ArrowDownIcon.svg")

    def showPopup(self):
        self.set_arrow_icon("ArrowUpIcon.svg")
        super().showPopup()

    def hidePopup(self):
        super().hidePopup()
        self.set_arrow_icon("ArrowDownIcon.svg")

    def set_arrow_icon(self, icon_name):
        icon_path = (self.assets_dir / icon_name).as_posix()
        self.setStyleSheet(f"""
            QComboBox#mainFilter {{
                background-color: #261C40;
                color: #ffffff;
                border: none;
                border-radius: 7px;
                padding-left: 10px;
                padding-right: 34px;
                padding-top: 0px;
                padding-bottom: 0px;
                font-family: "Figtree Light", "Figtree", "Segoe UI", "Arial";
                font-size: 16px;
                font-weight: 300;
                min-height: 36px;
                max-height: 36px;
            }}

            QComboBox#mainFilter::drop-down {{
                border: none;
                width: 34px;
                subcontrol-origin: padding;
                subcontrol-position: top right;
            }}

            QComboBox#mainFilter::down-arrow {{
                image: url({icon_path});
                width: 12px;
                height: 12px;
                margin-right: 10px;
            }}

            QComboBox#mainFilter QAbstractItemView {{
                background-color: #21153B;
                color: #ffffff;
                border: 1px solid #8B5CF6;
                selection-background-color: #7C3AED;
            }}
        """)
