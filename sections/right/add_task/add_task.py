import json
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QFrame, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
)

class AddTask(QFrame):
    add_task_signal = pyqtSignal(dict)


    def __init__(self):
        super().__init__()
        self._create_sections()
        self.setStyleSheet(open('sections/right/add_task/add_task.css').read())


    def _create_sections(self):   # Definir elementos
        content = QFrame(self)
        content.setObjectName('content')
        content.setFixedWidth(596)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(7)

        title = QLabel('Agregar tarea')
        title.setObjectName("title")
        info_layout.addWidget(title)

        # Título 
        title_label = QLabel('Título:')
        title_label.setObjectName("title_label")
        info_layout.addWidget(title_label)
        self.title_input = QLineEdit()
        self.title_input.setObjectName("title_input")
        info_layout.addWidget(self.title_input)

        # Descripción
        description_label = QLabel('Descripción:')
        description_label.setObjectName("description_label")
        info_layout.addWidget(description_label)
        self.description_input = QLineEdit()
        self.description_input.setObjectName("description_input")
        info_layout.addWidget(self.description_input)

        # Botón de agregar
        add_button = QPushButton('Agregar')
        add_button.clicked.connect(self._add_task)
        info_layout.addWidget(add_button)

        content.setLayout(info_layout)


    def _add_task(self):  # Submit de agregar nueva tarea
        title = self.title_input.text()
        description = self.description_input.text()

        if not title or not description:
            QMessageBox.warning(self, 'Error', 'Por favor ingrese datos válidos')
        elif len(title) > 20:
            QMessageBox.warning(self, 'Error', 'El título no debe exceder los 20 caracteres')
        else:
            try:
                with open("tasks.json", "r") as json_file:
                    tasks = json.load(json_file)
                new_task = {
                    "action": 'add',
                    "task": {
                        "id": tasks[-1]['id'] + 1,
                        "title": title,
                        "description": description,
                        "state": 'Pendiente'
                    }
                }
                self.add_task_signal.emit(new_task)
            except Exception as e:
                QMessageBox.warning(self, 'Error', f"Error: {e}")
