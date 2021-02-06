from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

positions = {}
pixmap_dict = {}
reference_icon_size = 0
pixelsize = 0

class utils:
    def __init__(self, new_pixelsize, new_resolution):
        global positions
        global reference_icon_size
        global pixmap_dict
        global pixelsize

        reference_icon_size = round(new_resolution[0] / 20)
        pixelsize = new_pixelsize

        positions = {
            "width_servo0": 0,
            "width_servo1": 0,
            "width_servo2": 0,
            "width_servo3": 0,
            "width_servo4": 0,
            "width_servo5": 0,
            "elbow_pos": [0, 0],
            "claw_pos": [1, 1],
            "is_second_arm_part_lower": False       
        }

        pixmap_dict = {
            "pi": self.scale_pixmap("./files/pi.png", reference_icon_size),
            "controller": self.scale_pixmap("./files/controller.png", reference_icon_size),
            "arm": self.scale_pixmap("./files/arm.png", reference_icon_size)
        }

    def scale_pixmap(self, url, size_ref):
        return QPixmap(url).scaled(size_ref, size_ref, Qt.KeepAspectRatio, Qt.SmoothTransformation)
 
    @staticmethod
    def get_resized_pixmap(name, ratio):
        return pixmap_dict[name].scaled(int(reference_icon_size * ratio), int(reference_icon_size * ratio), Qt.KeepAspectRatio, Qt.SmoothTransformation)

    @staticmethod
    def get_pixmap(name):
        return pixmap_dict[name]

    @staticmethod
    def set_position(what, value):
        global positions
        positions[what] = value
    
    @staticmethod
    def get_position(what):
        return positions[what]

    @staticmethod
    def resize_and_color_font(widget, value, color):
        widget.setStyleSheet("font-size: {0}px; color: {1}; font: bold;".format(int(pixelsize * value), color))