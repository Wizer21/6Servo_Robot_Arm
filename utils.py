from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

positions = {}

class utils:
    def __init__(self):
        positions = {
            "width_servo0": 0,
            "width_servo1": 0,
            "width_servo2": 0,
            "width_servo3": 0,
            "width_servo4": 0,
            "width_servo5": 0,
            "elbow_pos": [0, 0],
            "claw_pos": [0, 0],
            "is_second_arm_part_lower": False       
        }

    @staticmethod
    def set_position(what, value):
        positions[what] = value
    
    @staticmethod
    def get_position(what):
        return positions[what]
