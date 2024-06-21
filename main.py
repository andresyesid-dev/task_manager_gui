import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QDesktopWidget, QHBoxLayout
)
#Diferentes vistas de la aplicación
from sections.left.menu_left import LeftFrame #Menu izquierdo
from sections.right.view_task.view_task import ViewTask #Datos de la tarea seleccionada
from sections.right.add_task.add_task import AddTask #Formulario de agregar tarea
from sections.right.edit_task.edit_task import EditTask #Formulario de actualizar tarea

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initialize_ui()
        self.setStyleSheet(open('main.css').read())
    

    def initialize_ui(self):
        self.setWindowTitle("Gestor de Tareas")
        self.setFixedSize(900, 550)
        self.center_window()
        self.get_data()
        self.create_sections()  # Estructura de la página


    def center_window(self): # Centrar ventana al escritorio
        screen_geometry = QDesktopWidget().screenGeometry() 
        x = (screen_geometry.width() - self.width()) // 2 
        self.move(x, 100)
    

    def get_data(self):  # Obtener JSON del listado de tareas
        with open("tasks.json", "r") as json_file:
            self.tasks = json.load(json_file)
    

    def create_sections(self):
        # Agregar el menú izquierdo
        self.left_frame = LeftFrame(self.tasks)
        self.left_frame.item_clicked_signal.connect(self.show_task)
        self.left_frame.add_task_signal.connect(self.show_add_task)

        # Agregar en la sección derecha la visualización de la tarea seleccionada
        self.right_frame = ViewTask(self.tasks[0])
        self.right_frame.update_task_signal.connect(self.show_update_task)
        self.right_frame.delete_task_signal.connect(self.actions_tasks)

        # División de la sección derecha e izquierda
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.left_frame)
        self.main_layout.addWidget(self.right_frame)

        # Agregar los cambios al widget principal
        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)
    

    def show_add_task(self):  # Mostrar formulario de agregar tarea
        self.main_layout.removeWidget(self.right_frame)
        self.right_frame = AddTask()
        self.right_frame.add_task_signal.connect(self.actions_tasks)
        self.main_layout.addWidget(self.right_frame)


    def show_update_task(self, index):  # Mostrar formulario de actualizar tarea
        self.main_layout.removeWidget(self.right_frame)
        self.right_frame = EditTask(self.tasks[index])
        self.right_frame.update_task_signal.connect(self.actions_tasks)
        self.main_layout.addWidget(self.right_frame)


    def show_task(self, index):  # Mostrar datos de tarea seleccionada
        self.main_layout.removeWidget(self.right_frame)
        self.right_frame = ViewTask(self.tasks[index])
        self.right_frame.update_task_signal.connect(self.show_update_task)
        self.right_frame.delete_task_signal.connect(self.actions_tasks)
        self.main_layout.addWidget(self.right_frame)
    

    def actions_tasks(self, json_object):  # Las 3 funciones principales (Agregar, Actualizar, Eliminar)
        action = json_object['action']  # Función a realizar
        task = json_object['task']

        if action == 'add':  # Agregar
            self.tasks.append(task)
            with open("tasks.json", "w") as json_file:  # Se actualizan las tareas con los nuevos cambios
                json.dump(self.tasks, json_file, indent=4)
            self.left_frame.update_content(self.tasks)  # Se actualiza la lista del menú izquierdo
            self.show_task(task['id'])  # Mostrar datos de tarea que se agregó o actualizó
    
        elif action == 'update':  # Actualizar
            self.tasks[task['id']] = task
            with open("tasks.json", "w") as json_file:
                json.dump(self.tasks, json_file, indent=4)
            
            self.left_frame.update_content(self.tasks)
            self.show_task(task['id'])


        elif action == 'delete': #Eliminar
            for tarea in self.tasks:
                if tarea["id"] == task['id']:
                    self.tasks.remove(tarea)
                    break
            with open("tasks.json", "w") as json_file:
                json.dump(self.tasks, json_file, indent=4)
            
            self.left_frame.update_content(self.tasks)
            self.left_frame.list_widget.setCurrentRow(0)
            self.show_task(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec())
