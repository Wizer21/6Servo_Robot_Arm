from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from thread_axes import*
from presets_widget import *
from servo_player import *
from controller_settings import *
from servo_thread import*
from xbox_controller import*
from time import sleep
import os
import math

class main_gui(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.pi = pigpio.pi()
        self.controller = xbox_controller(self)
        self.controller_window = controller_settings(self, self.controller)
        self.arm_chord = [[0, 0], [0, 0]]
        self.is_second_part_lower = False
        self.is_first_part_frontward = True
        self.second_part_front = True
        self.heatTimer = QTimer()

        # WIDGETS
        self.bar = QMenuBar(self)
        self.menu_more = QMenu("More", self)
        self.action_controller_settings = QAction("Controller", self)

        self.widget_central = QWidget(self)
        self.layout_main = QGridLayout(self)
        self.layout_header = QGridLayout(self)
        self.label_claw = QLabel(self)
        self.label_title = QLabel("Arm Controller", self)

        self.layout_right_header = QGridLayout(self)
        self.label_raspberry = QLabel(self)
        self.label_heat = QLabel("0°", self)
        self.label_controller = QLabel("controler icon", self)
        self.label_controller_name = QLabel("none", self)

        self.scene_arm_profile = QGraphicsScene(self)
        self.graphic_view_arm = QGraphicsView(self.scene_arm_profile, self)
        
        # SETUP SERVO THREADS
        pi = pigpio.pi()
        self.servo_0 = servo_thread(self, pi, 0, [500, 2500]) # MORE IS LEFT
        self.servo_1 = servo_thread(self, pi, 1, [500, 2250]) # MORE IS DOWN
        self.servo_2 = servo_thread(self, pi, 2, [500, 2220]) # MORE IS DOWN
        self.servo_3 = servo_thread(self, pi, 3, [500, 2500]) # MORE IS UP
        self.servo_4 = servo_thread(self, pi, 4, [500, 2500]) # MORE IS RIGHT
        self.servo_5 = servo_thread(self, pi, 5, [1300, 2500]) # MORE IS WIDER
        self.thread_y = thread_axes(self, self.servo_1, self.servo_2, False)
        self.thread_x = thread_axes(self, self.servo_1, self.servo_2, True)
        self.player = servo_player(self, self.servo_0, self.servo_1, self.servo_2, self.servo_3, self.servo_4, self.servo_5)

        self.widget_profiles = presets_widget(self, self.player)

        utils.window_resize_on_rez(self, 0.6, 0.6)
        self.build()
        self.update_heat()
        self.connections()
        self.ini_servo()
        self.draw_profile()
        self.controller.load_last_controller()

    def connections(self):
        # CONNECTIONS
        # CONTROLLER CONNECTION
        self.controller.messager.claw_move.connect(self.move_claw)
        self.controller.messager.claw_stop.connect(self.stop_claw)
        self.controller.messager.claw_rotation.connect(self.rotate_claw)
        self.controller.messager.claw_rotation_stop.connect(self.stop_claw_rotation)
        self.controller.messager.claw_y_move.connect(self.move_y_claw)
        self.controller.messager.claw_y_stop.connect(self.stop_y_claw)
        self.controller.messager.robot_rotation.connect(self.rotation_robot)
        self.controller.messager.robot_rotation_stop.connect(self.stop_rotation_robot)
        self.controller.messager.move_y.connect(self.move_y_axis)
        self.controller.messager.stop_y.connect(self.stop_y_axis)
        self.controller.messager.move_x.connect(self.move_x_axis)
        self.controller.messager.stop_x.connect(self.stop_x_axis)
        self.controller.messager.push_position.connect(self.call_push_position)

        # UPDATE DISPLAYED POSITION
        self.servo_0.messager.update_displayed_pos.connect(self.update_position)
        self.servo_1.messager.update_displayed_pos.connect(self.update_position)
        self.servo_2.messager.update_displayed_pos.connect(self.update_position)
        self.servo_3.messager.update_displayed_pos.connect(self.update_position)
        self.servo_4.messager.update_displayed_pos.connect(self.update_position)
        self.servo_5.messager.update_displayed_pos.connect(self.update_position)

        # HEAT CONTROL
        self.heatTimer.timeout.connect(self.update_heat)

        # MENU BAR
        self.action_controller_settings.triggered.connect(self.open_controller)

    def build(self):
        self.setCentralWidget(self.widget_central)
        self.widget_central.setLayout(self.layout_main)

        self.setMenuBar(self.bar)
        self.bar.addMenu(self.menu_more)
        self.menu_more.addAction(self.action_controller_settings)

        # HEADER
        self.layout_main.addLayout(self.layout_header, 0, 0)
        self.layout_header.addWidget(self.label_claw, 0, 0)
        self.layout_header.addWidget(self.label_title, 0, 1)
        self.layout_header.addWidget(self.graphic_view_arm, 1, 0, 1, 2)

        self.layout_header.addLayout(self.layout_right_header, 0, 2, 2, 1)
        self.layout_right_header.addWidget(self.label_heat, 0, 0)
        self.layout_right_header.addWidget(self.label_raspberry, 0, 1)
        self.layout_right_header.addWidget(self.label_controller_name, 1, 0)
        self.layout_right_header.addWidget(self.label_controller, 1, 1)

        self.layout_main.addWidget(self.widget_profiles, 1, 0)

        # CUSTOM
        utils.resize_and_font(self.label_title, 2.5)
        self.layout_header.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.layout_right_header.setAlignment(Qt.AlignRight)

        self.layout_header.setColumnStretch(0, 0)
        self.layout_header.setColumnStretch(1, 0)
        self.layout_header.setColumnStretch(2, 1)

        self.label_claw.setPixmap(utils.get_resized_pixmap("arm", 0.5))
        self.label_raspberry.setPixmap(utils.get_resized_pixmap("pi", 0.5))
        self.label_controller.setPixmap(utils.get_resized_pixmap("controller", 0.5))


    def ini_servo(self): 
        self.servo_0.quick_movement(1500)
        self.servo_1.quick_movement(1700)
        self.servo_2.quick_movement(1712)
        self.servo_3.quick_movement(1300)
        self.servo_4.quick_movement(1500)
        self.servo_5.quick_movement(1500)


    def update_heat(self):
        output = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
        val = output[5:].replace("C", "")
        val = val.replace("/n", "")
        val = val.replace("'", "")
        val = float(val[:-1])

        output = output.replace("'", "")
        output = output.replace("\n", "")
        output += "°"
        
        self.label_heat.setText(output[5:])
        if val >= 75:
            utils.resize_and_color_font(self.label_heat, 2, "#d32f2f")
        else:            
            utils.resize_and_color_font(self.label_heat, 2, "white")
            
        self.heatTimer.start(1000)

    def closeEvent(self, event):
        self.servo_0.servo_running = False
        self.servo_1.servo_running = False
        self.servo_2.servo_running = False
        self.servo_3.servo_running = False
        self.servo_4.servo_running = False
        self.servo_5.servo_running = False

        self.servo_0.quick_movement(1500)
        self.servo_1.quick_movement(1800)
        self.servo_2.quick_movement(1900)
        self.servo_3.quick_movement(800)
        self.servo_4.quick_movement(1500)
        self.servo_5.quick_movement(1300)
        sleep(1)

        self.servo_0.cancel()
        self.servo_1.cancel()
        self.servo_2.cancel()
        self.servo_3.cancel()
        self.servo_4.cancel()
        self.servo_5.cancel()

        self.widget_profiles.save_presets()
        self.controller.save_controller()

    # XBOX CONTROLLER MOVEMENTS
    def move_claw(self, action):
        self.servo_5.movement(action)
    
    def stop_claw(self):
        self.servo_5.servo_running = False
        self.calc_arm_position()

    def rotate_claw(self, action):
        self.servo_4.movement(action)
    
    def stop_claw_rotation(self):
        self.servo_4.servo_running = False
        self.calc_arm_position()

    def move_y_claw(self, action):
        self.servo_3.movement(action)

    def stop_y_claw(self):
        self.servo_3.servo_running = False
        self.calc_arm_position()

    def rotation_robot(self, action):
        self.servo_0.movement(action)

    def stop_rotation_robot(self):
        self.servo_0.servo_running = False
        self.calc_arm_position()

    def move_y_axis(self, action):
        self.thread_y.call_movement(action / 300)

    def stop_y_axis(self):
        self.thread_y.run_movement = False

    def move_x_axis(self, action):
        self.thread_x.call_movement(action / 300)

    def stop_x_axis(self):
        self.thread_x.run_movement = False

    def calc_arm_position(self):
        pi_rad = math.pi / 180

        # TRIANGLE 1: X
        width_1 = self.servo_1.servo_position
        first_degrees = 180 - (width_1 - 500) / 9.722222

        if first_degrees != 90:
            if first_degrees > 90: 
                is_first_part_frontward = False
                # THE ARM IS BACKWARD
                # TRIANGLE 1: X
                degrees = first_degrees - 90
                rad = degrees * pi_rad
                tri_1_y = math.cos(rad) * 10.5

                # TRIANGLE 1: Y
                third_angle  = 180 - (degrees + 90)
                rad = third_angle * pi_rad
                tri_1_x = math.cos(rad) * 10.5
            else:
                is_first_part_frontward = True
                # THE ARM IS FRONTWARD
                rad = first_degrees * pi_rad
                tri_1_x = math.cos(rad) * 10.5

                # TRIANGLE 1: Y
                third_angle = 180 - (first_degrees + 90)
                rad = third_angle * pi_rad
                tri_1_y = math.cos(rad) * 10.5       
        else:
            third_angle = 90
            tri_1_y = 10.5
            tri_1_x = 0

        width_2 = self.servo_2.servo_position
        degrees = 180 - (width_2 - 500) / 9.5555555

        back_angle = first_degrees - ((first_degrees - 90) * 2)
        #deg = degrees - 90
        if degrees > back_angle:
            # SECOND PART HIGHT AND BACKWARD
            second_part_front = False            
            is_second_part_lower = False
            degrees -= back_angle

            # TRIANGLE 2: Y
            rad = degrees * pi_rad
            tri_2_y = math.cos(rad) * 10.5

            # TRIANGLE 2: X
            third_angle_tri_2 = 180 - (degrees + 90)
            rad = third_angle_tri_2 * pi_rad
            tri_2_x = math.cos(rad) * 10.5

        elif degrees > 90 - first_degrees or not is_first_part_frontward: 
            # SECOND PART HIGHT AND FRONT
            is_second_part_lower = False
            second_part_front = True
            # TRIANGLE 2: X
            if not is_first_part_frontward:
                rec_degree = degrees + (first_degrees - 90)
            else:
                rec_degree = degrees - (90 - first_degrees)

            rad = rec_degree * pi_rad
            tri_2_x = math.cos(rad) * 10.5
        
            # TRIANGLE 2: Y
            third_angle_tri_2 = 180 - (rec_degree + 90)
            rad = third_angle_tri_2 * pi_rad
            tri_2_y = math.cos(rad) * 10.5
        else: 
            # SECOND PART LOW AND FRONT
            second_part_front = True
            is_second_part_lower = True
            rec_degree = (90 + degrees) - third_angle
            third_angle_tri_2 = 180 - (rec_degree + 90)

            # TRIANGLE 2: X
            rad = third_angle_tri_2 * pi_rad
            tri_2_x = math.cos(rad) * 10.5

            # TRIANGLE 2: Y
            rad = rec_degree * pi_rad
            tri_2_y = math.cos(rad) * 10.5

        if is_first_part_frontward and second_part_front:
            pos1 = round(tri_1_x + tri_2_x, 2)
        elif not is_first_part_frontward and not second_part_front:
            pos1 = round(0 - (tri_2_x + tri_1_x), 2)        
        elif not is_first_part_frontward and second_part_front:
            pos1 = round(tri_2_x - tri_1_x, 2)

        if is_second_part_lower:
            pos2 = round(tri_1_y - tri_2_y, 2)
        else:
            pos2 = round(tri_1_y + tri_2_y, 2)
            
        self.arm_chord = [[tri_1_x, tri_1_y], [pos1, pos2]]

        utils.set_position("elbow_pos", [tri_1_x, tri_1_y])
        utils.set_position("claw_pos", [pos1, pos2])
        self.draw_profile()

    def draw_profile(self):
        size = 4
        part = round(size / 5)        
        centimeter_in_pixels = round((part * 3) / 21)
        servo1 = [round(self.arm_chord[0][0] * centimeter_in_pixels), round(self.arm_chord[0][1] * centimeter_in_pixels)]
        claw = [round(self.arm_chord[1][0] * centimeter_in_pixels), round(self.arm_chord[1][1] * centimeter_in_pixels)]
 
        pen = QPen()
        pen.setCapStyle(Qt.RoundCap)
        pen.setWidth(round(size / 30))

        self.scene_arm_profile.clear()

        # DRAW GROUND
        pen.setColor(QColor("#9e9e9e"))
        #self.scene_arm_profile.addLine(0, part, size, part, pen)

        # DRAW ARM
        #pen.setColor(QColor("#e53935"))
        #painter.setPen(pen)
        #painter.drawLine(part, part, part + servo1[0], part + servo1[1])
        #painter.drawLine(part + servo1[0], part + servo1[1], part + claw[0], part + claw[1])

        # DRAW MOTORS
        #pen.setColor(QColor("#000000"))
        #painter.setPen(pen)
        #painter.drawPoint(part, part)
        #painter.drawPoint(part + servo1[0], part + servo1[1])
        #painter.drawPoint(part + claw[0], part + claw[1])

        #pix.mirrored(False, True)
        #self.graphic_view_arm.setPixmap(self.pix, 200, 200) 
        #painter.end()  

    def update_position(self, id_servo, pos):
        self.widget_profiles.update_pos(id_servo, pos)

    def call_push_position(self):
        self.widget_profiles.push_position()

    def open_controller(self):
        self.controller_window.exec()

    def update_controller(self, controller_name):
        self.label_controller_name.setText(controller_name)
