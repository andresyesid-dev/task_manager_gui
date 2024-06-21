from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QFrame, QLabel, QLineEdit, QCheckBox, QPushButton, QVBoxLayout, QMessageBox
)

class EditTask(QFrame):
    update_task_signal = pyqtSignal(dict)


    def __init__(self, task):
        super().__init__()
        self._create_sections(task)
        self.setStyleSheet(open('sections/right/edit_task/edit_task.css').read())


    def _create_sections(self, task):  # Definir elementos
        content = QFrame(self)
        content.setObjectName('content')
        content.setFixedWidth(596)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(7)

        title = QLabel('Actualizar tarea')
        title.setObjectName("title")
        info_layout.addWidget(title)

        # Título
        title_label = QLabel('Título:')
        title_label.setObjectName("title_label")
        info_layout.addWidget(title_label)
        self.title_input = QLineEdit(task['title'])
        self.title_input.setObjectName("title_input")
        info_layout.addWidget(self.title_input)

        # Descripción
        description_label = QLabel('Descripción:')
        description_label.setObjectName("description_label")
        info_layout.addWidget(description_label)
        self.description_input = QLineEdit(task['description'])
        self.description_input.setObjectName("description_input")
        info_layout.addWidget(self.description_input)

        # Estado de tarea
        self.state_input = QCheckBox('Tarea Finalizada')
        self.state_input.setChecked(task['state'] == 'Finalizada')
        self.state_input.setObjectName("state_check_box")
        info_layout.addWidget(self.state_input)

        # Botón de actualización
        update_button = QPushButton('Actualizar')
        update_button.clicked.connect(lambda: self._update_task(task))
        info_layout.addWidget(update_button)

        content.setLayout(info_layout)


    def _update_task(self, task):  # Submit de actualizar tarea
        title = self.title_input.text()
        description = self.description_input.text()

        if not title or not description:
            QMessageBox.warning(self, 'Error', 'Por favor ingrese datos válidos')
        elif len(title) > 20:
            QMessageBox.warning(self, 'Error', 'El título no debe exceder los 20 caracteres')
        else:
            state = 'Finalizada' if self.state_input.isChecked() else 'Pendiente'
            new_task = {
                "action": 'update',
                "task": {
                    "id": task['id'],
                    "title": title,
                    "description": description,
                    "state": state
                }
            }
            self.update_task_signal.emit(new_task)

