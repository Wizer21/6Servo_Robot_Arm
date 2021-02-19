from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import json
from utils import *
from confirm_button import *

class presets_widget(QWidget):
    def __init__(self, parent, new_player, new_draw_surface):
        QWidget.__init__(self, parent)
        self.json_file = {}
        self.servo_positions = [0, 0, 0, 0, 0, 0]
        self.opened_preset = "Default"
        self.player = new_player
        self.opened_size_list = 0
        self.draw_surface = new_draw_surface
        self.play_parameters = {
            "pause": False,
            "pause_time": 0,
            "reverse": False,
            "loop": False,
            "infinite": False, 
            "loop_times": 2
        }

        self.layout_main = QGridLayout(self)

        # PRESETS LIST
        self.layout_list = QGridLayout(self)
        self.widget_presets_header = QWidget(self)
        self.layout_presets_header = QGridLayout(self)
        self.label_presets_icon = QLabel(self)
        self.label_presets_title = QLabel("Presets", self)

        self.button_new_perset = QPushButton("New", self)
        
        self.scroll_presets_list = QScrollArea(self)
        self.widget_area = QWidget(self)
        self.layout_area = QVBoxLayout(self)

        # PRESET DETAILS
        self.layout_detail = QGridLayout(self)
        self.widget_loaded_header = QWidget(self)
        self.layout_loaded_header = QHBoxLayout(self)
        self.label_loaded_icon = QLabel(self)
        self.lineedit_preset_name = QLineEdit("None", self)

        self.button_play = QPushButton("Play", self)
        self.button_trash = confirm_button(self, "Delete", "trash")

        self.scroll_area_positions_list = QScrollArea(self)
        self.widget_area_position = QWidget(self)
        self.layout_area_position = QVBoxLayout(self)

        self.label_current_position = QLabel("000/000/000/000/000/000", self)
        self.button_add = QPushButton("Add", self)

        # PARAMETERS
        self.layout_parameters = QGridLayout(self)

        self.widget_param_header = QWidget(self)
        self.layout_param_header = QHBoxLayout(self)
        self.label_parameters_icon = QLabel(self)
        self.label_parameters_title = QLabel("Parameters", self)

        self.check_box_pause = QCheckBox("Step Pause", self)
        self.line_edit_pause_time = QLineEdit(str(self.play_parameters["pause_time"]), self)

        self.check_box_reverse_play = QCheckBox("Reverse play", self)
        self.group_box_loop = QGroupBox("Loop", self)
        self.box_layout = QGridLayout(self)
        self.check_box_infinite = QCheckBox("Infinite", self)
        self.check_box_times = QCheckBox(self)
        self.line_edit_loop_number = QLineEdit(str(self.play_parameters["loop_times"]), self)  

        self.button_stop = QPushButton("Stop", self)

        self.build()
        self.load_presets()
        self.build_presets_list()
        self.player.send_parameters(self.play_parameters)
        
        for key in self.json_file:
            self.opened_preset = key
            self.load_a_preset()
            self.lineedit_preset_name.setText(key)
            break


    def build(self):
        self.setLayout(self.layout_main)

        # PRESETS LIST
        self.layout_main.addLayout(self.layout_list, 0, 0)

        self.layout_list.addWidget(self.widget_presets_header, 0, 0)
        self.widget_presets_header.setLayout(self.layout_presets_header)
        self.layout_presets_header.addWidget(self.label_presets_icon, 0, 0)
        self.layout_presets_header.addWidget(self.label_presets_title, 0, 1)
        self.layout_presets_header.addWidget(self.button_new_perset, 0, 2)

        self.layout_list.addWidget(self.scroll_presets_list, 1, 0, 1, 2)

        self.scroll_presets_list.setWidget(self.widget_area)
        self.widget_area.setLayout(self.layout_area)

        # PRESET DETAILS
        self.layout_main.addLayout(self.layout_detail, 0, 1, 2, 1)
        self.layout_detail.addWidget(self.widget_loaded_header, 0, 0, 1, 2)
        self.widget_loaded_header.setLayout(self.layout_loaded_header)
        self.layout_loaded_header.addWidget(self.label_loaded_icon)
        self.layout_loaded_header.addWidget(self.lineedit_preset_name)

        self.layout_detail.addWidget(self.button_play, 1, 0)
        self.layout_detail.addWidget(self.button_trash, 1, 1)
        self.layout_presets_header.setSpacing(15)
        self.layout_detail.addWidget(self.scroll_area_positions_list, 2, 0, 1, 2)
        self.scroll_area_positions_list.setWidget(self.widget_area_position)
        self.widget_area_position.setLayout(self.layout_area_position)
        self.layout_detail.addWidget(self.label_current_position, 3, 0)
        self.layout_detail.addWidget(self.button_add, 3, 1)

        # PARALETERS BUILD
        self.layout_main.addLayout(self.layout_parameters, 1, 0)
        self.layout_parameters.addWidget(self.widget_param_header, 0, 0, 1, 2)
        self.widget_param_header.setLayout(self.layout_param_header)
        self.layout_param_header.addWidget(self.label_parameters_icon)
        self.layout_param_header.addWidget(self.label_parameters_title)

        self.layout_parameters.addWidget(self.check_box_pause, 1, 0)
        self.layout_parameters.addWidget(self.line_edit_pause_time, 1, 1)
        self.layout_parameters.addWidget(self.check_box_reverse_play, 2, 0, 1, 2)

        self.layout_parameters.addWidget(self.group_box_loop, 3, 0, 1, 2)
        self.group_box_loop.setLayout(self.box_layout)
        self.box_layout.addWidget(self.check_box_infinite, 0, 0, 1, 2)
        self.box_layout.addWidget(self.check_box_times, 1, 0)
        self.box_layout.addWidget(self.line_edit_loop_number, 1, 1)

        self.layout_parameters.addWidget(self.button_stop, 4, 0, 1, 2)

        self.layout_parameters.addWidget(self.draw_surface, 0, 2, 4, 1)

        # PARAMETERS 
        self.scroll_presets_list.setWidgetResizable(True)
        self.scroll_area_positions_list.setWidgetResizable(True)
        self.layout_list.setColumnStretch(0, 1)
        self.layout_list.setColumnStretch(1, 0)
        self.layout_area.setAlignment(Qt.AlignTop)
        self.layout_area_position.setAlignment(Qt.AlignTop)
        self.layout_main.setColumnStretch(0, 1)
        self.layout_main.setColumnStretch(1, 1)
        self.layout_main.setRowStretch(0, 1)
        self.layout_main.setRowStretch(1, 1)

        self.layout_presets_header.setColumnStretch(1, 1)

        #self.layout_presets_header.setContentsMargins(0, 0, 0, 0)
        #self.button_new_perset.setStyleSheet("margin: 16px")
        #self.label_presets_icon.setStyleSheet("padding: 16px")
        #self.button_new_perset.setContextMenuPolicy(QSizePolicy.Expanding)

        #self.layout_param_header.setContentsMargins(0, 0, 0, 0)
        #self.layout_loaded_header.setContentsMargins(0, 0, 0, 0)



        utils.resize_and_font(self.label_presets_title, 1.5)
        self.label_presets_icon.setPixmap(utils.get_resized_pixmap("list", 0.4))
        self.widget_presets_header.setStyleSheet("background-color: #455a64")

        utils.resize_and_font(self.lineedit_preset_name, 1.5)
        self.label_loaded_icon.setPixmap(utils.get_resized_pixmap("line", 0.4))
        self.widget_loaded_header.setStyleSheet("background-color: #455a64")

        utils.set_icon_resized(self.button_play, "play", 1)
        utils.set_icon_resized(self.button_add, "corner-arrow", 1)

        utils.style_click_button(self.button_play, "#388e3c")
        utils.style_click_button(self.button_trash, "#d32f2f")
        utils.style_click_button(self.button_add, "#6a1b9a")
        utils.style_click_button(self.button_new_perset, "#ffa000")

        self.label_parameters_icon.setPixmap(utils.get_resized_pixmap("play_settings", 0.4))
        self.layout_parameters.setColumnStretch(0, 0)
        self.layout_parameters.setColumnStretch(1, 1)
        self.layout_parameters.setColumnStretch(2, 1)
        self.button_play.setCursor(Qt.PointingHandCursor)
        self.button_add.setCursor(Qt.PointingHandCursor)
        self.button_new_perset.setCursor(Qt.PointingHandCursor)
        
        self.widget_param_header.setStyleSheet("background-color: #455a64")
        self.layout_param_header.setAlignment(Qt.AlignLeft)
        utils.resize_and_font(self.label_parameters_title, 1.5)
        self.group_box_loop.setCheckable(True)
        self.group_box_loop.setChecked(False)
        self.check_box_times.setChecked(True)

        utils.resize_and_color_font(self.check_box_pause, 1, "#616161")
        self.line_edit_pause_time.setStyleSheet("border: 0px solid white; color: #616161")
        utils.resize_and_color_font(self.check_box_reverse_play, 1, "#616161")
        self.toggle_loop(False)

        self.check_box_pause.setCursor(Qt.PointingHandCursor)
        self.check_box_reverse_play.setCursor(Qt.PointingHandCursor)
        
        self.check_box_infinite.setCursor(Qt.PointingHandCursor)
        self.check_box_times.setCursor(Qt.PointingHandCursor)
        self.button_stop.setCursor(Qt.PointingHandCursor)

        self.lineedit_preset_name.setStyleSheet("border: 0px solid white; font-size: {0}px;".format(str(int(utils.get_resolution()[0] * 0.015))))

        # CONNECTIONS
        self.button_add.clicked.connect(self.push_position)
        self.button_play.clicked.connect(self.play_sequence)
        self.lineedit_preset_name.editingFinished.connect(self.update_preset_name)
        self.button_new_perset.clicked.connect(self.new_preset_clicked)
        self.button_trash.messager.clicked_valid.connect(self.delete_opened_preset)

        # CONNECTIONS PARAMETERS
        self.check_box_pause.stateChanged.connect(self.pause_state_changed)
        self.line_edit_pause_time.editingFinished.connect(self.set_pause_value)
        self.check_box_reverse_play.stateChanged.connect(self.reverse_state_changed)
        self.group_box_loop.toggled.connect(self.toggle_loop)
        self.check_box_infinite.stateChanged.connect(self.infinite_state_changed)
        self.check_box_times.stateChanged.connect(self.loop_time_state_changed)
        self.line_edit_loop_number.editingFinished.connect(self.set_loop_times)
        self.button_stop.clicked.connect(self.stop_loop)

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
        utils.clear_layout(self.layout_area)

        for preset in self.json_file:
            widget = QWidget(self)
            layout = QGridLayout(self)
            label = QLabel(preset, self)
            button_play = QPushButton("Play", self)
            button_trash = confirm_button(self, "Delete", "trash", preset)
            button_open = QPushButton(self)

            widget.setLayout(layout)
            layout.addWidget(label, 0, 0)
            layout.addWidget(button_play, 0, 1)
            layout.addWidget(button_trash, 0, 2)
            layout.addWidget(button_open, 0, 3)
            self.layout_area.addWidget(widget)

            layout.setColumnStretch(0, 1)
            button_play.setObjectName(preset)
            button_open.setObjectName(preset)
            button_play.clicked.connect(self.play_preset_from_list)
            button_open.clicked.connect(self.preset_clicked)
            button_trash.messager.clicked_valid.connect(self.delete_preset_from_list)

            button_play.setCursor(Qt.PointingHandCursor)
            button_open.setCursor(Qt.PointingHandCursor)

            utils.set_icon_resized(button_play, "run", 1)
            utils.set_icon_resized(button_open, "right", 1)
            utils.style_click_button(button_play, "#388e3c")
            utils.style_click_button(button_open, "#0288d1")
            utils.set_icon_resized(button_play, "play", 1)

    def preset_clicked(self):
        self.opened_preset = self.sender().objectName()
        self.lineedit_preset_name.setText(self.opened_preset)
        self.load_a_preset()

    def load_a_preset(self):
        self.opened_size_list = 0
        utils.clear_layout(self.layout_area_position)

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
        button_trash = confirm_button(self, "Erase", "eraser", str(self.opened_size_list))

        button_play.setObjectName(str(self.opened_size_list))
        button_play.clicked.connect(self.play_position)
        button_trash.messager.clicked_valid.connect(self.delete_position)

        layout.addWidget(pos_line, 0, 0)
        layout.addWidget(label, 0, 1)
        layout.addWidget(button_play, 0, 2)
        layout.addWidget(button_trash, 0, 3)
        self.layout_area_position.addLayout(layout)

        layout.setColumnStretch(1, 1)

        button_play.setCursor(Qt.PointingHandCursor)
        utils.set_icon_resized(button_play, "run", 1)
        utils.style_click_button(button_play, "#283593")
        pos_line.setStyleSheet("color: white; background-color: #474747; font-size: {0}px; padding: 0px; margin: 0px; min-width: {1}px; min-eight: {1}px;".format(str(int(utils.get_resolution()[0] * 0.007)), str(int(utils.get_resolution()[0] * 0.02))))
        pos_line.setAlignment(Qt.AlignCenter)

        self.opened_size_list += 1


    def update_pos(self, servo_id, position):
        self.servo_positions[servo_id] = position

        text = ""
        for p in self.servo_positions:
            text += str(p) + "/"

        self.label_current_position.setText(text)

    def play_position(self):
        self.player.go_to_position([self.json_file[self.opened_preset][int(self.sender().objectName())]])

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

    
    def pause_state_changed(self, state):
        if state == 2:
            self.play_parameters["pause"] = True
            utils.resize_and_color_font(self.sender(), 1, "#ffffff")
            self.line_edit_pause_time.setStyleSheet("border: 0px solid white; color: #ffffff")
        else:
            self.play_parameters["pause"] = False
            utils.resize_and_color_font(self.sender(), 1, "#616161")
            self.line_edit_pause_time.setStyleSheet("border: 0px solid white; color: #616161")

    def set_pause_value(self):
        self.play_parameters["pause_time"] = self.sender().text()

    def reverse_state_changed(self, state):
        if state == 2:
            self.play_parameters["reverse"] = True
            utils.resize_and_color_font(self.sender(), 1, "#ffffff")
        else:
            self.play_parameters["reverse"] = False
            utils.resize_and_color_font(self.sender(), 1, "#616161")
    
    def infinite_state_changed(self, state):
        if state == 2:
            self.play_parameters["infinite"] = True
            self.check_box_times.setChecked(False)
            utils.resize_and_color_font(self.sender(), 1, "#ffffff")
            self.line_edit_loop_number.setStyleSheet("border: 0px solid white; color: #616161")
        else:
            self.play_parameters["infinite"] = False
            self.check_box_times.setChecked(True)
            utils.resize_and_color_font(self.sender(), 1, "#616161")
            self.line_edit_loop_number.setStyleSheet("border: 0px solid white; color: #ffffff")
    
    def loop_time_state_changed(self, state):
        if state == 2:
            self.check_box_infinite.setChecked(False)
        else:
            self.check_box_infinite.setChecked(True)
    
    def set_loop_times(self):
        self.play_parameters["loop_times"] = self.sender().text()

    def stop_loop(self):
        if self.player.running:
            self.player.stop = True

    def toggle_loop(self, state_bool):
        self.play_parameters["loop"] = state_bool
        if not state_bool:
            utils.resize_and_color_font(self.check_box_infinite, 1, "#616161")
            self.line_edit_loop_number.setStyleSheet("border: 0px solid white; color: #616161")
            utils.resize_and_color_font(self.group_box_loop, 1, "#616161")
        else:
            utils.resize_and_color_font(self.group_box_loop, 1, "#ffffff")
            if self.check_box_infinite.isChecked():
                utils.resize_and_color_font(self.check_box_infinite, 1, "#ffffff")
                self.line_edit_loop_number.setStyleSheet("border: 0px solid white; color: #616161")
            else:
                utils.resize_and_color_font(self.check_box_infinite, 1, "#616161")
                self.line_edit_loop_number.setStyleSheet("border: 0px solid white; color: #ffffff")




        