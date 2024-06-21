from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem
)

class LeftFrame(QFrame):
    item_clicked_signal = pyqtSignal(int)  # Señal personalizada para pasar el índice
    add_task_signal = pyqtSignal()  # Mostrar formulario de agregar tarea


    def __init__(self, tasks):
        super().__init__()
        self.setFixedWidth(270)
        self.setObjectName('main_frame')
        self._create_sections(tasks)  # Crear elementos, secciones
        self.setStyleSheet(open('sections/left/menu_left.css').read())


    def _create_sections(self, tasks):
        # Elementos del header
        header_layout = QHBoxLayout()
        titulo = QLabel('Tus tareas')
        titulo.setFixedSize(180, 40)
        agregar = QPushButton('+', objectName="button_add")
        agregar.clicked.connect(self._add_task)
        header_layout.addWidget(titulo)
        header_layout.addWidget(agregar)

        # Lista de tareas
        self.list_widget = QListWidget()
        for i, task in enumerate(tasks):
            item = QListWidgetItem(task['title'])
            self.list_widget.addItem(item)
            item.setData(Qt.UserRole, i)
        self.list_widget.setCurrentRow(0)
        self.list_widget.itemClicked.connect(self._show_task)

        # Unir los elementos
        main_layout = QVBoxLayout()
        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.list_widget)

        self.setLayout(main_layout)


    def _show_task(self, item):  # Mostrar tarea según el Item seleccionado
        index = item.data(Qt.UserRole)
        self.item_clicked_signal.emit(index) 


    def _add_task(self):  # Mostrar formulario de agregar tarea
        self.add_task_signal.emit()  
    

    def update_content(self, new_tasks):  # Actualizar datos de la lista
        self.list_widget.clear()  # Elimina los elementos para volverlos a ingresar actualizados

        for i, task in enumerate(new_tasks):
            item = QListWidgetItem(task['title'])
            self.list_widget.addItem(item)
            item.setData(Qt.UserRole, i)
            