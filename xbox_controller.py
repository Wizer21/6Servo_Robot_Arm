from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from evdev import*

class Communication(QObject):
    claw_move = pyqtSignal(int)
    claw_stop = pyqtSignal()
    claw_rotation = pyqtSignal(int)
    claw_rotation_stop = pyqtSignal()
    claw_y_move = pyqtSignal(int)
    claw_y_stop = pyqtSignal()
    robot_rotation = pyqtSignal(int)
    robot_rotation_stop = pyqtSignal()
    move_x = pyqtSignal(int)
    stop_x = pyqtSignal()
    move_y = pyqtSignal(int)
    stop_y = pyqtSignal()
    push_position = pyqtSignal()

class xbox_controller(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.messager = Communication()

        try:
            self.gamepad = InputDevice('/dev/input/event4')
        except FileNotFoundError:
            print("NO CONTROLLER FOUND")
            return

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

        self.joy2_y = 5
        self.joy2_x = 2

        self.directionnal_button_x = 16
        self.directionnal_button_y = 17

        self.holded_button = 0
        self.start()

    def run(self):
        for event in self.gamepad.read_loop():
            val_button = int(event.value)
            code_button = int(event.code)
            #BUTTON
            if event.type == ecodes.EV_KEY:             
                if code_button == 309: # RB
                    if val_button == 0:
                        self.messager.claw_rotation_stop.emit()
                    else:
                        self.messager.claw_rotation.emit(10)
                elif code_button == 308: # LB
                    if val_button == 0:
                        self.messager.claw_rotation_stop.emit()
                    else:
                        self.messager.claw_rotation.emit(-10)
                elif code_button == 310: # VIEW
                    if val_button == 0:
                        self.messager.push_position.emit()


            #JOYSTICK
            elif event.type == ecodes.EV_ABS: 
                # JOY 1
                if code_button == self.joy1_x:
                    if not 29767.5 < val_button < 35767.5:
                        if val_button < 32767.5:
                            self.messager.robot_rotation.emit(-round((val_button - 32767.5) / 3276.75))
                        else:
                            self.messager.robot_rotation.emit(round((32767.5 - val_button) / 3276.75))
                    else:
                        self.messager.robot_rotation_stop.emit()

                elif code_button == self.joy1_y:
                    if not 29767.5 < val_button < 35767.5:
                        if val_button < 32767.5:
                            self.messager.move_x.emit(-round((val_button - 32767.5) / 3276.75))
                        else:
                            self.messager.move_x.emit(round((32767.5 - val_button) / 3276.75))
                    else:
                        self.messager.stop_x.emit() 

                # JOY 2
                elif code_button == self.joy2_x:
                    if not 29767.5 < val_button < 35767.5:
                        if val_button < 32767.5:
                            self.messager.robot_rotation.emit(-round((val_button - 32767.5) / 3276.75))
                        else:
                            self.messager.robot_rotation.emit(round((32767.5 - val_button) / 3276.75))
                    else:
                        self.messager.robot_rotation_stop.emit()

                if code_button == self.joy2_y:
                    if not 29767.5 < val_button < 35767.5:
                        if val_button < 32767.5:
                            self.messager.move_y.emit(-round((val_button - 32767.5) / 3276.75))
                        else:
                            self.messager.move_y.emit(round((32767.5 - val_button) / 3276.75))
                    else:
                        self.messager.stop_y.emit() 

                # DIRECTIONAL BUTTON AXIS Y
                elif code_button == self.directionnal_button_y:  
                    pos = int(str(event.value).replace("L", ""))
                    if pos > 0:
                        self.messager.claw_y_move.emit(-10)
                    elif pos < 0:
                        self.messager.claw_y_move.emit(10)
                    elif pos == 0:
                        self.messager.claw_y_stop.emit()

                # DIRECTIONAL BUTTON AXIS X
                elif code_button == self.directionnal_button_x:
                    pos = int(str(val_button).replace("L", ""))
                    if pos > 0:
                        print("Right pressed")
                        self.holded_button = "Right"
                    elif pos < 0:
                        print("Left pressed")
                        self.holded_button = "Left"
                    elif pos == 0:
                        print(self.holded_button + " released")
                
                elif code_button == self.rt: # RT
                    if val_button == 0:
                        self.messager.claw_stop.emit()
                    else:
                        self.messager.claw_move.emit(round(val_button / 102.6))
                elif code_button == self.lt: # LT                    
                    if val_button == 0:
                        self.messager.claw_stop.emit()
                    else:
                        self.messager.claw_move.emit(-round(val_button / 102.6))