from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from time import sleep
import math
from utils import *

class thread_axes(QThread):
    def __init__(self, new_parent, servo1, servo2, new_is_x_axes):
        QThread.__init__(self, parent = new_parent)
        self.action = 0
        self.run_movement = False
        self.servo_1 = servo1
        self.servo_2 = servo2
        self.parent = new_parent
        self.is_x_axes = new_is_x_axes

    def call_movement(self, new_action):
        self.action = new_action

        if not self.run_movement:
            self.run_movement = True
            self.start()
    
    def run(self):
        while self.run_movement:
            claw_pos = utils.get_position("claw_pos").copy()
            if self.is_x_axes:
                claw_pos[0] += self.action
            else:
                claw_pos[1] += self.action
            print(str(claw_pos))
            
            #    M = motor  
            #                         CLAW
            #        M2  O--------------O
            #           / \          -  |
            #          /   \     -      |
            #         /      X          |
            #        /   -              |
            #       / -                 |
            #   M1 O ------------------ A

            # CALCULATE TANGENT: [0, 0] to claw
            M1_X = (math.sqrt(claw_pos[0] ** 2 + claw_pos[1] ** 2)) / 2
            X_M1_A_angle = (math.atan(claw_pos[1] / claw_pos[0])) * 57.2958

            # CALCULATE MIDDLE POINT TO ELBOW POS
            if M1_X >= 10.5:
                M1_X = 10.4
            M2_X = math.sqrt(10.5 ** 2 - M1_X ** 2)
            M2_M1_X_angle = (math.atan(M2_X / M1_X)) * 57.2958

            # CALCULATE THIRD ANGLE OF THE SECOND RECTANGLE
            M1_M2_X_angle = 180 - (90 + M2_M1_X_angle)

            M2_M1_A_angle = X_M1_A_angle + M2_M1_X_angle
            M1_M2_CLAW_angle_minus_90 = (M1_M2_X_angle * 2) - 90

            first_motor_width = 1400 - round(M2_M1_A_angle / 0.1)
            second_motor_width = 2200 - round(M1_M2_CLAW_angle_minus_90 / 0.10588)

            print(str(first_motor_width) + " " + str(second_motor_width))

            self.servo_1.direct_movement(first_motor_width)
            self.servo_2.direct_movement(second_motor_width)
            self.parent.calc_arm_position()
            #sleep(0.1)
