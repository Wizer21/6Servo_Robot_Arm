from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

pixmap_dict = {}
reference_icon_size = 0
pixelsize = 0
resolution = [0, 0]

class utils:
    def __init__(self, new_pixelsize, new_resolution):
        global reference_icon_size
        global pixmap_dict
        global pixelsize
        global resolution

        reference_icon_size = round(new_resolution[0] / 20)
        pixelsize = new_pixelsize
        resolution = new_resolution

        pixmap_dict = {
            "pi": self.scale_pixmap("./files/pi.png", reference_icon_size),
            "controller": self.scale_pixmap("./files/controller.png", reference_icon_size),
            "arm": self.scale_pixmap("./files/arm.png", reference_icon_size),
            "right": self.scale_pixmap("./files/right.png", reference_icon_size),
            "play": self.scale_pixmap("./files/play.png", reference_icon_size),
            "trash": self.scale_pixmap("./files/trash.png", reference_icon_size),
            "corner-arrow": self.scale_pixmap("./files/corner-arrow.png", reference_icon_size),
            "run": self.scale_pixmap("./files/run.png", reference_icon_size),
            "eraser": self.scale_pixmap("./files/eraser.png", reference_icon_size),
            "reload": self.scale_pixmap("./files/reload.png", reference_icon_size)
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
    def resize_and_color_font(widget, value, color):
        widget.setStyleSheet("font-size: {0}px; color: {1}; font: bold;".format(int(pixelsize * value), color))
    
    @staticmethod
    def resize_and_font(widget, value):
        widget.setStyleSheet("font-size: {0}px; font: bold;".format(int(pixelsize * value)))

    @staticmethod
    def style_click_button(widget, color, padding = 10):
        style = """QPushButton {
                background-color: <color>;
                padding: <pad>px;
                border: 0px solid red;
                }
                QPushButton::hover {
                    border: 2px solid white;
                }
                QPushButton::pressed {
                    background-color: #161616;
                    color: <color>;
                    border: 0px solid transparent
                }"""

        style = style.replace("<pad>", str(padding))
        widget.setStyleSheet(style.replace("<color>", color))

    @staticmethod
    def get_resolution():
        return resolution

    @staticmethod
    def clear_layout(layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clear_layout(child.layout())