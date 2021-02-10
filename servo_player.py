from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from time import sleep

class servo_player(QThread):
    def __init__(self, parent, servo0, servo1, servo2, servo3, servo4, servo5):
        QThread.__init__(self, parent)
        self.sequence = []
        self.servo_0 = servo0
        self.servo_1 = servo1
        self.servo_2 = servo2
        self.servo_3 = servo3
        self.servo_4 = servo4
        self.servo_5 = servo5
    
    def play_new_sequence(self, new_sequence):
        self.sequence = new_sequence
        self.start()

    def run(self):
        for movement in self.sequence:
            self.servo_0.quick_movement(movement[0])
            self.servo_1.quick_movement(movement[1])
            self.servo_2.quick_movement(movement[2])
            self.servo_3.quick_movement(movement[3])
            self.servo_4.quick_movement(movement[4])
            self.servo_5.quick_movement(movement[5])

            while self.servo_0.quick or self.servo_1.quick or self.servo_2.quick or self.servo_3.quick or self.servo_4.quick or self.servo_5.quick:
                sleep(0.005)
