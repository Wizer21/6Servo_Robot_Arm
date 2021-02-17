from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import requests

class api_messager(QThread):
    def __init__(self, parent):
        QThread.__init__(self, parent)

        self.url = 'http://127.0.0.1:8080/position/'
        self.data = ""

        self.running = False    

    
    def send_pos(self, new_pos):
        self.data = new_pos

        if not self.running:
            self.start()

    def run(self):   
        self.running = True    

        try:
            r = requests.get(self.url + self.data, timeout=5)
            print(r.text)
        except requests.exceptions.ReadTimeout as err:
            print(err)        
        except requests.exceptions.ConnectionError as err:
            print(err)
        
        self.running = False

