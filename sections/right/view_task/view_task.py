from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea
)

class ViewTask(QFrame):
    update_task_signal = pyqtSignal(int)  # Abrir pestaña de editar tarea
    delete_task_signal = pyqtSignal(dict)  # Eliminar tarea

    def __init__(self, task):
        super().__init__()
        self._create_sections(task)
        self.setStyleSheet(open('sections/right/view_task/view_task.css').read())


    def _create_sections(self, task): # Definir elementos
        content = QFrame(self)
        content.setObjectName('content')
        content.setFixedWidth(596)

        info_layout = QVBoxLayout()
        info_layout.setSpacing(20)

        # Crear y asignar título
        title_label = QLabel(task['title'])
        title_label.setObjectName("title_label")
        info_layout.addWidget(title_label)

        # Crear y asignar descripción
        description_label = QLabel(f'Descripción:\n{task["description"]}')
        description_label.setObjectName("description_label")
        description_label.setWordWrap(True)
        scroll_area = QScrollArea()
        scroll_area.setWidget(description_label)
        scroll_area.setWidgetResizable(True)
        info_layout.addWidget(scroll_area)

        # Crear y asignar estado
        state_label = QLabel(f'Estado:\n{task["state"]}')
        state_label.setObjectName("state_label")
        info_layout.addWidget(state_label)

        # Botones de acción
        actions_layout = QHBoxLayout() 
        actions_layout.setSpacing(15)

        # Actualizar
        update_button = QPushButton('Actualizar')
        update_button.setObjectName('update_button')
        update_button.clicked.connect(lambda: self._update_task(task))
        actions_layout.addWidget(update_button)

        # Eliminar
        delete_button = QPushButton('Eliminar')
        delete_button.setObjectName('delete_button')
        delete_button.clicked.connect(lambda: self._delete_task(task))
        actions_layout.addWidget(delete_button)

        # Unir elementos
        info_layout.addLayout(actions_layout)
        content.setLayout(info_layout)


    def _update_task(self, task):  # Mostrar formulario de actualizar tarea
        self.update_task_signal.emit(task['id'])


    def _delete_task(self, task): # Eliminar tarea
        task_for_delete = {
            "action": 'delete',
            "task": task
        }
        self.delete_task_signal.emit(task_for_delete)
