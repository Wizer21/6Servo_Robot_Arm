from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from evdev import*

class controller_settings(QDialog):
    def __init__(self, new_parent, xbox_controller):
        QDialog.__init__(self, parent = new_parent)
        self.parent = new_parent
        self.xbox_class = xbox_controller
        self.devices_dict = {}

        # WIDGETS
        self.layout_main = QGridLayout(self)
        self.label_title = QLabel("Controller", self)
        self.label_current = QLabel("Current", self)

        self.label_display_current_controller = QLabel(self)

        self.label_avaible = QLabel("Avaible", self)
        self.area_list = QScrollArea(self)
        self.widget_area = QWidget(self)
        self.layout_area = QVBoxLayout(self)

        self.build()
        self.fill_devices_list()

    def build(self):
        self.setLayout(self.layout_main)
        self.layout_main.addWidget(self.label_title, 0, 0)
        self.layout_main.addWidget(self.label_current, 1, 0)
        self.layout_main.addWidget(self.label_display_current_controller, 2, 0)
        self.layout_main.addWidget(self.label_avaible, 3, 0)
        self.layout_main.addWidget(self.area_list, 4, 0)

        # SETTINGS
        self.area_list.setWidgetResizable(True)
        self.area_list.setWidget(self.widget_area)
        self.widget_area.setLayout(self.layout_area)
        self.layout_area.setAlignment(Qt.AlignTop)

    def fill_devices_list(self):
        devices_list = [InputDevice(path) for path in list_devices()]
        self.devices_dict.clear()

        for device in devices_list:
            self.devices_dict[device.name] = device.path
            button = QPushButton(device.name, self)
            
            self.layout_area.addWidget(button)
            button.clicked.connect(self.set_new_device)
            button.setCursor(Qt.PointingHandCursor)

    def set_new_device(self):
        text = self.sender().text()

        self.label_display_current_controller.setText(text)
        self.xbox_class.new_device(self.devices_dict[text])
        self.parent.update_controller(text)

