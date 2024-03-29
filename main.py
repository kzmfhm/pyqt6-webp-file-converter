#!/home/khuzaima/Public/pyqt6-webp-file-converter/venv/bin/python3
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QApplication,
    QPushButton,
    QWidget,
    QListWidget,
    QListWidgetItem,QMessageBox,QSizePolicy
)
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QIcon, QFont
from labels import ImageLabel
import sys
import webbrowser
from PIL import Image
import os


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
        main_layout.addWidget(
            self.total_files_label, alignment=Qt.AlignmentFlag.AlignLeft
        )
        self.total_files_label.hide()

        self.convert_button = QPushButton()
        self.convert_button.setText("Convert")
        self.convert_button.setStyleSheet(
            "QPushButton { border: 1px; background-color: #552D96; width:850px;height:35px;}"
        )
        font = QFont("Poppins", 14)
        self.convert_button.setFont(font)
        main_layout.addWidget(self.convert_button)
        self.convert_button.clicked.connect(self.convert_action)
        self.convert_button.hide()

        button_layout = QHBoxLayout()

        self.go_back_button = QPushButton()
        self.go_back_button.setText("Go Back")
        font = QFont("Poppins", 14)
        self.go_back_button.setFont(font)
        self.go_back_button.setStyleSheet(
            "border: 1px; background-color: #3F4746; width:650px;height:35px;"
        )
        button_layout.addWidget(
            self.go_back_button, alignment=Qt.AlignmentFlag.AlignLeft
        )
        self.go_back_button.clicked.connect(self.go_back_action)
        button_layout.addStretch()
        self.go_back_button.hide()

        self.save_files = QPushButton()
        self.save_files.setText("Save Files")
        self.save_files.setStyleSheet(
            "border:1px;background-color:#552D96;width:200px;height:35px;"
        )
        font = QFont("Poppins", 14)
        self.save_files.setFont(font)
        button_layout.addWidget(self.save_files, alignment=Qt.AlignmentFlag.AlignRight)
        self.converted_files = []
        self.save_files.clicked.connect(self.save_file)
        self.save_files.hide()

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
        self.button.clicked.connect(self.open_source_code)
        additional_layout.addStretch()
        additional_layout.addWidget(self.button)

        self.counter = 0
        self.max_files_threshold = 14
        self.scrollbar_added = False

    def open_source_code(self):
        webbrowser.open("https://github.com/kzmfhm/pyqt6-webp-file-converter")

    def add_scrollbar_to_list(self):
        self.scrollbar_added = True
        self.image_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    def convert_action(self):
        save_directory = os.path.join(
            os.path.expanduser("~"), "Downloads"
        )  # Change the directory as per your needs
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        for i in range(self.image_list.count()):
            item = self.image_list.item(i)
            file_path = item.data(Qt.ItemDataRole.UserRole)

            try:
                image = Image.open(file_path)
                webp_path = os.path.join(save_directory, os.path.basename(file_path))
                webp_path = os.path.splitext(webp_path)[0] + ".webp"

                # Convert the image to WebP format and save it
                image.save(webp_path, "WebP")

                # Append the webp_path to the converted_files list
                self.converted_files.append(webp_path)

                # Update the list item text to the WebP file path
                item.setData(Qt.ItemDataRole.UserRole, webp_path)
                item.setText(os.path.basename(webp_path))
            except Exception as e:
                # Handle any errors that occur during conversion
                print(f"Error converting {file_path}: {str(e)}")

        self.convert_button.hide()
        self.resize(900, 600)
        self.go_back_button.show()
        self.save_files.show()

    def save_file(self,s):
        save_directory = os.path.join(
            os.path.expanduser("~"), "Downloads"
        )  # Change the directory as per your needs
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        for file_path in self.converted_files:
            try:
                # Check the file extension
                _, file_extension = os.path.splitext(file_path)
                if file_extension.lower() == ".webp":
                    # Open the image file
                    image = Image.open(file_path)

                    # Construct the webp_save_path
                    webp_save_path = os.path.join(
                        save_directory, os.path.basename(file_path)
                    )

                    # Save the image as WebP format
                    image.save(webp_save_path, "WebP")
            except Exception as e:
                # Handle any errors that occur during saving
                print(f"Error saving {file_path} as WebP: {str(e)}")

        dlg = QMessageBox(self)
        dlg.setWindowTitle("Checkout Save Files!")
        dlg.setText("WebP files are saved in Downloads.")
        dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
        dlg.exec()

        self.resize(900, 600)
    def go_back_action(self):
        self.go_back_button.hide()
        self.save_files.hide()
        self.convert_button.hide()
        self.image_list.hide()
        self.total_files_label.hide()
        self.image_label.show()
        self.image_label.clear()
        self.image_list.clear()
        self.resize(900, 600)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if (
            event.mimeData().hasUrls()
            and len(event.mimeData().urls()) > 0
            and event.mimeData().urls()[0].isLocalFile()
        ):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        if self.go_back_button.isVisible():
            event.ignore()
            return

        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.lower().endswith((".png", ".jpg", ".jpeg")):
                self.image_label.set_image(file_path)
                self.image_list.show()

                item = QListWidgetItem(os.path.basename(file_path))
                item.setData(Qt.ItemDataRole.UserRole, file_path)
                self.image_list.addItem(item)
                self.image_list.scrollToBottom()
                self.image_list.setGeometry(25, 50, 800, 460)
                self.image_list.setAlternatingRowColors(True)

                # Set stylesheet for each item in the QListWidget
                item_style = "QListWidget:item { padding: 7px; background: #212E2E; border: 5px solid #333; }"
                self.image_list.setStyleSheet(item_style)
                self.image_label.hide()
                if (
                    not self.scrollbar_added
                    and self.image_list.count() >= self.max_files_threshold
                ):
                    self.add_scrollbar_to_list()

                self.total_files_label.show()
                self.convert_button.show()
                self.total_files_label.setText(
                    f"Total Files: {self.image_list.count()}"
                )
                self.resize(900, 600)
        event.acceptProposedAction()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())