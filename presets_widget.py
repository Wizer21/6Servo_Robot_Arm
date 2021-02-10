from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import json

class presets_widget(QWidget):
    def __init__(self, parent, new_player):
        QWidget.__init__(self, parent)
        self.json_file = {}
        self.servo_positions = [0, 0, 0, 0, 0, 0]
        self.opened_preset = "Default"
        self.player = new_player
        self.opened_size_list = 0

        self.layout_main = QGridLayout(self)

        # PRESETS LIST
        self.layout_list = QGridLayout(self)
        self.label_presets_title = QLabel("Presets", self)
        self.button_new_perset = QPushButton("New", self)
        
        self.scroll_presets_list = QScrollArea(self)
        self.widget_area = QWidget(self)
        self.layout_area = QVBoxLayout(self)

        # PRESET DETAILS
        self.layout_detail = QGridLayout(self)
        self.lineedit_preset_name = QLineEdit("Profile Name", self)
        self.button_play = QPushButton("Play", self)
        self.button_trash = QPushButton("Trash", self)

        self.scroll_area_positions_list = QScrollArea(self)
        self.widget_area_position = QWidget(self)
        self.layout_area_position = QVBoxLayout(self)

        self.label_current_position = QLabel("000/000/000/000/000/000", self)
        self.button_add = QPushButton("Add", self)

        self.build()
        self.load_presets()
        self.build_presets_list()

    def build(self):
        self.setLayout(self.layout_main)

        # PRESETS LIST
        self.layout_main.addLayout(self.layout_list, 0, 0)

        self.layout_list.addWidget(self.label_presets_title, 0, 0)
        self.layout_list.addWidget(self.button_new_perset, 0, 1)
        self.layout_list.addWidget(self.scroll_presets_list, 1, 0, 1, 2)

        self.scroll_presets_list.setWidget(self.widget_area)
        self.widget_area.setLayout(self.layout_area)

        # PRESET DETAILS
        self.layout_main.addLayout(self.layout_detail, 0, 1, 2, 1)

        self.layout_detail.addWidget(self.lineedit_preset_name, 0, 0, 1, 2)
        self.layout_detail.addWidget(self.button_play, 1, 0)
        self.layout_detail.addWidget(self.button_trash, 1, 1)
        self.layout_detail.addWidget(self.scroll_area_positions_list, 2, 0, 1, 2)
        self.scroll_area_positions_list.setWidget(self.widget_area_position)
        self.widget_area_position.setLayout(self.layout_area_position)
        self.layout_detail.addWidget(self.label_current_position, 3, 0)
        self.layout_detail.addWidget(self.button_add, 3, 1)

        # PARAMETERS 
        self.scroll_presets_list.setWidgetResizable(True)
        self.scroll_area_positions_list.setWidgetResizable(True)
        self.layout_list.setColumnStretch(0, 1)
        self.layout_list.setColumnStretch(1, 0)
        self.layout_area.setAlignment(Qt.AlignTop)
        self.layout_area_position.setAlignment(Qt.AlignTop)
        self.layout_main.setColumnStretch(0, 1)
        self.layout_main.setColumnStretch(1, 2)

        # CONNECTIONS
        self.button_add.clicked.connect(self.push_position)


    def load_presets(self):
        try:
            with open("./files/presets.json", "r") as presets_file:
                self.json_file = json.load(presets_file)  

        except FileNotFoundError:
            self.json_file = {
                "Default":[
                    [1500, 1700, 1712, 1300, 1500, 1500],
                    [1500, 1700, 1712, 1300, 1400, 1500],
                    [1500, 1700, 1712, 1300, 1600, 1500]
                ]
            }

    def save_presets(self):        
        with open("./files/presets.json", "w") as file:
            json.dump(self.json_file, file)


    def build_presets_list(self):
        for preset in self.json_file:
            widget = QWidget(self)
            layout = QHBoxLayout(self)
            label = QLabel(preset, self)
            button_play = QPushButton("Play", self)
            button_trash = QPushButton("Trash", self)
            button_open = QPushButton("Right arrow", self)

            widget.setLayout(layout)
            layout.addWidget(label)
            layout.addWidget(button_play)
            layout.addWidget(button_trash)
            layout.addWidget(button_open)
            self.layout_area.addWidget(widget)

            button_play.setObjectName(preset)
            button_trash.setObjectName(preset)
            button_open.setObjectName(preset)
            button_open.clicked.connect(self.open_a_preset)

    def open_a_preset(self):
        self.opened_size_list = 0
        self.clear_layout(self.layout_area_position)

        self.opened_preset = self.sender().objectName()
        positions_list = self.json_file[self.sender().objectName()]
        for pos in positions_list:            
            text = ""
            for p in pos:
                text += str(p) + "/"

            self.build_pos_line(text)

    def push_position(self):
        new_pos = []
        text = ""
        for p in self.servo_positions:
            new_pos.append(p)
            text += str(p) + "/"
        
        self.json_file[self.opened_preset].append(new_pos)
        self.build_pos_line(text)

    def build_pos_line(self, text):
        layout = QHBoxLayout(self)
        label = QLabel(text, self)
        button_play = QPushButton("Play", self)
        button_trash = QPushButton("Trash", self)

        button_play.setObjectName(str(self.opened_size_list))
        button_play.clicked.connect(self.play_sequence)

        layout.addWidget(label)
        layout.addWidget(button_play)
        layout.addWidget(button_trash)
        self.layout_area_position.addLayout(layout)

        self.opened_size_list += 1


    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clear_layout(child.layout())


    def update_pos(self, servo_id, position):
        self.servo_positions[servo_id] = position

        text = ""
        for p in self.servo_positions:
            text += str(p) + "/"

        self.label_current_position.setText(text)

    def play_sequence(self):
        self.player.play_new_sequence([self.json_file[self.opened_preset][int(self.sender().objectName())]])