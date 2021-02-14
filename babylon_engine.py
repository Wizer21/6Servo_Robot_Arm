from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from PyQt5.QtWebEngineWidgets import QWebEngineView

class babylon_engine(QWebEngineView):
    def __init__(self, parent):
        QWebEngineView.__init__(self, parent)

        self.load("http://127.0.0.1:8080/")
        self.show()