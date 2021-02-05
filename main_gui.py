from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from servo_thread import*
from time import sleep
from xbox_controller import*
import math

class main_gui(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.pi = pigpio.pi()
        self.controller = xbox_controller()
        self.arm_chord = [[0, 0], [0, 0]]

        # WIDGETS
        self.widget_central = QWidget(self)
        self.layout_main = QGridLayout(self)

        self.button_left = QPushButton("Left", self)
        self.button_right = QPushButton("Right", self)

        self.line_edit_servo_0 = QLineEdit(self)
        self.line_edit_servo_1 = QLineEdit(self)
        self.line_edit_servo_2 = QLineEdit(self)
        self.line_edit_servo_3 = QLineEdit(self)
        self.line_edit_servo_4 = QLineEdit(self)
        self.line_edit_servo_5 = QLineEdit(self)
        self.label_profile_arm = QLabel(self)
        
        # SETUP SERVO THREADS
        pi = pigpio.pi()
        self.servo_0 = servo_thread(self, pi, 1500, 0, [500, 2500]) # MORE IS LEFT
        self.servo_1 = servo_thread(self, pi, 800, 1, [500, 1400]) # MORE IS DOWN
        self.servo_2 = servo_thread(self, pi, 1700, 2, [500, 2500]) # MORE IS DOWN
        self.servo_3 = servo_thread(self, pi, 1000, 3, [500, 2500]) # MORE IS UP
        self.servo_4 = servo_thread(self, pi, 1500, 4, [500, 2500]) # MORE IS RIGHT
        self.servo_5 = servo_thread(self, pi, 1500, 5, [1300, 2500]) # MORE IS WIDER

        self.resize(700, 700)
        self.build()

        # CONNECTIONS
        self.button_left.pressed.connect(self.move_left)
        self.button_left.released.connect(self.stop_0)
        self.button_right.pressed.connect(self.move_right)
        self.button_right.released.connect(self.stop_0)  

        self.line_edit_servo_0.editingFinished.connect(self.update_servo_0)
        self.line_edit_servo_1.editingFinished.connect(self.update_servo_1)
        self.line_edit_servo_2.editingFinished.connect(self.update_servo_2)
        self.line_edit_servo_3.editingFinished.connect(self.update_servo_3)
        self.line_edit_servo_4.editingFinished.connect(self.update_servo_4)
        self.line_edit_servo_5.editingFinished.connect(self.update_servo_5)

        # CONTROLLER CONNECTION
        self.controller.messager.claw_move.connect(self.move_claw)
        self.controller.messager.claw_stop.connect(self.stop_claw)
        self.controller.messager.claw_rotation.connect(self.rotate_claw)
        self.controller.messager.claw_rotation_stop.connect(self.stop_claw_rotation)
        self.controller.messager.claw_y_move.connect(self.move_y_claw)
        self.controller.messager.claw_y_stop.connect(self.stop_y_claw)
        self.controller.messager.robot_rotation.connect(self.rotation_robot)
        self.controller.messager.robot_rotation_stop.connect(self.stop_rotation_robot)
    

    def build(self):
        self.setCentralWidget(self.widget_central)
        self.widget_central.setLayout(self.layout_main)
        self.layout_main.addWidget(self.button_left, 0, 0)
        self.layout_main.addWidget(self.button_right, 0, 1)

        self.layout_main.addWidget(self.line_edit_servo_0, 1, 0)
        self.layout_main.addWidget(self.line_edit_servo_1, 2, 0)
        self.layout_main.addWidget(self.line_edit_servo_2, 3, 0)
        self.layout_main.addWidget(self.line_edit_servo_3, 4, 0)
        self.layout_main.addWidget(self.line_edit_servo_4, 5, 0)
        self.layout_main.addWidget(self.line_edit_servo_5, 6, 0)
        self.layout_main.addWidget(self.label_profile_arm, 7, 0)

    def move_left(self):
        self.servo_0.movement(-10)

    def move_right(self):
        self.servo_0.movement(10)

    def stop_0(self):
        self.servo_0.servo_running = False

    def update_servo_0(self):
        if self.sender().text() != "":
            self.servo_0.quick_movement(int(self.sender().text()))

    def update_servo_1(self):
        if self.sender().text() != "":
            self.servo_1.quick_movement(int(self.sender().text()))
        self.calc_arm_position()

    def update_servo_2(self):
        if self.sender().text() != "":
            self.servo_2.quick_movement(int(self.sender().text()))
        self.calc_arm_position()

    def update_servo_3(self):
        if self.sender().text() != "":
            self.servo_3.quick_movement(int(self.sender().text()))

    def update_servo_4(self):
        if self.sender().text() != "":
            self.servo_4.quick_movement(int(self.sender().text()))

    def update_servo_5(self):
        if self.sender().text() != "":
            self.servo_5.quick_movement(int(self.sender().text()))

    def closeEvent(self, event):
        self.servo_0.servo_running = False
        self.servo_1.servo_running = False
        self.servo_2.servo_running = False
        self.servo_3.servo_running = False
        self.servo_4.servo_running = False
        self.servo_5.servo_running = False

        self.servo_0.quick_movement(1500)
        self.servo_1.quick_movement(900)
        self.servo_2.quick_movement(2000)
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

    def calc_arm_position(self):
        # Part = 10.5cm
        # SERVO1:
        # width 500 = 90°
        # width 1400 = 0°
        # SERVO2:
        # width 500 = 180°
        # width 2200 = 0°
        pi_rad = math.pi / 180
        is_second_part_lower = False

        # TRIANGLE 1: X
        width_1 = self.servo_1.servo_position
        degrees = 90 - (width_1 - 500) / 10
        rad = degrees * pi_rad
        tri_1_x = math.cos(rad) * 10.5
        print("tri1 x " + str(degrees))

        # TRIANGLE 1: Y
        third_angle = 180 - (degrees + 90)
        rad = third_angle * pi_rad
        tri_1_y = math.cos(rad) * 10.5
        print("tri1 y " + str(third_angle))

        width_2 = self.servo_2.servo_position
        degrees = 180 - (width_2 - 500) / 9.4444
        
        print("if " + str(degrees) + " is highter than " + str(third_angle))

        if degrees > third_angle: # 2nd part is is higher
            print("UPPER")
            # TRIANGLE 2: X
            rec_degree = degrees - third_angle
            rad = rec_degree * pi_rad
            tri_2_x = math.cos(rad) * 10.5
            print("tri2 x " + str(rec_degree))
            
            # TRIANGLE 2: Y
            third_angle_tri_2 = 180 - (rec_degree + 90)
            rad = third_angle_tri_2 * pi_rad
            tri_2_y = math.cos(rad) * 10.5
            print("tri2 y " + str(third_angle_tri_2))
        else: # 2nd part is lower
            print("LOWER")
            is_second_part_lower = True
            rec_degree = (90 + degrees) - third_angle
            third_angle_tri_2 = 180 - (rec_degree + 90)

            # TRIANGLE 2: X
            rad = third_angle_tri_2 * pi_rad
            tri_2_x = math.cos(rad) * 10.5
            print("tri2 x " + str(third_angle_tri_2))

            # TRIANGLE 2: Y
            rad = rec_degree * pi_rad
            tri_2_y = math.cos(rad) * 10.5
            print("tri2 y " + str(rec_degree))
        
        if is_second_part_lower:
            pos1 = round(tri_1_x + tri_2_x, 2)
            pos2 = round(tri_1_y - tri_2_y, 2)
            self.arm_chord = [[tri_1_x, tri_1_y], [pos1, pos2]]
            claw_position = [pos1, pos2]
        else:
            pos1 = round(tri_1_x + tri_2_x, 2)
            pos2 = round(tri_1_y + tri_2_y, 2)
            self.arm_chord = [[tri_1_x, tri_1_y], [pos1, pos2]]
            claw_position = [pos1, pos2]
        self.draw_profile()

    def draw_profile(self):
        size = 200
        part = round(size / 5)        
        centimeter_in_pixels = round((part * 3) / 21)
        servo1 = [round(self.arm_chord[0][0] * centimeter_in_pixels), round(self.arm_chord[0][1] * centimeter_in_pixels)]
        claw = [round(self.arm_chord[1][0] * centimeter_in_pixels), round(self.arm_chord[1][1] * centimeter_in_pixels)]
        print("arm " + str(self.arm_chord))
        print("servo " + str(servo1))
        print("claw " + str(claw))

        img = QImage(size, size, QImage.Format_ARGB32) 
        img.fill(Qt.transparent)

        painter = QPainter(img)
        pen = QPen()
        pen.setCapStyle(Qt.RoundCap)
        pen.setWidth(round(size / 30))

        # DRAW GROUND
        pen.setColor(QColor("#9e9e9e"))
        painter.setPen(pen)
        painter.drawLine(0, part, size, part)

        # DRAW ARM
        pen.setColor(QColor("#e53935"))
        painter.setPen(pen)
        painter.drawLine(part, part, part + servo1[0], part + servo1[1])
        painter.drawLine(part + servo1[0], part + servo1[1], part + claw[0], part + claw[1])

        # DRAW MOTORS
        pen.setColor(QColor("#000000"))
        painter.setPen(pen)
        painter.drawPoint(part, part)
        painter.drawPoint(part + servo1[0], part + servo1[1])
        painter.drawPoint(part + claw[0], part + claw[1])

        painter.end()
        self.label_profile_arm.setPixmap(QPixmap.fromImage(img.mirrored(False, True)))   
