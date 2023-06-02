#!/home/khuzaima/Public/pyqt6-webp-file-converter/venv/bin/python3
import pytest
import main
from main import ImageLabel, MainWindow
from PyQt6.QtCore import Qt, QMimeData,QUrl
from PyQt6.QtGui import QPixmap, QDragEnterEvent, QDropEvent, QIcon, QPainter, QFont


@pytest.fixture
def app(qtbot):
    main_window = MainWindow()
    main_window.show()
    qtbot.addWidget(main_window)
    
    yield main_window, qtbot

def test_drop_event(app):
    main_window, qtbot = app

    # Simulate a drop event by sending a key event
    file_path = "static/img/cloud.png"
    mime_data = QMimeData()
    mime_data.setUrls([QUrl.fromLocalFile(file_path)])
    
    modifier = Qt.KeyboardModifier.ShiftModifier | Qt.KeyboardModifier.ControlModifier
    qtbot.keyPress(main_window, Qt.Key.Key_Space, modifier, delay=-1)
  
    assert main_window.width() == 900
    assert main_window.height() == 600

   
def test_image_label(app):
    main_window, qtbot = app
    
    image_label = ImageLabel()
    main_window.layout().addWidget(image_label)

    file_path = "static/img/cloud.png"
    image_label.set_image(file_path)
    assert not image_label.pixmap().toImage().isNull()

def test_convert_button(app):
    main_window, qtbot = app

    main_window.convert_button.click()
    assert main_window.go_back_button.isVisible()
    main_window.image_label.hide()
    assert not main_window.image_label.isVisible()

def test_go_back_button(app):
    main_window, qtbot = app
    main_window.go_back_button.click()
    assert main_window.image_list.isHidden()
    assert not main_window.image_label.isHidden()

def test_save_files(app):
    main_window, qtbot = app

    main_window.save_files.click()
    assert main_window.saved_files_successfully.isVisible()
    main_window.image_label.hide()
    main_window.save_files.hide()
    main_window.saved_files_successfully.hide()
    assert not main_window.saved_files_successfully.isVisible()

if __name__ == "__main__":
    pytest.main([__file__])
