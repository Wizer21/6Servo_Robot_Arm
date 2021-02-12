from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from utils import*

class Communication(QObject):
    clicked_valid = pyqtSignal()

class confirm_button(QPushButton):
    def __init__(self, new_parent, new_text, new_icon, object_name = ""):
        QPushButton.__init__(self, parent = new_parent)
        self.setContentsMargins(10, 10, 10, 10)
        self.setMinimumHeight(int(utils.get_resolution()[0] * 0.023))

        self.setCursor(Qt.PointingHandCursor)
        self.is_waiting_second_click = False
        self.parent = new_parent
        self.messager = Communication()
        self.messager.setObjectName(object_name)

        self.default_text = new_text
        self.default_icon = new_icon

        self.update_appearence()

    def mousePressEvent(self, event):
        if self.is_waiting_second_click:
            self.is_waiting_second_click = False
            self.messager.clicked_valid.emit()     
            self.update_appearence()   
        else:
            self.is_waiting_second_click = True
            self.update_appearence()
    
    def leaveEvent(self, event):
        self.is_waiting_second_click = False
        self.update_appearence()

    def update_appearence(self):
        if self.is_waiting_second_click:
            # Waiting Appareance
            utils.style_click_button(self, "#00838f", 0)
            utils.set_icon_resized(self, self.default_icon, 1)    
            self.setText("Sure ?")    
        else:
            # Default Appareance
            utils.style_click_button(self, "#d32f2f", 0)
            utils.set_icon_resized(self, self.default_icon, 1)
            self.setText(self.default_text)