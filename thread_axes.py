from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from time import sleep
import math
from utils import *

class thread_axes(QThread):
    def __init__(self, new_parent, servo1, servo2, servo3, new_is_x_axes):
        QThread.__init__(self, parent = new_parent)
        self.action = 0
        self.run_movement = False
        self.servo_1 = servo1
        self.servo_2 = servo2
        self.servo_3 = servo3
        self.parent = new_parent
        self.is_x_axes = new_is_x_axes

        self.claw_pos = [1, 1]

        self.lock_claw = False
        # POSITION OF CLAW IN THE SPACE
        self.absolute_claw_angle = 0

    def call_movement(self, new_action):
        self.action = new_action

        if not self.run_movement:
            self.run_movement = True
            self.start()

    def run(self):
        while self.run_movement:
            if self.is_x_axes:
                self.claw_pos[0] += self.action
            else:
                self.claw_pos[1] += self.action

            if self.claw_pos[0] < 0:
                is_arm_front = False
                self.claw_pos[0] = -self.claw_pos[0]
            else:
                is_arm_front = True

            #    M = motor  
            #                         CLAW
            #        M2  O--------------O
            #           / \          -  |
            #          /   \     -      |
            #         /      X          |
            #        /   -              |
            #       / -                 |
            #   M1 O ------------------ A

            M1_X = (math.sqrt(self.claw_pos[0] ** 2 + self.claw_pos[1] ** 2)) / 2

            if M1_X >= 10.5:
                M1_X = 10.4

            M2_X = math.sqrt(10.5 ** 2 - M1_X ** 2)

            M2_M1_X_angle = (math.atan(M2_X / M1_X)) * 57.2958
            M1_M2_X_angle = 180 - (90 + M2_M1_X_angle)


            X_M1_A_angle = (math.atan(self.claw_pos[1] / self.claw_pos[0])) * 57.2958

            M2_M1_A_angle = X_M1_A_angle + M2_M1_X_angle
            M1_M2_CLAW_angle_minus_90 = (M1_M2_X_angle * 2) - 90

            if not is_arm_front:
                angle_m1 = 180 - (X_M1_A_angle - M2_M1_X_angle)
                first_motor_width = 2250 - round(angle_m1 / 0.102857)
            else:
                first_motor_width = 2250 - round(M2_M1_A_angle / 0.102857)
            second_motor_width = 2220 - round(M1_M2_CLAW_angle_minus_90 / 0.104651)

            # SET CLAW POSITION
            if self.lock_claw:
                absolute_0 = (90 - M2_M1_A_angle) + (90 - M1_M2_CLAW_angle_minus_90)
                M3_degree = absolute_0 + self.absolute_claw_angle

                M3_width = 640 + round(M3_degree / 0.10975)
                print("AVERAGE VALUE ", str(round(M3_degree / 0.10975)))
                print("M3_width", str(M3_width))
                self.servo_3.direct_movement(M3_width)
                    
            # SET ARM POSITION
            self.servo_1.direct_movement(first_motor_width)
            self.servo_2.direct_movement(second_motor_width)
            self.parent.calc_arm_position()
