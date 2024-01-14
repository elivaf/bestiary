from PySide6.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QWidget, QPushButton, QLineEdit, QListWidget, QListWidgetItem, QInputDialog, QHBoxLayout
from PySide6.QtCore import Qt
from app.controllers import NoteController

class MainWindow(QWidget):
    def __init__(self, note_controller):
        super().__init__()

        self.note_controller = note_controller

        self.setWindowTitle("Ваше приложение")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout(self)

        self.notes_list_widget = QListWidget(self)
        self.layout.addWidget(self.notes_list_widget)
        self.notes_list_widget.itemClicked.connect(self.handle_note_click)

        self.title_input = QLineEdit(self)
        self.layout.addWidget(self.title_input)

        self.content_input = QLineEdit(self)
        self.layout.addWidget(self.content_input)

        self.add_note_button = QPushButton("Добавить заметку", self)
        self.layout.addWidget(self.add_note_button)
        self.add_note_button.clicked.connect(self.add_note)

        self.load_notes()

    def load_notes(self):
        self.notes_list_widget.clear()

        notes = self.note_controller.get_all_notes()

        for note in notes:
            item = QListWidgetItem(note.title)
            item.setData(Qt.UserRole, note)
            self.notes_list_widget.addItem(item)

    def handle_note_click(self, item):
        selected_note = item.data(Qt.UserRole)
        self.title_input.setText(selected_note.title)
        self.content_input.setText(selected_note.content)

    def add_note(self):
        title = self.title_input.text()
        content = self.content_input.text()

        category = None

        new_note = self.note_controller.add_note(title, content, category)

        self.title_input.clear()
        self.content_input.clear()

        self.load_notes()

if __name__ == "__main__":
    app = QApplication([])

    note_controller = NoteController()

    main_window = MainWindow(note_controller)
    main_window.show()

    app.exec()
