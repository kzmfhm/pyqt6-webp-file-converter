#!/home/khuzaima/Public/pyqt6-webp-file-converter/venv/bin/python3
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
)
from PyQt6.QtGui import QPixmap, QDragEnterEvent, QDropEvent, QPainter, QFont


class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.resize(850, 550)
        self.setStyleSheet(
            """
            QLabel {
                border: 2px dashed #454545;
                background-color: transparent;
            }
            QLabel#combinedLabel {
                border: none;
            }
        """
        )

        self.background_image_1 = QPixmap("static/img/cloud.png")
        self.background_image_2 = QPixmap("static/img/arrow.png")
        self.button1 = QPushButton()

        self.image_paths = []
        self.update_label()

    def update_label(self):
        vbox = QVBoxLayout(self)
        vbox.addStretch(1)
        hbox = QHBoxLayout()
        hbox.addStretch(1)  # Add stretchable space to center-align the combined image
        combined_label = QLabel()
        combined_label.setObjectName("combinedLabel")

        combined_image = QPixmap(self.background_image_1.size())
        combined_image.fill(Qt.GlobalColor.transparent)

        painter = QPainter(combined_image)
        painter.drawPixmap(
            combined_image.rect().center() - self.background_image_1.rect().center(),
            self.background_image_1,
        )
        painter.drawPixmap(
            combined_image.rect().center() - self.background_image_2.rect().center(),
            self.background_image_2,
        )
        painter.end()

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.resize(850, 550)

        combined_label.setPixmap(combined_image)

        hbox.addWidget(combined_label)
        hbox.addStretch(1)
        vbox.addLayout(hbox)

        button1 = QPushButton("Drag and Drop here")
        button1.setStyleSheet("QPushButton { border: none; }")
        font = QFont("Roboto", 30)
        button1.setFont(font)

        vbox.addWidget(button1, alignment=Qt.AlignmentFlag.AlignCenter)
        vbox.addStretch(1)

    def drag_enter_event(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls() and all(
            url.isLocalFile()
            and url.toLocalFile().lower().endswith((".png", ".jpg", ".jpeg"))
            for url in event.mimeData().urls()
        ):
            event.acceptProposedAction()

    def drag_move_event(self, event: QDragEnterEvent):
        event.acceptProposedAction()

    def drop_event(self, event: QDropEvent):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            self.image_paths.append(file_path)
            self.set_image(file_path)

        event.acceptProposedAction()

    def set_image(self, file_path):
        pixmap = QPixmap(file_path)
        if pixmap.isNull():
            self.setText("Invalid image file")
        else:
            self.setPixmap(
                pixmap.scaled(
                    self.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
