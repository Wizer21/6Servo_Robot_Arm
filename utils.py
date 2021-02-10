from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

positions = {}
pixmap_dict = {}
reference_icon_size = 0
pixelsize = 0
resolution = [0, 0]

class utils:
    def __init__(self, new_pixelsize, new_resolution):
        global positions
        global reference_icon_size
        global pixmap_dict
        global pixelsize
        global resolution

        reference_icon_size = round(new_resolution[0] / 20)
        pixelsize = new_pixelsize
        resolution = new_resolution

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
            "arm": self.scale_pixmap("./files/arm.png", reference_icon_size),
            "right": self.scale_pixmap("./files/right.png", reference_icon_size),
            "play": self.scale_pixmap("./files/play.png", reference_icon_size),
            "trash": self.scale_pixmap("./files/trash.png", reference_icon_size),
            "corner-arrow": self.scale_pixmap("./files/corner-arrow.png", reference_icon_size),
            "run": self.scale_pixmap("./files/run.png", reference_icon_size),
            "eraser": self.scale_pixmap("./files/eraser.png", reference_icon_size)
        }

    def scale_pixmap(self, url, size_ref):
        return QPixmap(url).scaled(size_ref, size_ref, Qt.KeepAspectRatio, Qt.SmoothTransformation)
 
    @staticmethod
    def window_resize_on_rez(window, x, y):
        window.resize(int(resolution[0] * x),int(resolution[1] * y))

    @staticmethod
    def get_resized_pixmap(name, ratio):
        return pixmap_dict[name].scaled(int(reference_icon_size * ratio), int(reference_icon_size * ratio), Qt.KeepAspectRatio, Qt.SmoothTransformation)

    @staticmethod
    def get_pixmap(name):
        return pixmap_dict[name]

    @staticmethod
    def set_icon_resized(widget, name, ratio):
        widget.setIcon(QIcon(pixmap_dict[name].scaled(int(reference_icon_size * ratio), int(reference_icon_size * ratio), Qt.KeepAspectRatio, Qt.SmoothTransformation)))

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
    
    @staticmethod
    def resize_and_font(widget, value):
        widget.setStyleSheet("font-size: {0}px; font: bold;".format(int(pixelsize * value)))

    @staticmethod
    def style_click_button(widget, color):
        style = """QPushButton {
                background-color: <color>;
                padding: 10px;
                border: 0px solid red;
                }
                QPushButton::hover {
                    border: 2px solid white;
                }
                QPushButton::pressed {
                    background-color: #161616;
                    color: <color>;
                    padding: 5px;
                    border: 0px solid transparent
                }"""
        widget.setStyleSheet(style.replace("<color>", color))

    @staticmethod
    def get_resolution():
        return resolution