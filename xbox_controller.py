from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from evdev import*

class Communication(QObject):
    claw_move = pyqtSignal(int)
    claw_stop = pyqtSignal()

class xbox_controller(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.messager = Communication()
        self.gamepad = InputDevice('/dev/input/event4')

        self.buttons = {
            307: "Y",
            305: "B",
            304: "A",
            306: "X",
            309: "RB",
            308: "LB",
            172: "Xbox",
            310: "View",
            311: "Menu",
            313: "Joy1 clicked",
            312: "Joy2 clicked"
        }

        self.lt = 10
        self.rt = 9

        self.joy1_y = 1
        self.joy1_x = 0
        self.joy1_position = [0, 0]

        self.joy2_y = 5
        self.joy2_x = 2
        self.joy2_position = [0, 0]

        self.directionnal_button_x = 16
        self.directionnal_button_y = 17

        self.holded_button = 0
        self.start()

    def run(self):
        for event in self.gamepad.read_loop():
            #BUTTON
            if event.type == ecodes.EV_KEY: 
                val_button = int(event.value)
                code_button = int(event.code)

                if code_button == 309: # RB
                    if val_button == 0:
                        self.messager.claw_stop.emit()
                    else:
                        self.messager.claw_move.emit(10)
                elif code_button == 308: # LB
                    if val_button == 0:
                        self.messager.claw_stop.emit()
                    else:
                        self.messager.claw_move.emit(-10)

            #JOYSTICK
            elif event.type == ecodes.EV_ABS: 
                # JOY 1
                if event.code == self.joy1_x:
                    self.joy1_position[0] = int(event.value)
                    print("JOY 1: X " + str(self.joy1_position[0]) + " Y " + str(self.joy1_position[1]))

                elif event.code == self.joy1_y: 
                    self.joy1_position[1] = int(event.value)
                    print("JOY 1: X " + str(self.joy1_position[0]) + " Y " + str(self.joy1_position[1]))

                # JOY 2
                elif event.code == self.joy2_x:
                    self.joy2_position[0] = int(event.value)
                    print("JOY 2: X " + str(self.joy2_position[0]) + " Y " + str(self.joy2_position[1]))

                if event.code == self.joy2_y: 
                    self.joy2_position[1] = int(event.value)
                    print("JOY 2: X " + str(self.joy2_position[0]) + " Y " + str(self.joy2_position[1]))

                # DIRECTIONAL BUTTON AXIS Y
                elif event.code == self.directionnal_button_y:  
                    pos = int(str(event.value).replace("L", ""))
                    if pos > 0:
                        print("Down pressed")
                        self.holded_button = "Down"
                    elif pos < 0:
                        print("Up pressed")
                        self.holded_button = "Up"
                    elif pos == 0:
                        print(self.holded_button + " released")

                # DIRECTIONAL BUTTON AXIS X
                elif event.code == self.directionnal_button_x:
                    pos = int(str(event.value).replace("L", ""))
                    if pos > 0:
                        print("Right pressed")
                        self.holded_button = "Right"
                    elif pos < 0:
                        print("Left pressed")
                        self.holded_button = "Left"
                    elif pos == 0:
                        print(self.holded_button + " released")

                elif event.code == self.lt:
                    print("LT pressed at " + str(event.value))
                
                elif event.code == self.rt:
                    print("self.RT pressed at " + str(event.value))
  