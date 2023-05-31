from PyQt6.QtCore import Qt, QMimeData
from PyQt6.QtWidgets import (
    QLabel, QSizePolicy, QHBoxLayout, QVBoxLayout, QApplication,
    QPushButton, QWidget, QListWidget, QListWidgetItem
)
from PyQt6.QtGui import QPixmap, QDragEnterEvent, QDropEvent, QIcon, QPainter, QFont
import sys
import webbrowser
from PIL import Image
import os


class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.resize(850, 550)
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #454545;
                background-color: transparent;
            }
            QLabel#combinedLabel {
                border: none;
            }
        """)

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
            self.background_image_1
        )
        painter.drawPixmap(
            combined_image.rect().center() - self.background_image_2.rect().center(),
            self.background_image_2
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

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls() and all(
            url.isLocalFile() and url.toLocalFile().lower().endswith(('.png', '.jpg', '.jpeg'))
            for url in event.mimeData().urls()
        ):
            event.acceptProposedAction()

    def dragMoveEvent(self, event: QDragEnterEvent):
        event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
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
                    Qt.TransformationMode.SmoothTransformation
                )
            )


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(900, 600)
        self.setContentsMargins(10, 10, 10, 10)
        self.setStyleSheet("background-color: #1C2626;")
        self.setWindowTitle("KZM IMAGE TO WEBP")
        self.setWindowIcon(QIcon("static/img/Vector.png"))
        self.setAcceptDrops(True)

        main_layout = QVBoxLayout(self)

        self.image_label = ImageLabel()
        main_layout.addWidget(self.image_label)

        self.image_list = QListWidget()
        self.image_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        main_layout.addWidget(self.image_list)

        self.image_list.hide()

        self.total_files_label = QLabel(self)
        self.total_files_label.setStyleSheet("color: white; font-size: 16px;")
        font = QFont("Poppins", 16)
        self.total_files_label.setFont(font)
        main_layout.addWidget(self.total_files_label, alignment=Qt.AlignmentFlag.AlignLeft)
        self.total_files_label.hide()

        self.convert_button = QPushButton()
        self.convert_button.setText("Convert")
        self.convert_button.setStyleSheet(
            "QPushButton { border: 1px; background-color: #552D96; width:850px;height:35px;}"
        )
        font = QFont("Poppins", 14)
        self.convert_button.setFont(font)
        main_layout.addWidget(self.convert_button)
        self.convert_button.clicked.connect(self.ConvertAction)
        self.convert_button.hide()

        button_layout = QHBoxLayout()

        self.Go_Back_button = QPushButton()
        self.Go_Back_button.setText("Go Back")
        font = QFont("Poppins", 14)
        self.Go_Back_button.setFont(font)
        self.Go_Back_button.setStyleSheet(
            "border: 1px; background-color: #3F4746; width:650px;height:35px;"
        )
        button_layout.addWidget(self.Go_Back_button, alignment=Qt.AlignmentFlag.AlignLeft)
        self.Go_Back_button.clicked.connect(self.GO_Back_Action)
        button_layout.addStretch()
        self.Go_Back_button.hide()

        self.save_files = QPushButton()
        self.save_files.setText("Save Files")
        self.save_files.setStyleSheet("border:1px;background-color:#552D96;width:200px;height:35px;")
        font = QFont("Poppins", 14)
        self.save_files.setFont(font)
        button_layout.addWidget(self.save_files, alignment=Qt.AlignmentFlag.AlignRight)
        
        self.save_files.clicked.connect(self.Save_Files)
        self.save_files.hide()


        self.saved_files_successfully = QLabel()
        self.saved_files_successfully.setText("webp-Files are Saved")
        self.saved_files_successfully.setStyleSheet("border:1px;background-color:#146C94;width:180px;height:35px;")
        font = QFont("Poppins", 14)
        self.saved_files_successfully.setFont(font)
        button_layout.addWidget(self.saved_files_successfully, alignment=Qt.AlignmentFlag.AlignRight)
       
        self.saved_files_successfully.hide()

        main_layout.addLayout(button_layout)

        additional_layout = QHBoxLayout()
        self.additional_label = QLabel("Designed and Developed by Khuzaima N.")
        self.additional_label.setStyleSheet("color: white; font-size: 14px;")
        additional_layout.addWidget(self.additional_label)
        additional_layout.addStretch()
        main_layout.addLayout(additional_layout)

        self.button = QPushButton()
        self.button.setIcon(QIcon("static/img/GithubIcon.png"))
        self.button.setStyleSheet("QPushButton { border: none; padding: 0px; }")
        additional_layout.addStretch()
        additional_layout.addWidget(self.button)

        self.counter = 0
        self.max_files_threshold = 14
        self.scrollbar_added = False

    def Save_Files(self):
        save_directory = os.path.join(os.path.expanduser("~"), "webp_files")  # Change the directory as per your needs
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        for i in range(self.image_list.count()):
            item = self.image_list.item(i)
            file_path = item.data(Qt.ItemDataRole.UserRole)

            try:
                # Open the image file
                image = Image.open(file_path)

                # Convert the image to WebP format
                webp_path = os.path.splitext(file_path)[0] + ".webp"
                webp_save_path = os.path.join(save_directory, os.path.basename(webp_path))
                image.save(webp_save_path, "WebP")

                # Update the list item text to the WebP file path
                item.setData(Qt.ItemDataRole.UserRole, webp_save_path)
                item.setText(os.path.basename(webp_save_path))
            except Exception as e:
                # Handle any errors that occur during conversion
                print(f"Error converting {file_path}: {str(e)}")
        self.save_files.hide()
        self.saved_files_successfully.show()
        self.resize(900,600)
      

    def GO_Back_Action(self):
        self.Go_Back_button.hide()
        self.save_files.hide()
        self.saved_files_successfully.hide()
        self.convert_button.hide()
        self.image_list.hide()
        self.total_files_label.hide()
        self.image_label.show()
        self.image_label.clear()
        self.image_list.clear()
        self.resize(900,600)

    def add_scrollbar_to_list(self):
        self.scrollbar_added = True
        self.image_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    def ConvertAction(self):
        for i in range(self.image_list.count()):
            item = self.image_list.item(i)
            file_path = item.data(Qt.ItemDataRole.UserRole)

            try:
                # Open the image file
                image = Image.open(file_path)

                # Convert the image to WebP format
                webp_path = os.path.splitext(file_path)[0] + ".webp"
                image.save(webp_path, "WebP")

                # Update the list item text to the WebP file path
                item.setData(Qt.ItemDataRole.UserRole, webp_path)
                item.setText(os.path.basename(webp_path))
            except Exception as e:
                # Handle any errors that occur during conversion
                print(f"Error converting {file_path}: {str(e)}")

        self.convert_button.hide()
        self.resize(900,600)
        self.Go_Back_button.show()
        self.save_files.show()

    def open_source_code(self):
        webbrowser.open("https://github.com/kzmfhm/webp-converter")

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls() and len(event.mimeData().urls()) > 0 and event.mimeData().urls()[0].isLocalFile():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QDragEnterEvent):
        event.acceptProposedAction()

    
    def dropEvent(self, event: QDropEvent):
        if self.Go_Back_button.isVisible():
            event.ignore()
            return
        

        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                self.image_label.set_image(file_path)
                self.image_list.show()

                item = QListWidgetItem(os.path.basename(file_path))
                item.setData(Qt.ItemDataRole.UserRole, file_path)
                self.image_list.addItem(item)
                self.image_list.scrollToBottom()
                self.image_list.setGeometry(25, 50, 800, 460)
                self.image_list.setAlternatingRowColors(True)

                # Set stylesheet for each item in the QListWidget
                item_style = (
                    "QListWidget::item { padding: 10px; background: #212E2E; border: 1px solid #445858; margin: 5px; }"
                )
                self.image_list.setStyleSheet(item_style)

                self.image_label.hide()
                if not self.scrollbar_added and self.image_list.count() >= self.max_files_threshold:
                    self.add_scrollbar_to_list()

                self.total_files_label.show()
                self.convert_button.show()
                self.total_files_label.setText(f"Total Files: {self.image_list.count()}")
                self.resize(900,600)
        event.acceptProposedAction()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())































