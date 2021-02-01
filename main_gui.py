from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*

class main_gui(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.widget_central = QWidget(self)
        self.layout_main = QGridLayout(self)
        self.buttontest = QPushButton("Button", self)
        self.buttontest2 = QPushButton("Button2", self)

        self.resize(700, 700)
        self.build()

    def build(self):
        self.setCentralWidget(self.widget_central)
        self.widget_central.setLayout(self.layout_main)
        self.layout_main.addWidget(self.buttontest, 0, 0)
        self.layout_main.addWidget(self.buttontest2, 0, 1)