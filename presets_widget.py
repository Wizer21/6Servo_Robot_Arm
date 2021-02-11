from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import json
from utils import *

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
        self.lineedit_preset_name = QLineEdit("None", self)
        self.button_play = QPushButton("Play", self)
        self.button_trash = QPushButton("Delete", self)

        self.scroll_area_positions_list = QScrollArea(self)
        self.widget_area_position = QWidget(self)
        self.layout_area_position = QVBoxLayout(self)

        self.label_current_position = QLabel("000/000/000/000/000/000", self)
        self.button_add = QPushButton("Add", self)

        self.build()
        self.load_presets()
        self.build_presets_list()
        
        for key in self.json_file:
            self.opened_preset = key
            self.load_a_preset()
            self.lineedit_preset_name.setText(key)
            break


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

        utils.resize_and_font(self.label_presets_title, 1.5)

        utils.set_icon_resized(self.button_play, "play", 1)
        utils.set_icon_resized(self.button_trash, "trash", 1)
        utils.set_icon_resized(self.button_add, "corner-arrow", 1)

        utils.style_click_button(self.button_play, "#388e3c")
        utils.style_click_button(self.button_trash, "#d32f2f")
        utils.style_click_button(self.button_add, "#6a1b9a")
        utils.style_click_button(self.button_new_perset, "#ffa000")

        self.lineedit_preset_name.setStyleSheet("border: 0px solid white; font-size: {0}px;".format(str(int(utils.get_resolution()[0] * 0.015))))

        # CONNECTIONS
        self.button_add.clicked.connect(self.push_position)
        self.button_play.clicked.connect(self.play_sequence)
        self.lineedit_preset_name.editingFinished.connect(self.update_preset_name)
        self.button_new_perset.clicked.connect(self.new_preset_clicked)
        self.button_trash.clicked.connect(self.delete_opened_preset)

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
        self.clear_layout(self.layout_area)

        for preset in self.json_file:
            widget = QWidget(self)
            layout = QGridLayout(self)
            label = QLabel(preset, self)
            button_play = QPushButton("Play", self)
            button_trash = QPushButton("Delete", self)
            button_open = QPushButton(self)

            widget.setLayout(layout)
            layout.addWidget(label, 0, 0)
            layout.addWidget(button_play, 0, 1)
            layout.addWidget(button_trash, 0, 2)
            layout.addWidget(button_open, 0, 3)
            self.layout_area.addWidget(widget)

            layout.setColumnStretch(0, 1)
            button_play.setObjectName(preset)
            button_trash.setObjectName(preset)
            button_open.setObjectName(preset)
            button_play.clicked.connect(self.play_preset_from_list)
            button_open.clicked.connect(self.preset_clicked)
            button_trash.clicked.connect(self.delete_preset_from_list)

            utils.set_icon_resized(button_play, "run", 1)
            utils.set_icon_resized(button_trash, "trash", 1)
            utils.set_icon_resized(button_open, "right", 1)
            utils.style_click_button(button_play, "#388e3c")
            utils.style_click_button(button_trash, "#d32f2f")
            utils.style_click_button(button_open, "#0288d1")
            utils.set_icon_resized(button_play, "play", 1)

    def preset_clicked(self):
        self.opened_preset = self.sender().objectName()
        self.lineedit_preset_name.setText(self.opened_preset)
        self.load_a_preset()

    def load_a_preset(self):
        self.opened_size_list = 0
        self.clear_layout(self.layout_area_position)

        positions_list = self.json_file[self.opened_preset]
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
        layout = QGridLayout(self)

        pos_line = QLabel(str(self.opened_size_list + 1))
        label = QLabel(text, self)
        button_play = QPushButton("Go to", self)
        button_trash = QPushButton("Erase", self)

        button_play.setObjectName(str(self.opened_size_list))
        button_trash.setObjectName(str(self.opened_size_list))
        button_play.clicked.connect(self.play_position)
        button_trash.clicked.connect(self.delete_position)

        layout.addWidget(pos_line, 0, 0)
        layout.addWidget(label, 0, 1)
        layout.addWidget(button_play, 0, 2)
        layout.addWidget(button_trash, 0, 3)
        self.layout_area_position.addLayout(layout)

        layout.setColumnStretch(1, 1)

        utils.set_icon_resized(button_play, "run", 1)
        utils.set_icon_resized(button_trash, "eraser", 1)
        utils.style_click_button(button_play, "#283593")
        utils.style_click_button(button_trash, "#d32f2f")
        pos_line.setStyleSheet("color: white; background-color: #474747; font-size: {0}px; padding: {1}px; margin: 0px".format(str(int(utils.get_resolution()[0] * 0.007)), str(int(utils.get_resolution()[0] * 0.009))))

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

    def play_position(self):
        self.player.play_new_sequence([self.json_file[self.opened_preset][int(self.sender().objectName())]])

    def play_sequence(self):
        self.player.play_new_sequence(self.json_file[self.opened_preset])

    def delete_position(self):
        self.json_file[self.opened_preset].pop(int(self.sender().objectName()))
        self.load_a_preset()

    def update_preset_name(self):
        new_name = self.sender().text()

        if not new_name in self.json_file:
            self.json_file[new_name] = self.json_file.pop(self.opened_preset)
            self.opened_preset = new_name
            
            self.build_presets_list()
            
    def new_preset_clicked(self):
        id = 1
        while True:
            if not "New(" + str(id) + ")" in self.json_file:
                self.opened_preset = "New(" + str(id) + ")"
                break
            else:
                id += 1
        
        self.json_file[self.opened_preset] = []        
        self.build_presets_list()
        self.lineedit_preset_name.setText(self.opened_preset)
        self.load_a_preset()

    def play_preset_from_list(self):
        self.player.play_new_sequence(self.json_file[self.sender().objectName()])

    def delete_preset_from_list(self):
        self.delete_profile(self.sender().objectName())

    def delete_opened_preset(self):
        self.delete_profile(self.opened_preset)

    def delete_profile(self, profile):  
        self.json_file.pop(profile)
        self.build_presets_list()

        if profile == self.opened_preset:
            if len(self.json_file) != 0:
                for i in self.json_file:
                    self.opened_preset = i
                    self.load_a_preset()
                    self.lineedit_preset_name.setText(self.opened_preset)
                    return
            else:
                self.new_preset_clicked()