from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from servo_thread import*
from time import sleep
from xbox_controller import*
import math
from thread_axes import*
import os

class main_gui(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.pi = pigpio.pi()
        self.controller = xbox_controller()
        self.arm_chord = [[0, 0], [0, 0]]
        self.is_second_part_lower = False
        self.is_first_part_frontward = True
        self.second_part_front = True
        self.heatTimer = QTimer()

        # WIDGETS
        self.widget_central = QWidget(self)
        self.layout_main = QGridLayout(self)
        self.layout_header = QGridLayout(self)
        self.label_claw = QLabel(self)
        self.label_title = QLabel("Arm Controller", self)

        self.layout_right_header = QGridLayout(self)
        self.label_raspberry = QLabel(self)
        self.label_heat = QLabel("0°", self)
        self.label_controller = QLabel("controler icon", self)
        self.label_controller_name = QLabel("ev4", self)

        self.label_profile_arm = QLabel(self)
        
        # SETUP SERVO THREADS
        pi = pigpio.pi()
        self.servo_0 = servo_thread(self, pi, 1500, 0, [500, 2500]) # MORE IS LEFT
        self.servo_1 = servo_thread(self, pi, 1700, 1, [500, 2250]) # MORE IS DOWN
        self.servo_2 = servo_thread(self, pi, 1712, 2, [500, 2220]) # MORE IS DOWN
        self.servo_3 = servo_thread(self, pi, 1300, 3, [500, 2500]) # MORE IS UP
        self.servo_4 = servo_thread(self, pi, 1500, 4, [500, 2500]) # MORE IS RIGHT
        self.servo_5 = servo_thread(self, pi, 1500, 5, [1300, 2500]) # MORE IS WIDER
        self.thread_y = thread_axes(self, self.servo_1, self.servo_2, False)
        self.thread_x = thread_axes(self, self.servo_1, self.servo_2, True)

        self.resize(700, 700)
        self.build()
        self.update_heat()

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

        # HEAT CONTROL
        self.heatTimer.timeout.connect(self.update_heat)

    def build(self):
        self.setCentralWidget(self.widget_central)
        self.widget_central.setLayout(self.layout_main)

        # HEADER
        self.layout_main.addLayout(self.layout_header, 0, 0)
        self.layout_header.addWidget(self.label_claw, 0, 0)
        self.layout_header.addWidget(self.label_title, 0, 1)
        self.layout_header.addWidget(self.label_profile_arm, 1, 0, 1, 2)

        self.layout_header.addLayout(self.layout_right_header, 0, 2, 2, 1)
        self.layout_right_header.addWidget(self.label_heat, 0, 0)
        self.layout_right_header.addWidget(self.label_raspberry, 0, 1)
        self.layout_right_header.addWidget(self.label_controller_name, 1, 0)
        self.layout_right_header.addWidget(self.label_controller, 1, 1)

        # CUSTOM
        self.layout_header.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.layout_right_header.setAlignment(Qt.AlignRight)

        self.layout_header.setColumnStretch(0, 0)
        self.layout_header.setColumnStretch(1, 0)
        self.layout_header.setColumnStretch(2, 1)

        self.label_claw.setPixmap(utils.get_resized_pixmap("arm", 0.5))
        self.label_raspberry.setPixmap(utils.get_resized_pixmap("pi", 0.5))
        self.label_controller.setPixmap(utils.get_resized_pixmap("controller", 0.5))

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
        # Part = 10.5cm
        # SERVO1:
        # width 500 = 90°
        # width 1400 = 0°
        # SERVO2:
        # width 500 = 180°
        # width 2220 = 0°
        pi_rad = math.pi / 180

        # TRIANGLE 1: X
        width_1 = self.servo_1.servo_position
        first_degrees = 180 - (width_1 - 500) / 9.722222
        print("DEGREE " + str(first_degrees))

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
        print("degre arm2", str(degrees))

        back_angle = first_degrees - ((first_degrees - 90) * 2)
        #deg = degrees - 90
        if degrees > back_angle:
            # SECOND PART HIGHT AND BACKWARD
            print("1")
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
            print("2")
            is_second_part_lower = False
            second_part_front = True
            # TRIANGLE 2: X
            if not is_first_part_frontward:
                rec_degree = degrees + (first_degrees - 90)
            else:
                rec_degree = degrees - (90 - first_degrees)

            rad = rec_degree * pi_rad
            tri_2_x = math.cos(rad) * 10.5
            
            print("degrees", str(degrees))
            print("third_angle", str(third_angle))
            print("rec_degree", str(rec_degree))
            # TRIANGLE 2: Y
            third_angle_tri_2 = 180 - (rec_degree + 90)
            print("third_angle_tri_2", str(third_angle_tri_2))
            rad = third_angle_tri_2 * pi_rad
            tri_2_y = math.cos(rad) * 10.5
        else: 
            print("3")
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

        print("tri_1_x", str(tri_1_x))
        print("tri_2_x", str(tri_2_x))
        print("tri_1_y", str(tri_1_y))
        print("tri_2_y", str(tri_2_y))

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
        size = 200
        part = round(size / 5)        
        centimeter_in_pixels = round((part * 3) / 21)
        servo1 = [round(self.arm_chord[0][0] * centimeter_in_pixels), round(self.arm_chord[0][1] * centimeter_in_pixels)]
        claw = [round(self.arm_chord[1][0] * centimeter_in_pixels), round(self.arm_chord[1][1] * centimeter_in_pixels)]

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

        #self.label_profile_arm.setPixmap(QPixmap.fromImage(img.mirrored(False, True)))   
