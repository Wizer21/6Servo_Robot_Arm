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

        self.go_to = False
        self.position_to_reach = []

        self.stop = False
        self.running = False

        self.param = {}
    
    def send_parameters(self, paremeters):
        self.param = paremeters

    def play_new_sequence(self, new_sequence):
        if self.running:
            self.stop = True
            self.wait(2000)
        
        self.stop = False
        self.go_to = False
        self.sequence = new_sequence
        self.start()

    def go_to_position(self, pos):
        if self.running:
            self.stop = True
            self.wait(2000)
        
        self.stop = False
        self.go_to = True
        self.position_to_reach = pos
        self.start()

    def run(self):
        self.running = True
        if self.go_to:
            for movement in self.position_to_reach:
                        self.servo_0.quick_movement(movement[0])
                        self.servo_1.quick_movement(movement[1])
                        self.servo_2.quick_movement(movement[2])
                        self.servo_3.quick_movement(movement[3])
                        self.servo_4.quick_movement(movement[4])
                        self.servo_5.quick_movement(movement[5])
        else:
            if self.param["loop"] and not self.param["infinite"]:
                iterations = int(self.param["loop_times"])
            else:
                iterations = 1
            
            played_sequence = self.sequence.copy()
            already_reversed = False

            while self.param["loop"] and self.param["infinite"] or iterations > 0:

                iterations -= 1

                # DO THE LOOP
                for movement in played_sequence:
                    self.servo_0.quick_movement(movement[0])
                    self.servo_1.quick_movement(movement[1])
                    self.servo_2.quick_movement(movement[2])
                    self.servo_3.quick_movement(movement[3])
                    self.servo_4.quick_movement(movement[4])
                    self.servo_5.quick_movement(movement[5])

                    while self.servo_0.quick or self.servo_1.quick or self.servo_2.quick or self.servo_3.quick or self.servo_4.quick or self.servo_5.quick:
                        sleep(0.005)           

                    if self.stop:
                        self.stop = False
                        self.running = False
                        return     

                    if self.param["pause"]:
                        sleep(int(self.param["pause_time"]) / 1000)

                # IF REVERSE            
                if self.param["reverse"] and not already_reversed:
                    already_reversed = True
                    played_sequence = self.sequence.copy()
                    played_sequence.reverse()
                    iterations += 1
                else:
                    played_sequence = self.sequence.copy()
                    already_reversed = False
                
                if self.stop:
                    self.stop = False
                    self.running = False
                    return
            
            self.stop = False
            self.running = False