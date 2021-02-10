from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
import time
import pigpio
from utils import*

class Communication(QObject):
   update_displayed_pos = pyqtSignal(int, int)

class servo_thread(QThread):
   def __init__(self, parent, pi, new_pin, width_range = [500, 2500]):
      QThread.__init__(self)
      self.setParent(parent)
      self.quick = False
      self.messager = Communication()

      self.servo_position = 0
      self.servo_action = 0
      self.servo_quick_action = 0
      self.servo_running = False
      self.pin = new_pin

      self.min_width = width_range[0]
      self.max_width = width_range[1]

      self.pi = pi
      self.address = 0x40
      self._RESTART = 1<<7
      self._AI = 1<<5
      self._SLEEP = 1<<4
      self._ALLCALL = 1<<0
      self._OCH = 1<<3
      self._OUTDRV = 1<<2
      self._MODE1 = 0x00
      self._MODE2 = 0x01
      self._PRESCALE = 0xFE
      self._ALL_LED_ON_L = 0x06
      self._LED0_ON_L = 0x06

      self.h = self.pi.i2c_open(1, self.address)

      self._write_reg(self._MODE1, self._AI | self._ALLCALL)
      self._write_reg(self._MODE2, self._OCH | self._OUTDRV)
      time.sleep(0.0005)

      mode = self._read_reg(self._MODE1)
      self._write_reg(self._MODE1, mode & ~self._SLEEP)
      time.sleep(0.0005)

      self.set_frequency(60)

   def set_frequency(self, frequency):
      prescale = int(round(25000000.0 / (4096.0 * frequency)) - 1)

      if prescale < 3:
         prescale = 3
      elif prescale > 255:
         prescale = 255

      mode = self._read_reg(self._MODE1)
      self._write_reg(self._MODE1, (mode & ~self._SLEEP) | self._SLEEP)
      self._write_reg(self._PRESCALE, prescale)
      self._write_reg(self._MODE1, mode)

      time.sleep(0.0005)

      self._write_reg(self._MODE1, mode | self._RESTART)

      self._frequency = (25000000.0 / 4096.0) / (prescale + 1)
      self._pulse_width = (1000000.0 / self._frequency)

   def set_pulse_width(self, channel, width):
      self.set_duty_cycle(channel, (float(width) / self._pulse_width) * 100.0)
         
   def set_duty_cycle(self, channel, percent):
      steps = int(round(percent * (4096.0 / 100.0)))
      if steps < 0:
         on = 0
         off = 4096
      elif steps > 4095:
         on = 4096
         off = 0
      else:
         on = 0
         off = steps

      if (channel >= 0) and (channel <= 15):
         self.pi.i2c_write_i2c_block_data(self.h, self._LED0_ON_L+4*channel,
            [on & 0xFF, on >> 8, off & 0xFF, off >> 8])

      else:
         self.pi.i2c_write_i2c_block_data(self.h, self._ALL_LED_ON_L,
            [on & 0xFF, on >> 8, off & 0xFF, off >> 8])

   def cancel(self):
      self.pi.i2c_close(self.h)

   def _write_reg(self, reg, byte):
      self.pi.i2c_write_byte_data(self.h, reg, byte)

   def _read_reg(self, reg):
      return self.pi.i2c_read_byte_data(self.h, reg)
   
   def quick_movement(self, position):
      if position != self.servo_position:
         
         self.servo_quick_action = position
         self.servo_running = False
         self.quick = True
         self.start()

   def movement(self, action):
      self.servo_action = action

      if not self.servo_running:
         self.servo_running = True
         self.start()

   def direct_movement(self, new_pos):
      if not self.min_width <= new_pos <= self.max_width:
            print("OUT OF RANGE " + str(new_pos))
            self.quick = False
            return

      if self.servo_position > new_pos:
         diff = self.servo_position - new_pos
      elif self.servo_position < new_pos:
         diff = new_pos - self.servo_position
      else:
         return

      # SERVO MOTOR NEED 0.001666sec TO RUN 1 DEGREE
      sleep_time = (diff / 11.1111) * 0.001666

      self.set_pulse_width(self.pin, new_pos) 
      time.sleep(sleep_time)

      self.servo_position = new_pos
      utils.set_position("width_servo" + str(self.pin), new_pos)
      self.messager.update_displayed_pos.emit(self.pin, self.servo_position)

   def run(self):
      if self.quick:
         if not self.min_width <= self.servo_quick_action <= self.max_width:
            print("OUT OF RANGE " + str(self.servo_quick_action))
            self.quick = False
            return

         if self.servo_position > self.servo_quick_action:
            diff = self.servo_position - self.servo_quick_action
         elif self.servo_position < self.servo_quick_action:
            diff = self.servo_quick_action - self.servo_position
         else:
            self.quick = False
            return

         # SERVO MOTOR NEED 0.001666sec TO RUN 1 DEGREE
         sleep_time = (diff / 11.1111) * 0.001666

         self.set_pulse_width(self.pin, self.servo_quick_action) 
         print("sleep", str(sleep_time))
         time.sleep(sleep_time)
         self.servo_position = self.servo_quick_action

         utils.set_position("width_servo" + str(self.pin), self.servo_position)
         self.messager.update_displayed_pos.emit(self.pin, self.servo_position)

         self.quick = False
         print("servo end")
      else:
         while self.servo_running:
            newpos = self.servo_position + self.servo_action
            if not self.min_width <= newpos <= self.max_width:
               print("OUT OF RANGE " + str(newpos))
               self.servo_running = False
               break

            self.set_pulse_width(self.pin, newpos) 
            time.sleep(0.01)
            self.servo_position = newpos
            utils.set_position(self.pin, self.servo_position)
            self.messager.update_displayed_pos.emit(self.pin, self.servo_position)



